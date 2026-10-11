# 📊 Blinkit Analytics Dashboard

## 📌 Project Overview

The **Blinkit Analytics Dashboard** is a Data Analysis and Visualization project designed to analyze grocery delivery data and generate meaningful business insights.

The project uses Python for data processing and analysis, SQL for querying data, and HTML, CSS, JavaScript, and Chart.js to create an interactive dashboard.

## 🎯 Project Objectives

- Analyze sales and revenue performance.
- Evaluate delivery performance.
- Understand customer feedback and ratings.
- Analyze marketing campaign performance.
- Monitor inventory status.
- Present insights through interactive visualizations.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Data analysis and processing |
| Pandas | Data manipulation |
| NumPy | Numerical operations |
| Matplotlib | Data visualization |
| SQL | Data querying |
| HTML | Dashboard structure |
| CSS | Dashboard styling |
| JavaScript | Dashboard interactivity |
| Chart.js | Charts and graphs |

## ✨ Key Features

- 📈 **Sales Analysis:** Analyze orders, revenue, and average order value.
- 🚚 **Delivery Analysis:** Evaluate delivery performance and on-time delivery rates.
- ⭐ **Customer Feedback:** Explore customer ratings and feedback.
- 📢 **Marketing Analysis:** Examine marketing campaign performance.
- 📦 **Inventory Analysis:** Analyze stock availability and inventory status.
- 📊 **Interactive Dashboard:** Visualize key metrics using charts and KPI cards.

## 📂 Project Structure

```text
blinkit-analytics-dashboard/
│
├── data/
│   ├── raw/
│   └── orders_enriched.csv
│
├── src/
│   └── analysis.py
│
├── dashboard/
│   ├── index.html
│   └── data.js
│
├── outputs/
│
├── sql/
│   └── queries.sql
│
├── requirements.txt
└── README.md
```
## ⚙️ Installation and Setup

### Step 1: Clone the Repository

```bash
git clone https://github.com/sona-rajendren/blinkit-analytics-dashboard.git
```

Navigate to the project directory:

```bash
cd blinkit-analytics-dashboard
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

If you do not have a `requirements.txt` file, install the main Python libraries:

```bash
pip install pandas numpy matplotlib
```

### Step 3: Run the Data Analysis

Execute the analysis script:

```bash
python src/analysis.py
```

This script processes the available datasets and generates analysis outputs used by the dashboard.

### Step 4: Open the Dashboard

1. Navigate to the `dashboard` folder.
2. Open `index.html` in your web browser.
3. Explore the available charts, KPIs, and visualizations.

**Note:** If the dashboard requires `data.js`, make sure the analysis script has generated it successfully.

## 📊 Key Performance Indicators

The dashboard focuses on the following metrics:

- Total Orders
- Total Revenue
- Average Order Value
- On-Time Delivery Percentage
- Customer Ratings
- Marketing Performance
- Inventory Status

## 🔍 Expected Insights

The analysis helps identify:

- Sales and revenue trends.
- Delivery performance patterns.
- Customer satisfaction trends.
- Marketing campaign performance.
- Inventory-related issues.
- Opportunities for operational improvement.

*The insights depend on the datasets included in the project. The results should not be interpreted as actual Blinkit business figures.*

## 📚 Project Learning Outcomes

Through this project, the following concepts are demonstrated:

- Data cleaning and preprocessing.
- Exploratory Data Analysis (EDA).
- Data aggregation and transformation.
- SQL queries and data analysis.
- Data visualization.
- Interactive dashboard development.
- Communicating insights through visualizations.

## 🚀 Future Enhancements

- Add real-time data integration.
- Include advanced predictive analytics.
- Improve dashboard filtering and interactivity.
- Develop sales forecasting models.
- Add automated report generation.

## 👩‍💻 Author

**Sona Rajendren**

MCA Student | Presidency University
