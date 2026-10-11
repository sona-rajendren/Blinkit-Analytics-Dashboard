"""Join the Blinkit tables, compute KPIs, and export dashboard assets.

Run from the project root:  python src/analysis.py
"""
import json
from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"
OUT = ROOT / "outputs"
(OUT / "charts").mkdir(parents=True, exist_ok=True)
rd = lambda n: pd.read_csv(RAW / f"blinkit_{n}.csv")


def load():
    orders, items, products = rd("orders"), rd("order_items"), rd("products")
    customers, delivery, feedback = rd("customers"), rd("delivery_performance"), rd("customer_feedback")
    for name, t in [("orders", orders), ("order_items", items), ("delivery", delivery), ("feedback", feedback)]:
        assert t["order_id"].is_unique, f"{name}: order_id is not unique, joins would duplicate orders"
    orders["order_date"] = pd.to_datetime(orders["order_date"])

    fact = (orders
            .merge(items, on="order_id", how="left")
            .merge(products[["product_id", "product_name", "category", "brand", "margin_percentage"]], on="product_id", how="left")
            .merge(customers[["customer_id", "customer_segment", "area"]], on="customer_id", how="left")
            .merge(delivery[["order_id", "delivery_time_minutes", "distance_km", "reasons_if_delayed"]], on="order_id", how="left")
            .merge(feedback[["order_id", "rating", "sentiment", "feedback_category"]], on="order_id", how="left"))
    fact["month"] = fact["order_date"].dt.strftime("%Y-%m")
    fact["hour"] = fact["order_date"].dt.hour
    return fact, rd("marketing_performance"), rd("inventory"), products


def main():
    fact, mkt, inv, products = load()
    fact.to_csv(ROOT / "data" / "orders_enriched.csv", index=False)

    # marketing: dates are ISO
    mkt["date"] = pd.to_datetime(mkt["date"])
    mkt["month"] = mkt["date"].dt.strftime("%Y-%m")
    # inventory: dates are dd-mm-yyyy
    inv["date"] = pd.to_datetime(inv["date"], format="%d-%m-%Y")
    inv["month"] = inv["date"].dt.strftime("%Y-%m")
    inv = inv.merge(products[["product_id", "category"]], on="product_id", how="left")

    # ---- KPIs + summary tables
    print("Orders:", len(fact), "| Revenue:", round(fact.order_total.sum(), 2),
          "| AOV:", round(fact.order_total.mean(), 2), "| On-time %:", round((fact.delivery_status == "On Time").mean() * 100, 1))
    tables = {
        "revenue_by_month": fact.groupby("month").agg(orders=("order_id", "size"), revenue=("order_total", "sum"), avg_order_value=("order_total", "mean")),
        "revenue_by_category": fact.groupby("category").agg(orders=("order_id", "size"), revenue=("order_total", "sum"), avg_rating=("rating", "mean")).sort_values("revenue", ascending=False),
        "revenue_by_segment": fact.groupby("customer_segment").agg(orders=("order_id", "size"), revenue=("order_total", "sum")).sort_values("revenue", ascending=False),
        "revenue_by_payment": fact.groupby("payment_method").agg(orders=("order_id", "size"), revenue=("order_total", "sum")).sort_values("revenue", ascending=False),
        "delivery_status": fact.groupby("delivery_status").agg(orders=("order_id", "size"), avg_delay_min=("delivery_time_minutes", "mean"), avg_rating=("rating", "mean")),
        "marketing_by_campaign": mkt.groupby("campaign_name").agg(spend=("spend", "sum"), revenue=("revenue_generated", "sum"), conversions=("conversions", "sum"), clicks=("clicks", "sum"), impressions=("impressions", "sum")).assign(roas=lambda d: d.revenue / d.spend).sort_values("roas", ascending=False),
        "marketing_by_channel": mkt.groupby("channel").agg(spend=("spend", "sum"), revenue=("revenue_generated", "sum")).assign(roas=lambda d: d.revenue / d.spend),
        "inventory_by_category": inv.groupby("category").agg(stock_received=("stock_received", "sum"), damaged_stock=("damaged_stock", "sum")).assign(damage_rate=lambda d: d.damaged_stock / d.stock_received).sort_values("damage_rate", ascending=False),
    }
    for name, t in tables.items():
        t.round(3).to_csv(OUT / f"{name}.csv")

    # ---- static charts
    plt.rcParams.update({"axes.spines.top": False, "axes.spines.right": False})
    green, yellow = "#0C831F", "#F8CB46"
    t = tables["revenue_by_month"]
    fig, ax = plt.subplots(figsize=(9, 4)); ax.plot(t.index, t.revenue, color=green, marker="o")
    ax.set_title("Revenue by month"); plt.xticks(rotation=60); fig.tight_layout()
    fig.savefig(OUT / "charts" / "revenue_by_month.png", dpi=140); plt.close(fig)
    t = tables["revenue_by_category"].sort_values("revenue")
    fig, ax = plt.subplots(figsize=(8, 5)); ax.barh(t.index, t.revenue, color=green)
    ax.set_title("Revenue by category"); fig.tight_layout()
    fig.savefig(OUT / "charts" / "revenue_by_category.png", dpi=140); plt.close(fig)
    t = tables["marketing_by_campaign"]
    fig, ax = plt.subplots(figsize=(8, 4)); ax.bar(t.index, t.roas, color=yellow, edgecolor=green)
    ax.set_title("ROAS by campaign"); plt.xticks(rotation=35, ha="right"); fig.tight_layout()
    fig.savefig(OUT / "charts" / "roas_by_campaign.png", dpi=140); plt.close(fig)

    # ---- payload for the HTML dashboard (column-oriented; filters run in the browser)
    cols = lambda df, m: {k: df[v].tolist() for k, v in m.items()}
    payload = {
        "orders": cols(fact.assign(reason=fact.reasons_if_delayed.fillna("")), {
            "ym": "month", "hour": "hour", "cat": "category", "prod": "product_name", "seg": "customer_segment",
            "pay": "payment_method", "status": "delivery_status", "rev": "order_total",
            "dmin": "delivery_time_minutes", "dist": "distance_km", "rating": "rating",
            "sent": "sentiment", "fb": "feedback_category"}),
        "marketing": cols(mkt, {"ym": "month", "camp": "campaign_name", "ch": "channel", "aud": "target_audience",
                                "imp": "impressions", "clk": "clicks", "conv": "conversions",
                                "spend": "spend", "rev": "revenue_generated"}),
        "inventory": cols(inv.groupby(["month", "category"], as_index=False)[["stock_received", "damaged_stock"]].sum(),
                          {"ym": "month", "cat": "category", "rec": "stock_received", "dmg": "damaged_stock"}),
    }
    (ROOT / "dashboard" / "data.js").write_text("window.BLINKIT = " + json.dumps(payload, separators=(",", ":")) + ";\n")
    print("Wrote data/orders_enriched.csv, outputs/*.csv, outputs/charts/*.png, dashboard/data.js")


if __name__ == "__main__":
    main()
