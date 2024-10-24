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

        return closest_contracts
    except ValueError:
        st.error("Please enter valid numeric values.")
        return []

# Function to calculate the new premium for the selected profit target
def calculate_profit_target(selected_contracts, entry_premium, target_profit):
    return (target_profit / (selected_contracts * 100)) + entry_premium

# Function to calculate stop premium for a given maximum loss
def calculate_stop_premium(num_options, initial_premium, max_loss):
    # Formula to calculate the stop premium
    stop_premium = initial_premium - (max_loss / (num_options * 100))
    return stop_premium

# Streamlit layout and input fields
st.title("Options Contracts Calculator")

# --- FIRST CALCULATION (Number of Contracts) ---
st.subheader("Calculate Number of Contracts to Buy")

# Input fields with increment/decrement functionality
delta = st.number_input("Delta at Entry", value=0.60, step=0.01, format="%.2f")
premium = st.number_input("Premium at Entry Price", value=9.00, step=0.10, format="%.2f")
stop_distance = st.number_input("Stop Distance on Underlying Stock", value=4.00, step=0.10, format="%.2f")
risk_amount = st.number_input("Risk Amount in Dollars", value=1000.0, step=100.0, format="%.2f")

# Trigger the main risk calculation and store the results in session state
if st.button("Calculate Number of Contracts to Buy"):
    closest_contracts = calculate_risks(delta, premium, stop_distance, risk_amount)
    st.session_state['closest_contracts'] = closest_contracts  # Store in session state

# Retrieve closest contracts from session state (to persist them)
closest_contracts = st.session_state.get('closest_contracts', None)

# If we have closest contracts calculated, display them
if closest_contracts:
    selected_contracts = st.session_state.get('selected_contracts', None)
    cols = st.columns(3)  # Create 3 columns for the results
    for idx, (contracts, diff, calculated_risk) in enumerate(closest_contracts):
        # Determine box color based on the risk amount
        box_color = "#d4edda" if calculated_risk == closest_contracts[0][2] else "#f6d6d6" if calculated_risk > risk_amount else "#f0f0f0"
        
        # Create a button to select each contract
        if cols[idx].button(f"Select {contracts} contracts"):
            st.session_state['selected_contracts'] = contracts
            st.session_state['entry_premium'] = premium
            st.session_state['target_profit'] = risk_amount

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

# --- NEW SECTION: Calculate Profit Target ---
selected_contracts = st.session_state.get('selected_contracts', None)
entry_premium = st.session_state.get('entry_premium', None)
target_profit = st.session_state.get('target_profit', None)

if selected_contracts:
    st.subheader(f"Calculate Profit Target (for ${target_profit:.2f} Profit)")
    new_premium = calculate_profit_target(selected_contracts, entry_premium, target_profit)
    
    # Proper Markdown formatting without extra ** symbols
    st.markdown(f"""
        To make a **${target_profit:.2f}** profit with **{selected_contracts} contracts**, 
        the option premium must rise to: **${new_premium:.2f}**
    """)



# Explanation for the first calculation
st.info("This tool calculates the number of option contracts you should buy based on your risk tolerance, stop distance on the underlying stock, and the premium of the option.")

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
