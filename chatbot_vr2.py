import streamlit as st
import pydeck as pdk
from geopy.geocoders import Nominatim
import pandas as pd

# Define page configuration and title
st.set_page_config(page_title="HDB Chatbot Version 2", layout="wide")
st.title("HDB Chatbot Version 2 - Interactive Map")

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

# Geocoder initialization
geolocator = Nominatim(user_agent="hdb_app")

# Get coordinates for each town
locations = []
for town in towns:
    location = geolocator.geocode(f"{town}, Singapore")
    if location:
        locations.append({
            'town': town,
            'lat': location.latitude,
            'lon': location.longitude
        })

# Convert to DataFrame
location_data = pd.DataFrame(locations)

# Display the map
st.subheader("Select a Town to View Details")
layer = pdk.Layer(
    "ScatterplotLayer",
    data=location_data,
    get_position='[lon, lat]',
    get_color='[200, 30, 0, 160]',
    get_radius=100
)

view_state = pdk.ViewState(
    latitude=1.3521,
    longitude=103.8198,
    zoom=11,
    pitch=45
)

r = pdk.Deck(layers=[layer], initial_view_state=view_state, tooltip={"text": "{town}"})
st.pydeck_chart(r)

# Sidebar for details
st.sidebar.header("HDB Flat Information")
selected_town = st.sidebar.selectbox("Select Town", towns)
flat_type = st.sidebar.selectbox("Flat Type", flat_types)
flat_model = st.sidebar.selectbox("Flat Model", flat_models)
storey_range = st.sidebar.selectbox("Storey Range", storey_ranges)
floor_area = st.sidebar.slider("Floor Area (sqm)", min_value=40, max_value=150, value=90)
lease = st.sidebar.slider("Remaining Lease (years)", min_value=0, max_value=99, value=60)

# Estimate price
if st.sidebar.button("Estimate Resale Price"):
    estimated_price = 300000 + floor_area * 300 + lease * 100
    confidence_range = (round(estimated_price * 0.9), round(estimated_price * 1.1))

    st.sidebar.subheader("Estimated Resale Price:")
    st.sidebar.write(f"${estimated_price:,.2f}")
    st.sidebar.write(f"Confidence Range: ${confidence_range[0]:,.2f} - ${confidence_range[1]:,.2f}")


