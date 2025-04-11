import streamlit as st
import numpy as np
import numpy_financial as npf
import matplotlib.pyplot as plt

# Set page layout to wide for better space
st.set_page_config(layout="wide")

st.title("NPV and IRR Visualizer")

# Input area for cash flows (comma-separated)
cash_flow_input = st.text_area(
    "Enter cash flows (comma separated):",
    "-100, 30, 40, 50, 60"
)

# Convert the input text to a list of floats.
try:
    cash_flows = [float(x.strip()) for x in cash_flow_input.split(",")]
except Exception as e:
    st.error("Invalid input. Please enter valid numbers separated by commas.")
    st.stop()

# Slider to set the discount rate range (in percentages)
discount_rate_range = st.slider(
    "Discount Rate Range (%)",
    min_value=-20,
    max_value=50,
    value=(-10, 30)
)
min_rate, max_rate = discount_rate_range
min_rate_dec = min_rate / 100.0
max_rate_dec = max_rate / 100.0

# Create a vector of discount rates across the chosen range.
num_points = 100
rates = np.linspace(min_rate_dec, max_rate_dec, num_points)

# Function to calculate NPV for a given set of cash flows and discount rate.
def compute_npv(cash_flows, r):
    return sum(cf / ((1 + r) ** t) for t, cf in enumerate(cash_flows))

# Calculate NPV values for each discount rate in our range.
npv_values = [compute_npv(cash_flows, r) for r in rates]

# Compute the IRR using numpy_financial.
try:
    irr = npf.irr(cash_flows)
    irr_percent = irr * 100
except Exception as e:
    irr = None
    st.error("Error computing IRR.")

# Create the NPV vs Discount Rate plot.
fig, ax = plt.subplots(figsize=(10, 6))
# Plot NPV (x-axis: discount rate in percentage; y-axis: NPV)
ax.plot(rates * 100, npv_values, label="NPV Curve", lw=2)
ax.axhline(0, color='black', lw=0.8)  # Horizontal line at NPV=0

# If the IRR is computed and it lies within our selected range, mark it.
if irr is not None and min_rate <= (irr * 100) <= max_rate:
    npv_at_irr = compute_npv(cash_flows, irr)
    ax.plot(irr * 100, npv_at_irr, 'ro', label=f"IRR = {irr_percent:.2f}%")
    ax.annotate(
        f"IRR: {irr_percent:.2f}%", 
        (irr * 100, npv_at_irr),
        textcoords="offset points", 
        xytext=(0,10), 
        ha='center',
        color='red'
    )

ax.set_xlabel("Discount Rate (%)", fontsize=16)
ax.set_ylabel("NPV (€)", fontsize=16)
ax.set_title("NPV vs. Discount Rate", fontsize=18)
ax.legend(fontsize=14)
ax.tick_params(labelsize=14)
fig.tight_layout()

# Display the plot.
st.pyplot(fig)

# Display the IRR value (if computed).
if irr is not None:
    st.write(f"**Calculated IRR:** {irr_percent:.2f}%")
