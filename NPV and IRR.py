import streamlit as st
import numpy as np
import numpy_financial as npf
import matplotlib.pyplot as plt

# Set wide page layout for more screen space.
st.set_page_config(layout="wide")
st.title("NPV and IRR Visualizer")

# Input: let students change the cash flows.
cash_flow_input = st.text_area(
    "Enter cash flows for each period (comma separated):",
    "-100, 30, 40, 50, 60"
)

# Try converting the input to a list of floats.
try:
    cash_flows = [float(x.strip()) for x in cash_flow_input.split(",")]
except Exception as e:
    st.error("Invalid input. Please enter valid numbers separated by commas.")
    st.stop()

# Slider: select a range of discount rates (in percentage) from 0% to 50%.
discount_rate_range = st.slider(
    "Discount Rate Range (%)",
    min_value=0,
    max_value=50,
    value=(5, 30)
)
min_rate, max_rate = discount_rate_range
min_rate_dec = min_rate / 100.0
max_rate_dec = max_rate / 100.0

# Generate discount rates over the selected range.
num_points = 100
rates = np.linspace(min_rate_dec, max_rate_dec, num_points)

# Function to compute the NPV for a given rate.
def compute_npv(cash_flows, r):
    return sum(cf / ((1 + r) ** t) for t, cf in enumerate(cash_flows))

# Compute NPV for each rate.
npv_values = [compute_npv(cash_flows, r) for r in rates]

# Compute the IRR using numpy_financial.
try:
    irr = npf.irr(cash_flows)
    irr_percent = irr * 100
except Exception as e:
    irr = None
    st.error("Error computing IRR.")

# Create a Matplotlib figure.
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(rates * 100, npv_values, label="NPV Curve", lw=2)
ax.axhline(0, color='black', lw=0.8)

# Mark and label the IRR if it is computed and within the selected range.
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

# Display the chart.
st.pyplot(fig)

# Display the calculated IRR value.
if irr is not None:
    st.write(f"**Calculated IRR:** {irr_percent:.2f}%")
