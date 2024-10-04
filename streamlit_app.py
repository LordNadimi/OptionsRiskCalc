import streamlit as st

# Function to calculate risk for various contract numbers
def calculate_risks(delta, premium, stop_distance, risk_amount):
    try:
        # Convert inputs to float values
        delta = float(delta)
        premium = float(premium)
        stop_distance = float(stop_distance)
        risk_amount = float(risk_amount)

        # List to store results of different contract numbers and their corresponding risks
        contract_risks = []

        # Check risk for predefined contract numbers (1 to 100)
        for contracts in range(1, 101):
            # Calculate the risk using the specified formula from Excel
            risk = (contracts * delta) * (stop_distance * 100) + premium * contracts
            contract_risks.append((contracts, abs(risk - risk_amount), risk))

        # Sort by the closest risk to the chosen risk amount
        contract_risks.sort(key=lambda x: x[1])

        # Get the three contract options closest to the desired risk amount
        closest_contracts = contract_risks[:3]

        # Define colors for boxes with better contrast for both light and dark modes
        colors = {
            "closest": "#e0f4e0",  # Soft green for the closest match
            "neutral": "#f0f0f0",  # Light gray for neutral
            "over_limit": "#f6d6d6",  # Soft red for over the limit
        }

        # Display the results horizontally using Streamlit columns
        cols = st.columns(3)  # Create 3 columns for the results
        for idx, (contracts, diff, calculated_risk) in enumerate(closest_contracts):
            # Determine box color based on the risk amount
            if calculated_risk == closest_contracts[0][2]:
                box_color = colors["closest"]
            elif calculated_risk > risk_amount:
                box_color = colors["over_limit"]
            else:
                box_color = colors["neutral"]

            # Render each box in its respective column with improved styles
            cols[idx].markdown(
                f"""
                <div style="background-color: {box_color}; color: black; padding: 10px; border-radius: 5px; margin-bottom: 10px; 
                border: 1px solid #ccc; box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);">
                    <strong>Contracts: {contracts}</strong><br>
                    Calculated Risk: ${calculated_risk:.2f}
                </div>
                """,
                unsafe_allow_html=True,
            )

        return closest_contracts
    except ValueError:
        st.error("Please enter valid numeric values.")
        return []

# Streamlit layout and input fields
st.title("Options Contracts Calculator")

# Input fields with increment/decrement functionality
delta = st.number_input("Delta at Entry", value=0.60, step=0.01, format="%.2f")
premium = st.number_input("Premium at Entry Price", value=9.00, step=0.10, format="%.2f")
stop_distance = st.number_input("Stop Distance on Underlying Stock", value=4.00, step=0.10, format="%.2f")
risk_amount = st.number_input("Risk Amount in Dollars", value=1000.0, step=100.0, format="%.2f")

# Button to trigger the calculation
if st.button("Calculate Number of Contracts to Buy"):
    closest_contracts = calculate_risks(delta, premium, stop_distance, risk_amount)

# Provide information about the tool
st.info("This tool calculates the number of option contracts you should buy based on your risk tolerance, "
        "stop distance on the underlying stock, and the premium of the option.")
