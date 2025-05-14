#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HDB Resale Price Prediction Chatbot

This application helps users estimate HDB resale prices based on
various attributes like flat type, location, and lease.
"""
import streamlit as st  # Importing Streamlit for the web interface
import logging  # Importing logging module for tracking application events
import os  # Importing os module for file operations
from datetime import datetime  # Importing datetime for timestamping logs

# Configure logging to save to a file
if not os.path.exists('logs'):  # Check if logs directory exists
    os.makedirs('logs')  # Create logs directory if it doesn't exist

log_filename = f"logs/hdb_chatbot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"  # Create unique log filename with timestamp
logging.basicConfig(
    filename=log_filename,  # Set log file path
    level=logging.INFO,  # Set logging level to INFO
    format='%(asctime)s - %(levelname)s - %(message)s',  # Define log format with timestamp, level and message
    datefmt='%Y-%m-%d %H:%M:%S'  # Define date format for logs
)

# Define the options for dropdowns with descriptive variable names
TOWNS = [  # Using uppercase for constants per PEP 8
    "ANG MO KIO", "BEDOK", "BISHAN", "BUKIT BATOK", "BUKIT MERAH", "BUKIT PANJANG",
    "BUKIT TIMAH", "CENTRAL AREA", "CHOA CHU KANG", "CLEMENTI", "GEYLANG", "HOUGANG",
    "JURONG EAST", "JURONG WEST", "KALLANG/WHAMPOA", "MARINE PARADE", "PASIR RIS",
    "PUNGGOL", "QUEENSTOWN", "SEMBAWANG", "SENGKANG", "SERANGOON", "TAMPINES",
    "TOA PAYOH", "WOODLANDS", "YISHUN"
]  # List of all HDB towns in Singapore

FLAT_TYPES = ["3 ROOM", "4 ROOM", "5 ROOM", "EXECUTIVE", "MULTI-GENERATION"]  # Different HDB flat types available
FLAT_MODELS = ["STANDARD", "IMPROVED", "NEW GENERATION", "DBSS", "PREMIUM APARTMENT", "MODEL A", "MAISONETTE"]  # Different HDB flat models
STOREY_RANGES = ["01 TO 03", "04 TO 06", "07 TO 09", "10 TO 12", "13 TO 15", "16 TO 18",
                "19 TO 21", "22 TO 24", "25 TO 27", "28 TO 30"]  # Storey ranges in HDB buildings

def validate_inputs(floor_area: int, lease: int) -> bool:
    """
    Validate user inputs for floor area and lease.
    
    Args:
        floor_area: Floor area in square meters
        lease: Remaining lease in years
        
    Returns:
        bool: True if inputs are valid, False otherwise
    """
    if floor_area < 40 or floor_area > 200:  # Check if floor area is within reasonable range
        st.error("Floor area should be between 40 and 200 square meters")  # Display error message for invalid floor area
        logging.error(f"Invalid floor area input: {floor_area}")  # Log error for invalid floor area
        return False  # Return False to indicate validation failure
    
    if lease < 0 or lease > 99:  # Check if remaining lease is within valid range
        st.error("Remaining lease should be between 0 and 99 years")  # Display error message for invalid lease
        logging.error(f"Invalid lease input: {lease}")  # Log error for invalid lease
        return False  # Return False to indicate validation failure
    
    return True  # Return True to indicate all inputs are valid

def calculate_price(town: str, flat_type: str, flat_model: str, 
                   storey_range: str, floor_area: int, lease: int) -> tuple:
    """
    Calculate estimated resale price based on input parameters.
    
    Args:
        town: HDB town location
        flat_type: Type of flat (e.g., 3 ROOM, 4 ROOM)
        flat_model: Model of flat (e.g., STANDARD, IMPROVED)
        storey_range: Floor level range
        floor_area: Floor area in square meters
        lease: Remaining lease in years
        
    Returns:
        tuple: (estimated_price, confidence_range_low, confidence_range_high)
    """
    logging.info(f"Calculating price for: {town}, {flat_type}, {flat_model}, {storey_range}, {floor_area}sqm, {lease}yrs")  # Log price calculation inputs
    
    # Simple price calculation model - this would be replaced with a real ML model in production
    base_price = 300000  # Base price in SGD
    
    # Adjust price based on town (simplified example)
    town_multiplier = 1.0  # Default multiplier
    if town in ["BUKIT TIMAH", "CENTRAL AREA"]:  # Premium locations
        town_multiplier = 1.3  # Higher multiplier for premium locations
    elif town in ["ANG MO KIO", "BISHAN", "QUEENSTOWN"]:  # Mature estates
        town_multiplier = 1.2  # Higher multiplier for mature estates
    
    # Adjust price based on flat type
    type_addition = {
        "3 ROOM": 0,
        "4 ROOM": 100000,
        "5 ROOM": 200000,
        "EXECUTIVE": 250000,
        "MULTI-GENERATION": 300000
    }.get(flat_type, 0)  # Price addition based on flat type, defaulting to 0
    
    # Factor in storey range (higher floors typically cost more)
    storey_factor = STOREY_RANGES.index(storey_range) * 10000 if storey_range in STOREY_RANGES else 0  # Higher floors get higher price
    
    # Calculate the final estimated price
    estimated_price = (base_price + type_addition + storey_factor + 
                      (floor_area * 3000) + (lease * 1000)) * town_multiplier  # Combined price calculation
    
    # Generate confidence range (±10%)
    confidence_low = round(estimated_price * 0.9)  # Lower bound of confidence range
    confidence_high = round(estimated_price * 1.1)  # Upper bound of confidence range
    
    logging.info(f"Price estimate: ${estimated_price:,.2f} (Range: ${confidence_low:,.2f} - ${confidence_high:,.2f})")  # Log price calculation results
    
    return (round(estimated_price), confidence_low, confidence_high)  # Return the estimated price and confidence range

def main() -> None:
    """
    Main function to run the Streamlit application.
    """
    logging.info("Application started")  # Log application start
    
    st.title("🏠 HDB Resale Price Predictor Chatbot")  # Set application title
    st.write("Enter details about the flat to get an estimated resale price.")  # Add descriptive text for users
    
    # Collect user inputs through Streamlit widgets
    town = st.selectbox("Town", TOWNS)  # Dropdown for selecting HDB town
    flat_type = st.selectbox("Flat Type", FLAT_TYPES)  # Dropdown for selecting flat type
    flat_model = st.selectbox("Flat Model", FLAT_MODELS)  # Dropdown for selecting flat model
    storey_range = st.selectbox("Storey Range", STOREY_RANGES)  # Dropdown for selecting storey range
    
    # Sliders for numerical inputs with appropriate ranges
    floor_area = st.slider("Floor Area (sqm)", min_value=40, max_value=150, value=90)  # Slider for floor area input
    lease = st.slider("Remaining Lease (years)", min_value=0, max_value=99, value=60)  # Slider for remaining lease input
    
    # Optional address input
    address = st.text_input("Block & Street (optional)")  # Text input for address
    
    # Add a button to trigger the prediction
    if st.button("Calculate Resale Price"):  # Button to trigger price calculation
        if validate_inputs(floor_area, lease):  # Validate inputs before calculation
            try:
                estimated_price, confidence_low, confidence_high = calculate_price(
                    town, flat_type, flat_model, storey_range, floor_area, lease
                )  # Calculate price using the function
                
                # Display the results
                st.subheader("💰 Estimated Resale Price:")  # Heading for price results
                st.write(f"${estimated_price:,.2f}")  # Display the estimated price
                st.write(f"Confidence Range: ${confidence_low:,.2f} - ${confidence_high:,.2f}")  # Display confidence range
                
                # Log the successful estimation
                logging.info(f"Successful estimation for {address if address else town}")  # Log successful estimation
                
            except Exception as e:  # Catch any unexpected errors
                st.error("An error occurred during price calculation. Please try again.")  # Display general error message
                logging.error(f"Error in price calculation: {str(e)}")  # Log the specific error
    
    st.markdown("---")  # Add a separator line
    st.caption("Note: This is a simplified model for educational purposes only.")  # Add disclaimer
    
    logging.info("Page rendered successfully")  # Log successful page rendering

if __name__ == "__main__":
    main()  # Run the main function when the script is executed directly
