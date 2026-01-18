import streamlit as st
from supabase import create_client, Client

# Inicjalizacja połączenia z Supabase
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

st.title("📦 Zarządzanie Magazynem")

# --- SEKCJA KATEGORII ---
st.header("📂 Kategorie")

with st.expander("Dodaj nową kategorię"):
    kat_nazwa = st.text_input("Nazwa kategorii")
    kat_opis = st.text_area("Opis kategorii")
    if st.button("Dodaj kategorię"):
        data = {"nazwa": kat_nazwa, "opis": kat_opis}
        supabase.table("kategorie").insert(data).execute()
        st.success(f"Dodano kategorię: {kat_nazwa}")
        st.rerun()

# Lista kategorii z opcją usuwania
kategorie_data = supabase.table("kategorie").select("*").execute()
kategorie = kategorie_data.data

if kategorie:
    for kat in kategorie:
        col1, col2 = st.columns([4, 1])
        col1.write(f"**{kat['nazwa']}** - {kat['opis']}")
        if col2.button("Usuń", key=f"del_kat_{kat['id']}"):
            supabase.table("kategorie").delete().eq("id", kat['id']).execute()
            st.rerun()
else:
    st.info("Brak kategorii w bazie.")

st.divider()

# --- SEKCJA PRODUKTÓW ---
st.header("🛍️ Produkty")

with st.expander("Dodaj nowy produkt"):
    prod_nazwa = st.text_input("Nazwa produktu")
    prod_liczba = st.number_input("Liczba (szt.)", min_value=0, step=1)
    prod_cena = st.number_input("Cena", min_value=0.0, format="%.2f")
    
    # Wybór kategorii z listy (mapowanie nazwy na ID)
    kat_options = {k['nazwa']: k['id'] for k in kategorie}
    wybrana_kat = st.selectbox("Wybierz kategorię", options=list(kat_options.keys()))
    
    if st.button("Dodaj produkt"):
        nowy_produkt = {
            "nazwa": prod_nazwa,
            "liczba": prod_liczba,
            "cena": prod_cena,
            "kategoria_id": kat_options[wybrana_kat]
        }
        supabase.table("produkty").insert(nowy_produkt).execute()
        st.success(f"Dodano produkt: {prod_nazwa}")
        st.rerun()

# Lista produktów
produkty_data = supabase.table("produkty").select("*, kategorie(nazwa)").execute()
produkty = produkty_data.data

if produkty:
    for p in produkty:
        col1, col2, col3 = st.columns([3, 2, 1])
        col1.write(f"**{p['nazwa']}** ({p['kategorie']['nazwa']})")
        col2.write(f"{p['liczba']} szt. | {p['cena']} PLN")
        if col3.button("Usuń", key=f"del_prod_{p['id']}"):
            supabase.table("produkty").delete().eq("id", p['id']).execute()
            st.rerun()
else:
    st.info("Brak produktów w bazie.")
