import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import sys
import os

# Fix import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# ✅ Fixed: was importing get_sentiment which didn't exist
from backend.sentiment_analysis import get_sentiment

st.set_page_config(page_title="CX Analytics Dashboard", layout="wide")

st.title("📊 CX Analytics Dashboard")

# 📥 Upload CSV
uploaded_file = st.file_uploader("Upload Customer Feedback CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file, engine='python', on_bad_lines='skip')

    st.subheader("📄 Raw Data")
    st.write(df.head())

    # 🔍 Detect text column automatically
    text_col = None
    for col in df.columns:
        if "review" in col.lower() or "text" in col.lower() or "feedback" in col.lower():
            text_col = col
            break

    if text_col is None:
        st.error("No valid review/text column found!")
        st.stop()

    # 🧹 Clean text
    df[text_col] = df[text_col].astype(str).str.lower().str.strip()

    # 🧠 Sentiment Analysis
    sentiment_results = df[text_col].apply(get_sentiment)

    # Extract structured fields from dict return
    df["sentiment"] = sentiment_results.apply(lambda x: x["sentiment"])
    df["score"] = sentiment_results.apply(lambda x: x["score"])

    # 🏷️ Issue Categorization
    def categorize_issue(text):
        if "delivery" in text or "late" in text or "delay" in text:
            return "Delivery"
        elif "app" in text or "crash" in text or "bug" in text:
            return "Technical"
        elif "support" in text or "service" in text:
            return "Service"
        elif "product" in text or "damaged" in text:
            return "Product"
        else:
            return "Other"

    df["issue"] = df[text_col].apply(categorize_issue)

    # 📊 Summary Metrics
    total_reviews = len(df)
    sentiment_counts = df["sentiment"].value_counts()
    issue_counts = df["issue"].value_counts()

    colA, colB, colC = st.columns(3)
    colA.metric("Total Reviews", total_reviews)
    colB.metric("Positive %", f"{(sentiment_counts.get('Positive', 0)/total_reviews)*100:.1f}%")
    colC.metric("Negative %", f"{(sentiment_counts.get('Negative', 0)/total_reviews)*100:.1f}%")

    # 📊 Charts
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Sentiment Distribution")
        fig1, ax1 = plt.subplots()
        ax1.pie(sentiment_counts, labels=sentiment_counts.index, autopct='%1.1f%%')
        st.pyplot(fig1)

    with col2:
        st.subheader("Issue Distribution")
        fig2, ax2 = plt.subplots()
        ax2.bar(issue_counts.index, issue_counts.values)
        plt.xticks(rotation=30)
        st.pyplot(fig2)

    # 📅 Trend Analysis
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        df = df.dropna(subset=["date"])
        df = df.sort_values(by="date")

        st.subheader("📈 Feedback Trend Over Time")
        trend_data = df.groupby("date").size()

        fig3, ax3 = plt.subplots()
        ax3.plot(trend_data.index, trend_data.values)
        ax3.set_xlabel("Date")
        ax3.set_ylabel("Number of Reviews")
        ax3.set_title("Customer Feedback Trend")
        fig3.autofmt_xdate()
        st.pyplot(fig3)

        st.subheader("📊 Sentiment Trend Over Time")
        sentiment_trend = df.groupby(["date", "sentiment"]).size().unstack().fillna(0)

        fig4, ax4 = plt.subplots()
        for sentiment in sentiment_trend.columns:
            ax4.plot(sentiment_trend.index, sentiment_trend[sentiment], label=sentiment)
        ax4.set_xlabel("Date")
        ax4.set_ylabel("Count")
        ax4.set_title("Sentiment Trend")
        ax4.legend()
        fig4.autofmt_xdate()
        st.pyplot(fig4)

    # 🧠 Insights
    st.subheader("📌 Key Insights")

    top_issue = issue_counts.idxmax()
    negative_percent = (sentiment_counts.get("Negative", 0) / total_reviews) * 100

    st.write(f"🔴 Most common issue: {top_issue}")
    st.write(f"⚠️ Negative feedback: {negative_percent:.2f}%")

    if "date" in df.columns and len(df) > 1:
        if trend_data.iloc[-1] > trend_data.iloc[0]:
            st.write("⚠️ Customer complaints are increasing over time.")
        else:
            st.write("✅ Customer feedback trend is stable or improving.")

    # 💡 Recommendations
    st.subheader("💡 Recommendations")

    if top_issue == "Delivery":
        st.write("Improve delivery speed and optimize logistics routes.")
    elif top_issue == "Technical":
        st.write("Fix application bugs and improve system performance.")
    elif top_issue == "Service":
        st.write("Enhance customer support training and responsiveness.")
    elif top_issue == "Product":
        st.write("Improve product quality control and packaging.")
    else:
        st.write("Monitor feedback for emerging issues.")