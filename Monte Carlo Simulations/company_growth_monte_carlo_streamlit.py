import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

# Set up interactive widgets
st.title("Monte Carlo Simulation: Company Growth to end of the Year")

weekly_growth_rate = st.slider("Expected Weekly Growth Rate (%)", min_value=0.0, max_value=.1, value=0.0, step=.005)
reduction_factor = st.slider("Reduction Factor - % reducing baseline ", .92, 1.0,.01)
# years = st.slider("Number of Years", 1, 50, 20)
simulations = st.slider("Number of Simulations", 100, 5000, 1000, step=100)

# weekly_growth_rate = 0.0115  # 1.15% growth per week from new accounts
reduction_start_week = 14
reduction_weeks = 13
# reduction_factor = 0.92  # 8% reduction means multiply by 0.92

# # Past weekly sales data for 26 weeks
past_weekly_sales = np.array([
    3000, 3200, 3100, 3050, 3150, 3300, 3400, 3350, 3200, 3250, 3100, 3150,
    3300, 3400, 3450, 3350, 3200, 3150, 3100, 3050, 3000, 2950, 2900, 2850, 3000, 3100
])



past_weekly_sales = past_weekly_sales/.75

future_weeks = 26  # Forecast 26 weeks ahead
# num_simulations = 10000

mean_weekly_sales = np.mean(past_weekly_sales)
std_weekly_sales = np.std(past_weekly_sales)

total_sales_simulated = []
simulated_sales_examples = []

for n,_ in enumerate(range(simulations)):
    simulated_sales = []
    for week in range(future_weeks):
        # Simulate base sales from normal distribution
        base_sales = np.random.normal(mean_weekly_sales, std_weekly_sales)
        base_sales = max(base_sales, 0)  # type:ignore
        
        # Apply weekly growth multiplier
        growth_multiplier = 1 + weekly_growth_rate * week
        
        # Apply reduction factor for weeks 14-26 (index 13 to 25 zero-based)
        if reduction_start_week - 1 <= week < reduction_start_week - 1 + reduction_weeks:
            reduction = reduction_factor
        else:
            reduction = 1.0
        
        # Final sales for the week
        week_sales = base_sales * growth_multiplier * reduction
        simulated_sales.append(week_sales)
        
    if n % 1000 == 0:
        simulated_sales_examples.append(simulated_sales)
    total_sales_simulated.append(np.sum(simulated_sales))

mean_sales_future = np.mean(total_sales_simulated)
median_sales_future = np.median(total_sales_simulated)
conf_interval_sales = np.percentile(total_sales_simulated, [5, 95])

st.markdown(f"### Estimated Total Sales Over {future_weeks} Weeks (with reduction weeks 14–26)")
st.write(f"**Mean sales:** ${mean_sales_future:,.2f}")
st.write(f"**Median sales:** ${median_sales_future:,.2f}")
st.write(f"**90% confidence interval:** ${conf_interval_sales[0]:,.2f} to ${conf_interval_sales[1]:,.2f}")


# Plotting
fig, ax = plt.subplots(figsize=(10, 6))

ax.hist(total_sales_simulated, bins=50, color='skyblue', edgecolor='black')
plt.title(f"Monte Carlo Simulation of Total Sales Over {future_weeks} Weeks\n(with growth and reduction weeks 14-26)")
plt.xlabel("Total Sales ($)")
plt.ylabel("Frequency")
st.pyplot(fig)