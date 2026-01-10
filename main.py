import pandas as pd
import numpy as np
import streamlit as st
import os
import plotly.express as px


def load_transactions(file):
    try:
        df = pd.read_csv(file)
        df.columns = [col.strip() for col in df.columns]
        df["Amount"] = df["Amount"].str.replace(",","").astype(float)
        df["Date"] = pd.to_datetime(df["Date"],format="%d %b %Y")
        st.write(df)
        return df
    except Exception as e:
        st.error(f"error in processing file: {str(e)}")
        return None


def main():
    st.set_page_config(page_title="Personal SmartFinance",page_icon="💴",layout="wide")
    st.title("Personal Smart Financer",text_alignment="center")
    uploaded_file = st.file_uploader("uplolad the transactions csv files here",type="csv")
    if uploaded_file is not None:
        df = load_transactions(uploaded_file)
        if df is not None:
            debits_df = df[df["Debit/Credit"] == "Debit"].copy()
            credits_df = df[df["Debit/Credit"] == "Credit"].copy()

            tab1,tab2 = st.tabs(["Expenses(Credits)","Expenses(Debits)"])
            with tab1:
                st.write(credits_df)
            with tab2:
                st.write(debits_df)

main()
