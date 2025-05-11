import streamlit as st

# Define the options for dropdowns
towns = [
    "ANG MO KIO", "BEDOK", "BISHAN", "BUKIT BATOK", "BUKIT MERAH", "BUKIT PANJANG",
    "BUKIT TIMAH", "CENTRAL AREA", "CHOA CHU KANG", "CLEMENTI", "GEYLANG", "HOUGANG",
    "JURONG EAST", "JURONG WEST", "KALLANG/WHAMPOA", "MARINE PARADE", "PASIR RIS",
    "PUNGGOL", "QUEENSTOWN", "SEMBAWANG", "SENGKANG", "SERANGOON", "TAMPINES",
    "TOA PAYOH", "WOODLANDS", "YISHUN"
]
flat_types = ["3 ROOM", "4 ROOM", "5 ROOM", "EXECUTIVE", "MULTI-GENERATION"]
flat_models = ["STANDARD", "IMPROVED", "NEW GENERATION", "DBSS", "PREMIUM APARTMENT", "MODEL A", "MAISONETTE"]
storey_ranges = ["01 TO 03", "04 TO 06", "07 TO 09", "10 TO 12", "13 TO 15", "16 TO 18",
                 "19 TO 21", "22 TO 24", "25 TO 27", "28 TO 30"]

# Streamlit app
st.title("🏠 HDB Price Predictor Chatbot")

# Dropdowns for town, flat type, flat model, and storey range

flat_type = st.selectbox("Flat Type", flat_types)
flat_model = st.selectbox("Flat Model", flat_models)
storey_range = st.selectbox("Storey Range", storey_ranges)

# Sliders for floor area and lease
floor_area = st.slider("Floor Area (sqm)", min_value=40, max_value=150, value=90)
lease = st.slider("Remaining Lease (years)", min_value=0, max_value=99, value=60)

# Input for address (optional)
address = st.text_input("Block & Street (optional)")

# prediction logic
estimated_price = 300000 + floor_area * 300 + lease * 100
confidence_range = (round(estimated_price * 0.9), round(estimated_price * 1.1))

# Display the estimated price and confidence range
st.subheader("💰 Estimated Resale Price:")
st.write(f"${estimated_price:,.2f}")
st.write(f"Confidence Range: ${confidence_range[0]:,.2f} - ${confidence_range[1]:,.2f}")
