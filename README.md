# HDB Resale Price Predictor Chatbot

A Streamlit web application that helps predict HDB (Housing & Development Board) resale prices in Singapore based on various parameters such as location, flat type, and remaining lease.

## Features

- Interactive UI with dropdown menus and sliders for input
- Price prediction based on multiple parameters
- Confidence range display
- Logging system for tracking usage and errors

## Installation

```bash
conda create --prefix=venv python=3.11 -y
conda activate ./venv
python -m pip install -r requirements.txt
```

## Usage

To run the application:

```bash
streamlit run HDB_Chatbot.py
```

## Required Packages

Create a `requirements.txt` file with the following dependencies:
```text
streamlit>=1.22.0
pandas>=1.5.3
numpy>=1.24.3
```


## Application Structure

- `HDB_Chatbot.py`: Main application with Streamlit interface
- `logs/`: Directory for log files (auto-created on first run)

## Data Model

The current implementation uses a simplified calculation model. In a production environment, this would be replaced with a trained machine learning model based on actual HDB resale transaction data.

## Development Notes

- Input validation ensures that floor area and lease values are within reasonable ranges
- Comprehensive logging captures user interactions and any errors
- Exception handling provides graceful error recovery

## License

MIT