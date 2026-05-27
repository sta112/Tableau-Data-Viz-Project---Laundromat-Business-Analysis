# Tableau-Dashboard---Laundromat-Business-Analysis
Tableau Dashboard to highlight key metrics in order to understand business health
Markdown
# Laundromat Business Analysis

## Interactive Dashboard
Click the preview image below to view and interact with the live dashboard on Tableau Public.

[![Tableau Dashboard Preview](Dashboard%20Screenshot.png)](https://prod-ca-a.online.tableau.com/t/sophiatse51-925239984f/views/LaundromatDashboard/SalesDashboard)
---

## Business Problem

This project analyzes the operational efficiency and financial performance of a independent, single-location laundromat equipped with **10 washers, 10 dryers, and 2 vending machines** (vending machine products: laundry pods, dryer sheets, stain remover packs). 

Because historical data for this specific footprint was unavailable, I developed a realistic, synthetic relational database in Python to simulate a 3-year operational history. To ensure the data mirrored true retail conditions, the data pipeline incorporated:
1. **The Business Ramp-Up Curve:** Simulating the initial grand opening phase, modeling a gradual customer acquisition curve over the first couple months until the business reached steady-state maturity.
2. **True-to-Life Seasonality:** Encoding heavy weekend spikes (Saturday/Sunday peak utilization) and seasonal variations in laundry volume (e.g., higher dryer usage and bulkier loads in winter months).
3. **Strict Utility & Inventory COGS:** Mapping Cost of Goods Sold (water, electricity, gas, and wholesale inventory) with tight, normally distributed variances to ensure profit margins realistically scale with machine cycles.

The final Tableau dashboard uses this data to identify peak months, evaluate washer/dryer revenue contribution, and provide actionable recommendations for off-peak promotions and maintenance scheduling.

## Data Engineering 

To build this business simulation (10 washers, 10 dryers, 2 vending machines), I developed a custom data generation pipeline in Python. The script programmatically enforces relational integrity, operational constraints, and realistic business logic across four tables.

### Core Python Libraries Used

* **`pandas`**: Used as the primary data manipulation engine to construct DataFrames, handle date ranges, execute data type casting, and perform `.merge()` lookups to map dimension attributes to the fact table.
* **`numpy`**: Leveraged for its vectorized mathematical functions and random sampling capabilities (`numpy.random`). This was critical for generating random (but constrained) distributions for transaction frequencies, customer behavior, and cost variances.
* **`datetime` / `calendar`**: Utilized to manipulate timestamps, extract specific days of the week (to program weekend spikes), and isolate months (to calculate winter vs. summer utility variations).

### How the 4 Tables Were Developed

The pipeline operates to build three **Dimension (Lookup) tables** before compiling the central **Fact (Transaction) table**

Below is snippet of the core data compilation loop:

```python
# Business Logic Loop: Simulating Time Series Transaction Velocity
current_date = START_DATE
while current_date <= END_DATE:
    is_weekend = current_date.weekday() >= 5
    
    # Calculate non-linear growth curve multiplier (Ramp-up phase transition)
    time_delta_ratio = (current_date - START_DATE).days / TOTAL_DAYS
    growth_ramp_multiplier = 0.4 + (0.6 * np.sin(time_delta_ratio * (np.pi / 2)))
    
    # Enforce heavy weekend utilization spikes
    daily_base_traffic = np.random.randint(180, 240) if is_weekend else np.random.randint(90, 130)
    adjusted_daily_traffic = int(daily_base_traffic * growth_ramp_multiplier)
    
    # Distribute activity realistically across operational hours
    for _ in range(adjusted_daily_traffic):
        hour = int(np.random.choice(np.arange(0, 24), p=HOURLY_PROBABILITY_DISTRIBUTION))
        stream_choice = np.random.choice(['Machine', 'Vending'], p=[0.85, 0.15])
        
        # Calculations continue down to compute specific dynamic COGS & structural constraints...
---
