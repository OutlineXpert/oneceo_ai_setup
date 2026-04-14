import streamlit as st
import requests
from openai import OpenAI

# ---- UI ----
st.title("✈️ AI Flight Planner")

openai_key = st.text_input("Enter OpenAI API Key", type="password")
amadeus_api_key = st.text_input("Enter Amadeus API Key")
amadeus_api_secret = st.text_input("Enter Amadeus API Secret", type="password")

source = st.text_input("Source (IATA Code e.g. BOM)")
destination = st.text_input("Destination (IATA Code e.g. DEL)")
date = st.date_input("Travel Date")

# ---- Get Amadeus Token ----
def get_amadeus_token(api_key, api_secret):
    url = "https://test.api.amadeus.com/v1/security/oauth2/token"
    data = {
        "grant_type": "client_credentials",
        "client_id": api_key,
        "client_secret": api_secret
    }
    response = requests.post(url, data=data)
    return response.json().get("access_token")

# ---- Search Flights ----
def search_flights(token, origin, destination, date):
    url = "https://test.api.amadeus.com/v2/shopping/flight-offers"
    headers = {"Authorization": f"Bearer {token}"}
    params = {
        "originLocationCode": origin,
        "destinationLocationCode": destination,
        "departureDate": str(date),
        "adults": 1,
        "max": 5
    }

    response = requests.get(url, headers=headers, params=params)
    return response.json()

# ---- AI Formatter ----
def format_with_ai(api_key, flight_data):
    client = OpenAI(api_key=api_key)

    prompt = f"""
    Convert this flight data into a user-friendly table:
    {flight_data}
    """

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return completion.choices[0].message.content

# ---- Button ----
if st.button("Search Flights"):
    if not all([openai_key, amadeus_api_key, amadeus_api_secret]):
        st.error("Please provide all API keys")
    else:
        with st.spinner("Fetching flights..."):
            token = get_amadeus_token(amadeus_api_key, amadeus_api_secret)
            flights = search_flights(token, source, destination, date)

            if "data" in flights:
                st.success("Flights Found!")

                # Raw display
                st.subheader("Raw Data")
                st.json(flights["data"])

                # AI formatted output
                st.subheader("AI Formatted Results")
                ai_output = format_with_ai(openai_key, flights["data"])
                st.write(ai_output)
            else:
                st.error("No flights found or API error")
