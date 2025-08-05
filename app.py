import streamlit as st
import subprocess
import os

def show_logs():
    if os.path.exists("scraper.log"):
        with open("scraper.log", encoding='utf-8') as f:
            st.text(f.read())
    else:
        st.warning("No log file found.")

st.set_page_config(page_title="LinkedIn Scraper", page_icon="🔍")
st.title("LinkedIn Profile URL Scraper")

email = st.text_input("LinkedIn Email")
password = st.text_input("LinkedIn Password", type="password")
role = st.text_input("Job Role (e.g., Software Engineer)")
location = st.text_input("Location (e.g., Bangalore)")
experience = st.text_input("Experience (e.g., 5 years, Senior, Entry Level)")  # ✅ New field
pages = st.slider("Number of pages to scrape (max 50)", 1, 50, 5)
csv_filename = st.text_input("CSV filename (e.g., candidates.csv)", "candidates.csv")

if st.button("Start Scraping"):
    if not csv_filename.endswith('.csv'):
        csv_filename += '.csv'
    if not (email and password):
        st.error("Please enter your LinkedIn credentials.")
    else:
        st.info("A browser will open shortly. Please log in to LinkedIn. Scraping will begin automatically after login.")
        result = subprocess.run(
            ["python", "scraper.py", email, password, role, location, experience, str(pages), csv_filename],
            capture_output=True, text=True
        )
        if os.path.exists(csv_filename):
            with open(csv_filename, "rb") as f:
                st.download_button("Download CSV", f, file_name=csv_filename, mime="text/csv")
        else:
            st.error("No CSV generated. Check logs below.")
        st.subheader("Scraper Logs")
        show_logs()
