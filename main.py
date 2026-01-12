import pandas as pd
import numpy as np
import streamlit as st
import os
import plotly.express as px
import json


category_file = "categories.json"


if os.path.exists(category_file):
    try:
        with open(category_file,"r") as f:
            st.session_state.categories = json.load(f)
    except json.JSONDecodeError:
        st.session_state.categories = {
            "Uncategorized" : []
        }
else:
    st.session_state.categories = {
            "Uncategorized" : []
        }
    
        


        

def save_categories():
    with open(category_file,"w") as f:
        json.dump(st.session_state.categories,f)


def load_transactions(file):
    try:
        df = pd.read_csv(file)
        df.columns = [col.strip() for col in df.columns]
        df["Amount"] = df["Amount"].str.replace(",","").astype(float)
        df["Date"] = pd.to_datetime(df["Date"],format="%d %b %Y")
        st.write(df)
        return categorize_transactions(df)
    except Exception as e:
        st.error(f"error in processing file: {str(e)}")
        return None

def categorize_transactions(df):
    if "category" not in df.columns:
        df['category'] = "Uncategorized"
    
    for i,js in st.session_state.categories.items():
        if i == "Uncategorized" or not js:
            continue
        lowered_keywords = [j.lower().strip() for j in js]

        for idx,row in df.iterrows():
            details = row["Details"].lower().strip()
            if details in lowered_keywords:
                df.at[idx,"Category"] = i

    return df



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
                new_category = st.text_input("New CategoryName")
                add_button = st.button("Add Category")

                

                if add_button and new_category:
                    if new_category not in st.session_state.categories:
                        st.session_state.categories[new_category] = []
                        save_categories()
                        st.rerun()
                
            with tab2:
                st.write(debits_df)

main()
