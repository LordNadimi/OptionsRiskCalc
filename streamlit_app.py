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

        # Display the results horizontally using Streamlit columns
        cols = st.columns(3)  # Create 3 columns for the results
        selected_contracts = None  # To store user choice
        for idx, (contracts, diff, calculated_risk) in enumerate(closest_contracts):
            # Determine box color based on the risk amount
            if calculated_risk == closest_contracts[0][2]:
                box_color = "#d4edda"
            elif calculated_risk > risk_amount:
                box_color = "#f6d6d6"
            else:
                box_color = "#f0f0f0"

            # Render each box in its respective column with improved styles and clickable buttons
            if cols[idx].button(f"Select {contracts} contracts"):
                selected_contracts = contracts

            # Display the contracts and calculated risk in the columns
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

        return selected_contracts, premium, risk_amount
    except ValueError:
        st.error("Please enter valid numeric values.")
        return None, None, None

# Function to calculate the stop premium when $1000 loss is hit
def calculate_stop_premium(num_options, initial_premium, max_loss):
    total_cost = num_options * initial_premium * 100
    remaining_value = total_cost - max_loss
    stop_premium = remaining_value / (num_options * 100)
    return stop_premium

# Function to calculate the new premium for the selected profit target
def calculate_profit_target(selected_contracts, entry_premium, target_profit):
    return (target_profit / (selected_contracts * 100)) + entry_premium

# Streamlit layout and input fields
st.title("Options Contracts Calculator")

# --- FIRST CALCULATION (Number of Contracts) ---
st.subheader("Calculate Number of Contracts to Buy")
# Input fields with increment/decrement functionality
delta = st.number_input("Delta at Entry", value=0.60, step=0.01, format="%.2f")
premium = st.number_input("Premium at Entry Price", value=9.00, step=0.10, format="%.2f")
stop_distance = st.number_input("Stop Distance on Underlying Stock", value=4.00, step=0.10, format="%.2f")
risk_amount = st.number_input("Risk Amount in Dollars", value=1000.0, step=100.0, format="%.2f")

# Button to trigger the main risk calculation
selected_contracts, entry_premium, target_profit = calculate_risks(delta, premium, stop_distance, risk_amount)

# Explanation for the first calculation
st.info("This tool calculates the number of option contracts you should buy based on your risk tolerance, stop distance on the underlying stock, and the premium of the option.")

# --- NEW SECTION: Calculate Profit Target ---
if selected_contracts:
    st.subheader(f"Calculate Profit Target (for ${target_profit:.2f} Profit)")
    new_premium = calculate_profit_target(selected_contracts, entry_premium, target_profit)
    st.write(f"To make a ${target_profit:.2f} profit with {selected_contracts} contracts, the option premium must rise to: ${new_premium:.2f}")

# Horizontal line to visually separate the two sections
st.markdown("<hr style='border:1px solid gray;'>", unsafe_allow_html=True)

# --- SECOND CALCULATION (Stop Premium) ---
st.subheader("Calculate Stop Premium for a Given Maximum Loss")
# New inputs for stop premium calculation
num_options = st.number_input("Number of Options", value=5, step=1)
initial_premium = st.number_input("Initial Option Premium", value=3.00, step=0.10, format="%.2f")
max_loss = st.number_input("Maximum Loss in Dollars", value=1000.0, step=100.0, format="%.2f")

# Button to trigger the stop premium calculation
if st.button("Calculate Stop Premium"):
    stop_premium = calculate_stop_premium(num_options, initial_premium, max_loss)
    st.write(f"The stop premium to hit a loss of ${max_loss:.2f} is: ${stop_premium:.2f}")

# Explanation for the second calculation
st.info("This section calculates the option premium at the stop point that results in a specified maximum loss, based on the number of options and initial premium.")
