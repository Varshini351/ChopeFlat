import streamlit as st
import pandas as pd

st.set_page_config(page_title="Chopeflat Chatbot", layout="wide")

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("Dataset.csv")  # Update with your actual dataset path
    if "year" not in df.columns and "month" in df.columns:
        df["year"] = pd.to_datetime(df["month"]).dt.year
    return df

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
    towns = df["town"].unique()
    flat_types = df["flat_type"].unique()

    if "town" in question_lower:
        st.markdown("📍 The dataset includes resale flats in these towns:\n- " + "\n- ".join(towns))

    elif "flat type" in question_lower or "types of flat" in question_lower:
        st.markdown("🏢 Available flat types in the dataset:\n- " + "\n- ".join(flat_types))

    elif "average price" in question_lower and "in" not in question_lower:
        avg_price = df["resale_price"].mean()
        st.markdown(f"💰 The average resale price is **${avg_price:,.0f}**.")

    elif "highest price" in question_lower or "most expensive" in question_lower:
        max_price = df["resale_price"].max()
        st.markdown(f"🏆 The highest resale price is **${max_price:,.0f}**.")

    elif "lowest price" in question_lower or "cheapest" in question_lower:
        min_price = df["resale_price"].min()
        st.markdown(f"📉 The lowest resale price is **${min_price:,.0f}**.")

    elif "average price in" in question_lower:
        for town in towns:
            if town.lower() in question_lower:
                avg = df[df["town"].str.lower() == town.lower()]["resale_price"].mean()
                st.markdown(f"📍 The average resale price in **{town}** is **${avg:,.0f}**.")
                break
        else:
            st.warning("❓ I couldn't find that town in the dataset.")

    elif "average price of" in question_lower:
        for flat in flat_types:
            if flat.lower() in question_lower:
                avg = df[df["flat_type"].str.lower() == flat.lower()]["resale_price"].mean()
                st.markdown(f"🏢 The average price of **{flat}** flats is **${avg:,.0f}**.")
                break

    elif "highest priced" in question_lower:
        for flat in flat_types:
            if flat.lower() in question_lower:
                price = df[df["flat_type"].str.lower() == flat.lower()]["resale_price"].max()
                st.markdown(f"🏆 The highest price for a **{flat}** flat is **${price:,.0f}**.")
                break

    elif "how many flats" in question_lower:
        count = df.shape[0]
        st.markdown(f"🏘️ The dataset contains **{count:,}** resale flat records.")

    elif "most common flat type" in question_lower:
        common = df["flat_type"].value_counts().idxmax()
        st.markdown(f"🔢 The most common flat type is **{common}**.")

    elif "resale flats in" in question_lower:
        for town in towns:
            if town.lower() in question_lower:
                subset = df[df["town"].str.lower() == town.lower()]
                st.markdown(f"📄 Sample resale flats in **{town}**:")
                st.dataframe(subset.head(10))
                break
        else:
            st.warning("❓ I couldn't find that town in the dataset.")

    elif "cheapest resale flats" in question_lower:
        town_prices = df.groupby("town")["resale_price"].mean().sort_values()
        town = town_prices.index[0]
        st.markdown(f"📉 The town with the cheapest average resale flats is **{town}** with an average of **${town_prices.iloc[0]:,.0f}**.")

    elif "most expensive resale flats" in question_lower:
        town_prices = df.groupby("town")["resale_price"].mean().sort_values(ascending=False)
        town = town_prices.index[0]
        st.markdown(f"💰 The most expensive town on average is **{town}** with an average of **${town_prices.iloc[0]:,.0f}**.")

    elif "most common flat type in" in question_lower:
        for town in towns:
            if town.lower() in question_lower:
                most_common = df[df["town"].str.lower() == town.lower()]["flat_type"].value_counts().idxmax()
                st.markdown(f"🏘️ The most common flat type in **{town}** is **{most_common}**.")
                break

    elif "average price in" in question_lower and "year" in question_lower:
        for year in df["year"].unique():
            if str(year) in question_lower:
                avg = df[df["year"] == int(year)]["resale_price"].mean()
                st.markdown(f"📅 The average resale price in **{year}** was **${avg:,.0f}**.")
                break

    elif "price trend" in question_lower or "changed over time" in question_lower:
        trend = df.groupby("year")["resale_price"].mean().reset_index()
        st.line_chart(trend.rename(columns={"year": "index"}).set_index("index"))

    elif "which year had highest" in question_lower:
        year = df.groupby("year")["resale_price"].mean().idxmax()
        price = df.groupby("year")["resale_price"].mean().max()
        st.markdown(f"📈 The year with the highest average resale price was **{year}**, with an average of **${price:,.0f}**.")

    elif "average resale price of" in question_lower and "in" in question_lower:
        for town in towns:
            if town.lower() in question_lower:
                for flat in flat_types:
                    if flat.lower() in question_lower:
                        avg = df[(df["town"].str.lower() == town.lower()) & (df["flat_type"].str.lower() == flat.lower())]["resale_price"].mean()
                        st.markdown(f"📍 The average price of **{flat}** flats in **{town}** is **${avg:,.0f}**.")
                        break

    elif "show me" in question_lower and "in" in question_lower:
        for town in towns:
            if town.lower() in question_lower:
                for flat in flat_types:
                    if flat.lower() in question_lower:
                        subset = df[(df["town"].str.lower() == town.lower()) & (df["flat_type"].str.lower() == flat.lower())]
                        st.markdown(f"📄 Sample **{flat}** flats in **{town}**:")
                        st.dataframe(subset.head(10))
                        break

    elif "which town has the most" in question_lower:
        for flat in flat_types:
            if flat.lower() in question_lower:
                counts = df[df["flat_type"].str.lower() == flat.lower()]["town"].value_counts()
                town = counts.idxmax()
                st.markdown(f"📊 The town with the most **{flat}** flats is **{town}**.")
                break

    else:
        st.warning("🤖 I didn’t understand that. Try asking about towns, flat types, prices, or years.")


