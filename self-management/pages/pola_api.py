import requests
import streamlit as st

# Konfiguracja API - lista dostępnych serwerów
servers = {
    "Production": "https://www.pola-app.pl",
    "Staging": "https://pola-staging.herokuapp.com",
    "Docker": "http://web:8080",
}

# Interfejs użytkownika
st.title('Pola API Explorer')

# Wybór serwera
selected_server = st.selectbox("Choose Server", list(servers.keys()))

api_url = servers[selected_server]

# Globalne nagłówki (jeśli wymagane)
headers = {
    "Content-Type": "application/json",
}

# Formularze dla każdego endpointu
with st.form(key='get_by_code_form'):
    st.subheader("Get Product by Code")
    code = st.text_input("Code", key='gb_code', value='5901912622548')
    device_id = st.text_input("Device ID", key='gb_device_id', value="TEST-DEVICE-ID")
    noai = st.checkbox("No AI", value=False, key='gb_noai')
    submit_code = st.form_submit_button("Send GET Request")

    if submit_code:
        params = {"code": code, "device_id": device_id, "noai": noai}
        response = requests.get(api_url + "/a/v4/get_by_code", headers=headers, params=params)
        st.json(response.json())

with st.form(key='search_form'):
    st.subheader("Search Products")
    query = st.text_input("Query", key='s_query', value='Baton')
    page_token = st.text_input("Page Token", key='s_page_token')
    device_id = st.text_input("Device ID (optional)", key='s_device_id', value="TEST-DEVICE-ID")
    submit_search = st.form_submit_button("Send GET Request")

    if submit_search:
        params = {"query": query, "pageToken": page_token, "device_id": device_id}
        params = {k: v for k, v in params.items() if v}
        response = requests.get(api_url + "/a/v4/search", headers=headers, params=params)
        st.json(response.json())

with st.form(key='subscribe_newsletter_form'):
    st.subheader("Subscribe to Newsletter")
    contact_email = st.text_input("Contact Email", key='sn_email', value='test@example.com')
    contact_name = st.text_input("Contact Name", key='sn_name', value="TEST USER")
    submit_newsletter = st.form_submit_button("Send POST Request")

    if submit_newsletter:
        data = {"contact_email": contact_email, "contact_name": contact_name}
        response = requests.post(api_url + "/a/v4/subscribe_newsletter", headers=headers, json=data)
        if response.status_code == 204:
            st.success("Subscribed successfully!")
        else:
            st.json(response.json())
