import requests
import streamlit as st

st.set_page_config(layout="wide", page_title='eProdukty API Explorer')

st.title('eProdukty API Explorer')


# Konfiguracja API
API_URL = "https://www.eprodukty.gs1.pl/external_api/v2"
HEADERS = {"Content-Type": "application/json"}


def fetch_products(api_key, params):
    """Pobieranie listy produktów."""
    response = requests.get(f"{API_URL}/products/", headers={**HEADERS, "X-API-KEY": api_key}, params=params)
    return response


def fetch_product_details(api_key, gtin_number):
    """Pobieranie szczegółów produktu."""
    response = requests.get(
        f"{API_URL}/products/{gtin_number}?include_local_data=true", headers={**HEADERS, "X-API-KEY": api_key}
    )
    return response


# Interfejs użytkownika
# Konfiguracja API Key
api_key = st.text_input("API Key", type="password")

# Formularz dla listowania produktów
with st.form("product_list_form"):
    st.header('Pobierz listę produktów')
    brand = st.text_input('Marka')
    company_name = st.text_input('Nazwa firmy')
    company_nip = st.text_input('NIP firmy')
    gpc_code = st.text_input('Kod GPC')
    last_modified_date_range = st.selectbox(
        'Zakres daty ostatniej modyfikacji', ('month', 'today', 'week', 'year', 'yesterday'), index=0
    )
    page_size = st.number_input('Rozmiar strony', value=10, min_value=1)
    submit_list = st.form_submit_button("Wyślij żądanie")

    if submit_list:
        params = {
            "brand": brand,
            "company_name": company_name,
            "company_nip": company_nip,
            "gpc_code": gpc_code,
            "last_modified_date_range": last_modified_date_range,
            "page_size": page_size,
        }
        response = fetch_products(api_key, params)
        st.json(response.text)

# Formularz dla szczegółów produktu
with st.form("product_details_form"):
    st.header('Pobierz szczegóły produktu')
    gtin_number = st.text_input('Numer GTIN')
    submit_details = st.form_submit_button("Wyślij żądanie")

    if submit_details and gtin_number:
        response = fetch_product_details(api_key, gtin_number)
        st.json(response.text)
