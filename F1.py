import pandas as pd
# Define a new sample flat to predict its resale price
new_flat = pd.DataFrame({
    'floor_area_sqm': [90],
    'flat_type': ['4 ROOM'],
    'town': ['ANG MO KIO']
})

# Predict the resale price using the trained pipeline model
try:
    prediction = model.predict(new_flat)
    print(f"Estimated resale price: ${prediction[0]:,.2f}")
except Exception as e:
    print("Prediction failed:", e)