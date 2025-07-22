import streamlit as st
import pandas as pd
from openai import OpenAI

st.set_page_config(page_title="Sales Excel Analyzer", layout="wide")
st.title("📊 Excel Sales Analyzer with GPT Insights")

# Initialize OpenAI client using Streamlit secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# File upload
uploaded_file = st.file_uploader("Upload an Excel file", type=["xlsx", "xls"])

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)
        st.subheader("🔍 Preview of Data")
        st.dataframe(df)

        st.subheader("📈 Summary Statistics")
        st.write(df.describe(include='all'))

        # Generate AI Insights
        prompt = f"Analyze the following sales data and provide 5 actionable insights:\n\n{df.head(20).to_string()}"

        with st.spinner("Generating insights..."):
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}]
            )
            insights = response.choices[0].message.content

        st.subheader("🤖 GPT Insights")
        st.text_area("Insights from GPT", insights, height=300)

    except Exception as e:
        st.error(f"An error occurred while processing the file: {e}")