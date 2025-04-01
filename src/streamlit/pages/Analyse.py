import streamlit as st
from models.predict_model import predict_binary, predict_multiclass
from datetime import date
import pandas as pd
import time

st.set_page_config(
    page_title="Sentiment Analysis",
    page_icon="📝",
    layout="wide"
)

st.title("📝 Sentiment Analysis")

col1, col2, col3 = st.columns(3)
with st.container():
    st.subheader("Enter the necessary information for the analysis:")
    st.markdown("---")
    commentaire = st.text_area("📝 Comment:", placeholder="Enter a comment here...")
    col1, col2 = st.columns(2)
    with col1:
        date_experience = st.date_input("📅 Date of the experience:", value=date.today())
    with col2:
        note = st.slider(
            "⭐ Rating (1 to 5) for the multiclass model:",
            min_value=1,
            max_value=5,
            value=3,
            format="⭐ %d"
        )
    st.markdown("---")

col1, col2 = st.columns(2)
st.markdown("---")
with col1:
    if st.button("Analyze the sentiment polarity of the comment content"):
        if commentaire:
            data = pd.DataFrame({
                "Content": [commentaire],
                "dates.experiencedDate": [date_experience],
                "dates.publishedDate": [date.today()]
            })
            st.write("📄 Data sent to the `model`:", data)

            # Progress bar with gradient color
            progress_bar = st.empty()
            status_text = st.empty()

            for i in range(101):
                time.sleep(0.02)
                # Calculate gradient color from red to green
                red = int(255 * (1 - i / 100))
                green = int(255 * (i / 100))
                color = f"rgb({red},{green},0)"
                progress_bar.markdown(
                    f"""
                    <div style="width: 100%; background-color: #e0e0e0; border-radius: 5px; overflow: hidden;">
                    <div style="width: {i}%; background-color: {color}; height: 20px;"></div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                status_text.text(f"Analysis in progress... {i}%")

            result = predict_binary(data)
            st.success(f"The result of the sentiment polarity analysis is: {'Positive' if result[0] == 1 else 'Negative'}")

            # Clear progress bar and status text
            progress_bar.empty()
            status_text.empty()
        else:
            st.warning("Please enter a comment before analyzing.")

with col2:
    if st.button("Analyze the comment content to determine a rating between 1 and 5"):
        if commentaire:
            data = pd.DataFrame({
                "Content": [commentaire],
                "rating": [note],
                "dates.experiencedDate": [date_experience],
                "dates.publishedDate": [date.today()]
            })
            st.write("📄 Data sent to the `model`:", data)

            # Progress bar with gradient color
            progress_bar = st.empty()
            status_text = st.empty()

            for i in range(101):
                time.sleep(0.02)
                # Calculate gradient color from red to green
                red = int(255 * (1 - i / 100))
                green = int(255 * (i / 100))
                color = f"rgb({red},{green},0)"
                progress_bar.markdown(
                    f"""
                    <div style="width: 100%; background-color: #e0e0e0; border-radius: 5px; overflow: hidden;">
                    <div style="width: {i}%; background-color: {color}; height: 20px;"></div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                status_text.text(f"Analysis in progress... {i}%")

            result = (predict_multiclass(data)) + 1

            stars = "⭐" * result[0] + "☆" * (5 - result[0])
            st.success(f"The result of the comment's rating analysis is: {stars} (User's chosen rating: ⭐ {note})")
        else:
            st.warning("Please enter a comment before analyzing.")


# Footer with modern style
st.markdown(
    """
    <style>
    .footer {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background-color: #f8f9fa;
        text-align: center;
        padding: 10px 0;
        font-size: 14px;
        color: #6c757d;
        border-top: 1px solid #dee2e6;
        box-shadow: 0 -2px 5px rgba(0, 0, 0, 0.1);
        z-index: 1000;
    }
    .footer a {
        color: #007bff;
        text-decoration: none;
    }
    .footer a:hover {
        text-decoration: underline;
    }
    </style>
    <div class="footer">
        Created by <a href="">Baptiste Audroin</a>, <a href="">Jean-Claude Nguyen</a> and <a href="">Steffen Morvan</a>
    </div>
    """,
    unsafe_allow_html=True
)