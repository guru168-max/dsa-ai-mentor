import streamlit as st
import gspread
import json
from google.oauth2.service_account import Credentials
from datetime import datetime

scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

sheet = None

try:
    creds_dict = json.loads(st.secrets["gcp_service_account"])

    creds = Credentials.from_service_account_info(
        creds_dict,
        scopes=scope
    )

    client = gspread.authorize(creds)
    sheet = client.open("DSA_AI_Mentor_Data").sheet1

except Exception as e:
    print("Error connecting to Google Sheet:", e)
    sheet = None


def save_to_sheet(topic, difficulty, problem, result):
    if sheet is None:
        return

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    sheet.append_row([
        timestamp,
        topic,
        difficulty,
        problem,
        result
    ])
