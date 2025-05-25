import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import branca.colormap as cm
import altair as alt
 
# ---- PAGE CONFIG ----
st.set_page_config(page_title="ChopeFlat – Smart HDB Resale Finder", layout="wide")
st.title("🏠 ChopeFlat – Your Smart HDB Resale Companion")
 
# ---- LOAD DATA ----
df = pd.read_csv("Dataset.csv")
df['month'] = pd.to_datetime(df['month'])
 
# ---- TOWN COORDINATES ----
coordinates = {
    "ANG MO KIO": (1.3691, 103.8499), "BEDOK": (1.3244, 103.9301), "BISHAN": (1.3500, 103.8499),
    "BUKIT BATOK": (1.3504, 103.7465), "BUKIT MERAH": (1.2804, 103.8238), "BUKIT PANJANG": (1.3812, 103.7636),
    "BUKIT TIMAH": (1.3403, 103.7760), "CENTRAL AREA": (1.2838, 103.8600), "CHOA CHU KANG": (1.3852, 103.7440),
    "CLEMENTI": (1.3152, 103.7654), "GEYLANG": (1.3208, 103.8860), "HOUGANG": (1.3710, 103.8877),
    "JURONG EAST": (1.3323, 103.7437), "JURONG WEST": (1.3454, 103.7053), "KALLANG/WHAMPOA": (1.3133, 103.8639),
    "MARINE PARADE": (1.3001, 103.9058), "PASIR RIS": (1.3723, 103.9493), "PUNGGOL": (1.4039, 103.9114),
    "QUEENSTOWN": (1.2944, 103.8055), "SEMBAWANG": (1.4500, 103.8200), "SENGKANG": (1.3911, 103.8973),
    "SERANGOON": (1.3500, 103.8700), "TAMPINES": (1.3536, 103.9456), "TOA PAYOH": (1.3344, 103.8467),
    "WOODLANDS": (1.4380, 103.7860), "YISHUN": (1.4295, 103.8356)
}
 
# ---- SIDEBAR FILTERS ----
st.sidebar.header("🔍 Filter Your Preferences")
flat_type = st.sidebar.selectbox("🏢 Flat Type", df['flat_type'].unique())
flat_model = st.sidebar.selectbox("🏗 Flat Model", df['flat_model'].unique())
storey = st.sidebar.selectbox("📶 Storey Range", df['storey_range'].unique())
street = st.sidebar.selectbox("🛣 Street Name", df['street_name'].unique())
floor_range = st.sidebar.slider("📏 Floor Area (sqm)", 
                                 int(df['floor_area_sqm'].min()), 
                                 int(df['floor_area_sqm'].max()), 
                                 (60, 120))
 
selected_town = st.sidebar.selectbox("🧭 Zoom to Town (Map)", ["All"] + list(coordinates.keys()))
 
# ---- FILTER DATA ----
filtered_df = df[
    (df['flat_type'] == flat_type) &
    (df['flat_model'] == flat_model) &
    (df['storey_range'] == storey) &
    (df['street_name'] == street) &
    (df['floor_area_sqm'] >= floor_range[0]) &
    (df['floor_area_sqm'] <= floor_range[1])
]
 
# ---- SAVED FLATS STORAGE ----
if 'saved_flats' not in st.session_state:
    st.session_state['saved_flats'] = []
 
# ---- METRICS & SAVE BUTTON ----
if not filtered_df.empty:
    mean_price = filtered_df['resale_price'].mean()
    st.metric(label="💰 Average Resale Price", value=f"${mean_price:,.0f}")
    st.dataframe(filtered_df[['block', 'street_name', 'floor_area_sqm', 'resale_price']])
 
    if st.button("❤ Save This Flat"):
        st.session_state['saved_flats'].append(filtered_df.iloc[0].to_dict())
        st.success("Flat saved to your list!")
else:
    st.warning("⚠ No matching flats found. Please adjust your filters.")
 
# ---- TREND CHART ----
st.subheader("📈 Resale Price Trend by Town")
trend_df = df[df['town'] == selected_town] if selected_town != "All" else df
trend_chart = trend_df.groupby('month')['resale_price'].mean().reset_index()
chart = alt.Chart(trend_chart).mark_line(point=True).encode(
    x=alt.X('month:T', title='Month'),
    y=alt.Y(
        'resale_price:Q',
        title='Average Resale Price',
        axis=alt.Axis(format=',.0f')  # Format y-axis labels with no decimals
    ),
    tooltip=[
        alt.Tooltip('month:T', title='Month'),
        alt.Tooltip('resale_price:Q', title='Avg Price', format=',.0f')  # Format tooltip
    ]
).properties(
    width=900,
    height=300,
    title=f"Average Monthly Resale Price in {selected_town if selected_town != 'All' else 'All Towns'}"
)

st.altair_chart(chart, use_container_width=True)


 
# ---- MAP ----
# ---- MAP ----
town_prices = []
towns_to_plot = [selected_town] if selected_town != "All" else coordinates.keys()

# Step 1: Build town price summary
for town in towns_to_plot:
    if town in coordinates:
        lat, lon = coordinates[town]
        town_df = df[df['town'] == town]
        if not town_df.empty:
            avg_price = town_df['resale_price'].mean()
            count = town_df.shape[0]
            max_price = town_df['resale_price'].max()
            town_prices.append({
                'town': town,
                'lat': lat,
                'lon': lon,
                'avg_price': avg_price,
                'count': count,
                'max_price': max_price
            })

# Step 2: Bin average prices into 5 levels

prices = [t['avg_price'] for t in town_prices]

# If all prices are identical, assign the same bin index
if len(set(prices)) == 1:
    for town in town_prices:
        town['price_bin'] = 2  # Use the "middle" color
else:
    price_bins = pd.qcut(prices, 5, labels=False, duplicates='drop')  # Drop duplicate edges safely
    for i, town in enumerate(town_prices):
        town['price_bin'] = price_bins[i]

# Step 3: Map bin to folium icon colors
color_map = {
    0: "lightblue",
    1: "blue",
    2: "cadetblue",
    3: "darkblue",
    4: "purple"
}

# Step 4: Create map
map_location = coordinates[selected_town] if selected_town != "All" else [1.3521, 103.8198]
zoom_level = 13 if selected_town != "All" else 11
m = folium.Map(location=map_location, zoom_start=zoom_level, tiles="cartodbpositron")

# Step 5: Add color-coded icon markers with hover tooltips
for town in town_prices:
    price = town['avg_price']
    lat, lon = town['lat'], town['lon']
    count = town['count']
    max_price = town['max_price']
    bin_index = town['price_bin']
    icon_color = color_map.get(bin_index, "blue")

    tooltip_html = f"""
<b>🏘 {town['town']}</b><br>
💵 Avg Price: ${price:,.0f}<br>
🔢 Units Sold: {count}<br>
💰 Highest Price: ${max_price:,.0f}
"""

    folium.Marker(
        location=[lat, lon],
        tooltip=tooltip_html,
        icon=folium.Icon(color=icon_color, icon="home")
    ).add_to(m)

# Step 6: Show map in Streamlit
st.subheader("🗺 Explore Average Prices on the Map")
legend_html = """
<div style="
    position: fixed; 
    bottom: 50px; left: 50px; width: 180px; height: 150px; 
    background-color: white; z-index:9999; font-size:14px;
    border:2px solid grey; padding: 10px; border-radius: 8px;">
    <b>Legend – Avg Resale Price</b><br>
    <i class="fa fa-map-marker" style="color:lightblue"></i> Lowest 20%<br>
    <i class="fa fa-map-marker" style="color:blue"></i> Low-Mid<br>
    <i class="fa fa-map-marker" style="color:cadetblue"></i> Mid<br>
    <i class="fa fa-map-marker" style="color:darkblue"></i> Mid-High<br>
    <i class="fa fa-map-marker" style="color:purple"></i> Highest 20%
</div>
"""
m.get_root().html.add_child(folium.Element(legend_html))
st_folium(m, width=1000, height=600)

 
if st.session_state['saved_flats']:
    st.subheader("❤ Saved Flats")
    st.write(pd.DataFrame(st.session_state['saved_flats']))
