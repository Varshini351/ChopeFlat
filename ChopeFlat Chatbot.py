import streamlit as st
import pandas as pd

st.set_page_config(page_title="Chopeflat Chatbot", layout="wide")

# Load dataset
@st.cache_data
def load_data():
    return pd.read_csv("Dataset.csv")  # Replace with your actual dataset

df = load_data()

# UI
st.title("💬 Chopeflat Chatbot")
st.markdown("Ask questions about HDB resale prices in Singapore from the dataset.")

# Optional: show dataset
with st.expander("📊 Show dataset"):
    st.dataframe(df)

# Chat input
question = st.text_input("Ask me anything about HDB resale prices:")
if question:
    question_lower = question.lower()

    if "town" in question_lower:
        towns = df["town"].unique()
        st.markdown("📍 The dataset includes resale flats in these towns:\n- " + "\n- ".join(towns))

    elif "flat type" in question_lower or "types of flat" in question_lower:
        types = df["flat_type"].unique()
        st.markdown("🏢 Available flat types in the dataset:\n- " + "\n- ".join(types))

    elif "average price" in question_lower:
        avg_price = df["resale_price"].mean()
        st.markdown(f"💰 The average resale price is **${avg_price:,.0f}**.")

    elif "highest price" in question_lower or "most expensive" in question_lower:
        max_price = df["resale_price"].max()
        st.markdown(f"🏆 The highest resale price is **${max_price:,.0f}**.")

    elif "lowest price" in question_lower or "cheapest" in question_lower:
        min_price = df["resale_price"].min()
        st.markdown(f"📉 The lowest resale price is **${min_price:,.0f}**.")

    elif "average price in" in question_lower:
        for town in df["town"].unique():
            if town.lower() in question_lower:
                avg = df[df["town"].str.lower() == town.lower()]["resale_price"].mean()
                st.markdown(f"📍 The average resale price in **{town}** is **${avg:,.0f}**.")
                break
        else:
            st.warning("❓ I couldn't find that town in the dataset.")

    elif "how many flats" in question_lower:
        count = df.shape[0]
        st.markdown(f"🏘️ The dataset contains **{count:,}** resale flat records.")

    elif "most common flat type" in question_lower:
        common = df["flat_type"].value_counts().idxmax()
        st.markdown(f"🔢 The most common flat type in the dataset is **{common}**.")

    elif "resale flats in" in question_lower:
        for town in df["town"].unique():
            if town.lower() in question_lower:
                subset = df[df["town"].str.lower() == town.lower()]
                st.markdown(f"📄 Showing sample resale flats in **{town}**:")
                st.dataframe(subset.head(10))
                break
        else:
            st.warning("❓ I couldn't find that town in the dataset.")

    else:
        st.warning("🤖 I didn’t understand that. Try asking about towns, prices, or flat types.")


