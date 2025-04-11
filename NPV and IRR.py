import streamlit as st
import numpy as np
import numpy_financial as npf
import matplotlib.pyplot as plt

# Use a wide page layout for more horizontal space
st.set_page_config(layout="wide")
st.title("NPV and IRR Visualizer")

# Create two columns: left for controls; right for diagram
col_left, col_right = st.columns([1, 2])

with col_left:
    st.header("Input Controls")
    
    # Let students enter cash flows as comma-separated values.
    cash_flow_input = st.text_area(
        "Enter cash flows for each period (comma separated):",
        "-100, 30, 40, 50, 60"
    )
    
    # Convert the cash flow input into a list of floats.
    try:
        cash_flows = [float(x.strip()) for x in cash_flow_input.split(",")]
    except Exception:
        st.error("Invalid input. Please enter valid numbers separated by commas.")
        st.stop()
        
    # Slider to select a discount rate range (in percentages), avoiding negative rates.
    discount_rate_range = st.slider(
        "Discount Rate Range (%)",
        min_value=0,
        max_value=50,
        value=(5, 30)
    )
    min_rate, max_rate = discount_rate_range
    min_rate_dec = min_rate / 100.0
    max_rate_dec = max_rate / 100.0

    st.markdown("---")
    st.write("The app computes the NPV for various discount rates over the chosen range and calculates the IRR.")


# Define a function to compute NPV.
def compute_npv(cash_flows, r):
    return sum(cf / ((1 + r) ** t) for t, cf in enumerate(cash_flows))


# Generate a set of discount rates to evaluate
num_points = 100
rates = np.linspace(min_rate_dec, max_rate_dec, num_points)
npv_values = [compute_npv(cash_flows, r) for r in rates]

# Calculate the IRR using numpy_financial
try:
    irr = npf.irr(cash_flows)
    irr_percent = irr * 100
except Exception:
    irr = None

with col_right:
    st.header("NPV vs. Discount Rate")
    
    # Create a Matplotlib figure.
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Plot the NPV curve.
    ax.plot(rates * 100, npv_values, lw=2, label="NPV Curve")
    ax.axhline(0, color='black', lw=0.8)
    
    # If IRR is computed and lies within the selected discount rate range, mark it.
    if irr is not None and (min_rate <= (irr * 100) <= max_rate):
        npv_at_irr = compute_npv(cash_flows, irr)
        ax.plot(irr * 100, npv_at_irr, 'ro', label=f"IRR = {irr_percent:.2f}%")
        ax.annotate(
            f"IRR: {irr_percent:.2f}%",
            (irr * 100, npv_at_irr),
            textcoords="offset points",
            xytext=(0, 10),
            ha='center',
            color='red'
        )
    
    ax.set_xlabel("Discount Rate (%)", fontsize=16)
    ax.set_ylabel("NPV (€)", fontsize=16)
    ax.set_title("NPV vs. Discount Rate", fontsize=18)
    ax.legend(fontsize=14)
    ax.tick_params(labelsize=14)
    fig.tight_layout()
    
    st.pyplot(fig, use_container_width=True)
    
    # Show IRR below the plot if available.
    if irr is not None:
        st.write(f"**Calculated IRR:** {irr_percent:.2f}%")
