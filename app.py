import streamlit as st
import google.generativeai as genai

# Configurazione della pagina
st.set_page_config(page_title="La mia AI", page_icon="🤖")

st.title("🤖 La mia Intelligenza Artificiale")
st.write("Scrivi qui sotto e ti risponderò gratis!")

# Recuperiamo la chiave segreta (che imposteremo dopo)
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash') # Modello veloce e gratuito

    # Casella di testo per l'utente
    user_input = st.text_area("La tua domanda:", height=150)

    if st.button("Invia domanda"):
        if user_input:
            with st.spinner('Sto pensando...'):
                try:
                    response = model.generate_content(user_input)
                    st.success("Ecco la risposta:")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"Errore: {e}")
        else:
            st.warning("Per favore scrivi qualcosa prima di inviare!")

except Exception as e:
    st.error("Manca la Chiave API! Devi impostarla nei 'Secrets' di Streamlit.")
