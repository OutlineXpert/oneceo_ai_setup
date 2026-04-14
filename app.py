import streamlit as st
from openai import OpenAI

# ---- UI ----
st.title("✈️ AI Flight Planner (Simple)")

api_key = st.text_input("Enter OpenAI API Key", type="password")

source = st.text_input("Source City (e.g. Mumbai)")
destination = st.text_input("Destination City (e.g. Delhi)")
date = st.date_input("Travel Date")

# ---- AI Function ----
def get_flight_plan(api_key, source, destination, date):
    client = OpenAI(api_key=api_key)

    prompt = f"""
    You are a flight search assistant.

    Generate realistic flight options for:
    From: {source}
    To: {destination}
    Date: {date}

    Provide 5 options with:
    - Airline
    - Departure Time
    - Arrival Time
    - Duration
    - Price (in INR)
    - Stops (Non-stop / 1 stop)

    Format as a clean table.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content

# ---- Button ----
if st.button("Search Flights"):
    if not api_key:
        st.error("Please enter OpenAI API key")
    else:
        with st.spinner("Generating flights..."):
            result = get_flight_plan(api_key, source, destination, date)

            st.subheader("Available Flights ✈️")
            st.write(result)
