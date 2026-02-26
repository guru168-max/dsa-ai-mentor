import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

# Google API scope
scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

sheet = None

try:
    # Load credentials from Streamlit Secrets
    creds_dict = st.secrets["gcp_service_account"]

    creds = Credentials.from_service_account_info(
        creds_dict,
        scopes=scope
    )

    client = gspread.authorize(creds)

    # Open sheet
    sheet = client.open("DSA_AI_Mentor_Data").sheet1
    print("Connected to Google Sheet successfully!")

except Exception as e:
    print("Error connecting to Google Sheet:", e)
    sheet = None


def save_to_sheet(topic, difficulty, problem, result):
    if sheet is None:
        print("Sheet not connected. Cannot save data.")
        return

    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        sheet.append_row([
            timestamp,
            topic,
            difficulty,
            problem,
            result
        ])

        print("Data saved successfully!")

    except Exception as e:
        print("Error while saving to sheet:", e)
