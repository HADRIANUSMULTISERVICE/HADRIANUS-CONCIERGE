import streamlit as st
import datetime
import pandas as pd
import google.generativeai as genai

# --- CONFIGURAZIONE PAGINA E STILE ---
st.set_page_config(page_title="Hadriano Concierge", page_icon="🛎️", layout="centered")

# Stile CSS personalizzato per replicare il look "Luxury/Gold" del tuo codice React
st.markdown("""
    <style>
    .stApp { background-color: #FDFDFD; color: #1A1A1A; }
    h1, h2, h3 { font-family: 'Serif'; font-style: italic; color: #1A1A1A; }
    .gold-text { color: #D4AF37; font-weight: bold; text-transform: uppercase; letter-spacing: 2px; font-size: 12px; }
    .big-gold { color: #D4AF37; font-size: 3rem; font-weight: bold; font-family: 'Serif'; font-style: italic; }
    div[data-testid="stMetricValue"] { color: #D4AF37; }
    .stButton>button {
        background-color: #1A1A1A; color: #D4AF37; border-radius: 20px; 
        text-transform: uppercase; letter-spacing: 1px; font-size: 10px; font-weight: bold; border: none;
    }
    .stButton>button:hover { background-color: #D4AF37; color: white; }
    </style>
""", unsafe_allow_html=True)

# --- CONFIGURAZIONE ADMIN (Hardcoded come nel tuo file originale) ---
SUPER_ADMIN_EMAIL = "admin@conciergepro.it"
SUPER_ADMIN_PASS = "admin123"

# --- DATI INIZIALI (Tradotti dal tuo App.tsx) ---
# Usiamo st.session_state per mantenere i dati in memoria mentre usi l'app
def init_data():
    if 'users' not in st.session_state:
        st.session_state.users = [
            {'id': 'h1', 'email': 'marco@host.it', 'password': 'password123', 'fullName': 'Marco Rossi', 'role': 'HOST', 'isContactAvailable': True},
            {'id': 'h2', 'email': 'elena@host.it', 'password': 'securepass456', 'fullName': 'Elena Bianchi', 'role': 'HOST', 'isContactAvailable': True}
        ]
    
    if 'apartments' not in st.session_state:
        st.session_state.apartments = [
            {
                'id': 'a1', 'name': 'Tortona Boutique Loft', 'address': 'Via Tortona 12, Milano', 
                'houseRules': '1. Rispetta il silenzio dopo le 22:00.\n2. Non fumare.\n3. Rifiuti negli appositi contenitori.',
                'wifiName': 'Boutique_Guest', 'wifiPassword': 'milano-luxury',
                'videoUrl': 'https://www.w3schools.com/html/mov_bbb.mp4',
                'hostId': 'h1', 'lat': 45.4518, 'lon': 9.1678,
                'recommendations': [{'name': 'Langosteria', 'category': 'Ristorante', 'desc': 'Miglior pesce di Milano.'}]
            },
            {
                'id': 'a2', 'name': 'Brera Art District Suite', 'address': 'Via Brera 5, Milano', 
                'houseRules': '1. Massimo silenzio.\n2. Vietato fumare.',
                'wifiName': 'Brera_Guest', 'wifiPassword': 'art-and-style',
                'videoUrl': '',
                'hostId': 'h2', 'lat': 45.4718, 'lon': 9.1878,
                'recommendations': []
            }
        ]
    
    if 'bookings' not in st.session_state:
        st.session_state.bookings = [
             {'id': 'b0', 'apartmentId': 'a1', 'guestName': 'Ospite Demo', 'bookingCode': 'WELCOME', 'checkInDate': str(datetime.date.today()), 'status': 'ACTIVE'}
        ]
    
    if 'auth' not in st.session_state:
        st.session_state.auth = {'user': None, 'role': None}

init_data()

# --- FUNZIONI DI UTILITÀ ---
def login_guest(code):
    code = code.upper().strip()
    booking = next((b for b in st.session_state.bookings if b['bookingCode'] == code and b['status'] == 'ACTIVE'), None)
    
    if code == "WELCOME": # Backdoor demo come nel tuo codice
        st.session_state.auth = {'user': {'id': 'guest_demo', 'fullName': "Ospite d'Onore"}, 'role': 'GUEST'}
        # Assicuriamoci che la prenotazione demo esista
        demo_booking = next((b for b in st.session_state.bookings if b['bookingCode'] == 'WELCOME'), None)
        st.session_state.active_booking = demo_booking
        st.rerun()
    elif booking:
        st.session_state.auth = {'user': {'id': booking['id'], 'fullName': booking['guestName']}, 'role': 'GUEST'}
        st.session_state.active_booking = booking
        st.rerun()
    else:
        st.error("Codice non valido o scaduto.")

def login_staff(email, password):
    if email == SUPER_ADMIN_EMAIL and password == SUPER_ADMIN_PASS:
        st.session_state.auth = {'user': {'id': 'admin', 'fullName': 'Super Admin'}, 'role': 'ADMIN'}
        st.rerun()
        return

    user = next((u for u in st.session_state.users if u['email'] == email and u['password'] == password and u['role'] == 'HOST'), None)
    if user:
        st.session_state.auth = {'user': user, 'role': 'HOST'}
        st.rerun()
    else:
        st.error("Credenziali errate.")

def logout():
    st.session_state.auth = {'user': None, 'role': None}
    st.rerun()

# --- INTEGRAZIONE AI (GEMINI) ---
def ask_hadriano_ai(question, context_text):
    # Recupera la chiave dai Secrets
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = f"""
        Sei Hadriano, un concierge di lusso virtuale. Sei educato, professionale e breve.
        
        Informazioni sull'appartamento e sulla zona:
        {context_text}
        
        Domanda dell'ospite: {question}
        Rispondi all'ospite in italiano.
        """
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return "Mi dispiace, al momento non riesco a connettermi al mio cervello digitale. Riprova più tardi."

# --- VISTE (PAGINE) ---

def view_login():
    st.markdown("<div style='text-align: center; margin-top: 50px;'>", unsafe_allow_html=True)
    st.markdown("<p class='gold-text'>PREMIUM BOUTIQUE SERVICES</p>", unsafe_allow_html=True)
    st.title("Hadriano Concierge")
    st.markdown("</div>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["OSPITE", "STAFF / HOST"])
    
    with tab1:
        code = st.text_input("Inserisci il tuo Codice Soggiorno", placeholder="Es. WELCOME")
        if st.button("Entra in Casa"):
            login_guest(code)
            
    with tab2:
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        if st.button("Login Staff"):
            login_staff(email, password)

def view_guest():
    user = st.session_state.auth['user']
    booking = st.session_state.get('active_booking')
    
    # Troviamo l'appartamento collegato
    apt = next((a for a in st.session_state.apartments if a['id'] == booking['apartmentId']), None)
    host = next((u for u in st.session_state.users if u['id'] == apt['hostId']), None) if apt else None
    
    # Header
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f"<h1 style='font-size: 2rem;'>Benvenuto, {user['fullName']}</h1>", unsafe_allow_html=True)
        if apt: st.markdown(f"<p class='gold-text'>{apt['name']}</p>", unsafe_allow_html=True)
    with col2:
        if st.button("Logout", key="logout_guest"): logout()

    st.divider()

    # Menu Navigazione
    menu = st.radio("Cosa ti serve?", ["🏠 Home", "📶 WiFi", "📜 Regole", "🗺️ Guida", "🤖 Chiedi ad Hadriano"], horizontal=True)

    if menu == "🏠 Home":
        st.write("📍", apt['address'])
        if apt.get('videoUrl'):
            st.subheader("Video Istruzioni Ingresso")
            st.video(apt['videoUrl'])
        
        # Mappa semplice
        if 'lat' in apt:
            df_map = pd.DataFrame({'lat': [apt['lat']], 'lon': [apt['lon']]})
            st.map(df_map, zoom=15)

    elif menu == "📶 WiFi":
        st.markdown("<div style='text-align: center; padding: 40px; background-color: #fff; border-radius: 20px; border: 1px solid #eee;'>", unsafe_allow_html=True)
        st.markdown("<p class='gold-text'>RETE WI-FI</p>", unsafe_allow_html=True)
        st.markdown(f"<h2>{apt['wifiName']}</h2>", unsafe_allow_html=True)
        st.markdown("<p class='gold-text'>PASSWORD</p>", unsafe_allow_html=True)
        st.markdown(f"<h2 class='big-gold'>{apt['wifiPassword']}</h2>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    elif menu == "📜 Regole":
        st.info(apt['houseRules'])

    elif menu == "🗺️ Guida":
        st.subheader("I Consigli dell'Host")
        if not apt['recommendations']:
            st.write("Nessun consiglio specifico inserito ancora.")
        for rec in apt['recommendations']:
            with st.expander(f"{rec['category']}: {rec['name']}"):
                st.write(rec['desc'])

    elif menu == "🤖 Chiedi ad Hadriano":
        st.markdown("*Il tuo Concierge AI personale.*")
        user_question = st.chat_input("Chiedimi consigli su ristoranti, trasporti o sulla casa...")
        
        if user_question:
            # Costruiamo il contesto per l'AI
            context = f"L'ospite si trova in: {apt['name']} a {apt['address']}. Regole casa: {apt['houseRules']}. Consigli host: {str(apt['recommendations'])}"
            with st.spinner("Hadriano sta pensando..."):
                reply = ask_hadriano_ai(user_question, context)
                st.write(reply)

    # Bottone emergenza / contatto
    st.divider()
    if host and host.get('isContactAvailable'):
        st.success(f"L'Host {host['fullName']} è disponibile. Invia un messaggio se urgente.")
    else:
        st.caption("Host attualmente non disponibile.")

def view_admin():
    st.markdown("<p class='gold-text'>PANNELLO DI CONTROLLO</p>", unsafe_allow_html=True)
    st.title("Admin Dashboard")
    if st.button("Logout Admin"): logout()
    
    st.divider()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Gestione Host")
        # Form aggiunta host
        with st.form("add_host"):
            new_name = st.text_input("Nome Host")
            new_email = st.text_input("Email Host")
            new_pass = st.text_input("Password")
            if st.form_submit_button("Crea Host"):
                st.session_state.users.append({
                    'id': f'h{len(st.session_state.users)+1}', 
                    'fullName': new_name, 'email': new_email, 'password': new_pass, 
                    'role': 'HOST', 'isContactAvailable': True
                })
                st.success("Host creato!")
                st.rerun()
        
        st.write("---")
        for u in st.session_state.users:
            if u['role'] == 'HOST':
                st.write(f"👤 **{u['fullName']}** ({u['email']})")

    with col2:
        st.subheader("Gestione Appartamenti")
        with st.form("add_apt"):
            apt_name = st.text_input("Nome Appartamento")
            apt_addr = st.text_input("Indirizzo")
            apt_wifi = st.text_input("Nome WiFi")
            apt_pass = st.text_input("Pass WiFi")
            # Seleziona host
            hosts = [u for u in st.session_state.users if u['role'] == 'HOST']
            host_options = {h['fullName']: h['id'] for h in hosts}
            selected_host_name = st.selectbox("Assegna a Host", list(host_options.keys()) if hosts else [])
            
            if st.form_submit_button("Crea Appartamento"):
                if hosts:
                    st.session_state.apartments.append({
                        'id': f'a{len(st.session_state.apartments)+1}',
                        'name': apt_name, 'address': apt_addr, 
                        'wifiName': apt_wifi, 'wifiPassword': apt_pass,
                        'hostId': host_options[selected_host_name],
                        'houseRules': 'Regole standard...', 'recommendations': [], 'videoUrl': '',
                        'lat': 45.4642, 'lon': 9.1900 
                    })
                    st.success("Appartamento creato!")
                    st.rerun()

def view_host():
    user = st.session_state.auth['user']
    st.markdown(f"<p class='gold-text'>PORTALE HOST</p>", unsafe_allow_html=True)
    st.title(f"Ciao, {user['fullName']}")
    if st.button("Logout"): logout()
    
    # I miei appartamenti
    my_apts = [a for a in st.session_state.apartments if a['hostId'] == user['id']]
    
    st.divider()
    st.subheader("Genera Nuovo Codice Ospite")
    
    if not my_apts:
        st.warning("Non hai appartamenti assegnati dall'Admin.")
    else:
        with st.form("create_booking"):
            apt_choice = st.selectbox("Per quale appartamento?", [a['name'] for a in my_apts])
            guest_name = st.text_input("Nome Ospite")
            days = st.number_input("Giorni di permanenza", min_value=1, value=3)
            
            if st.form_submit_button("Crea Prenotazione"):
                import random, string
                code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
                selected_apt_id = next(a['id'] for a in my_apts if a['name'] == apt_choice)
                
                st.session_state.bookings.append({
                    'id': f'b{len(st.session_state.bookings)+1}',
                    'apartmentId': selected_apt_id,
                    'guestName': guest_name,
                    'bookingCode': code,
                    'checkInDate': str(datetime.date.today()),
                    'status': 'ACTIVE'
                })
                st.success(f"Prenotazione Creata! Codice: {code}")
                st.rerun()
    
    st.divider()
    st.subheader("Prenotazioni Attive")
    # Filtra prenotazioni per gli appartamenti di questo host
    my_apt_ids = [a['id'] for a in my_apts]
    my_bookings = [b for b in st.session_state.bookings if b['apartmentId'] in my_apt_ids]
    
    if my_bookings:
        for b in my_bookings:
            apt_name = next(a['name'] for a in st.session_state.apartments if a['id'] == b['apartmentId'])
            with st.container():
                st.markdown(f"""
                <div style='background-color: white; padding: 20px; border-radius: 15px; margin-bottom: 10px; border: 1px solid #eee;'>
                    <h3 style='margin:0'>{b['guestName']}</h3>
                    <p style='color: gray; font-size: 12px;'>{apt_name} • Check-in: {b['checkInDate']}</p>
                    <p class='gold-text' style='font-size: 18px;'>CODICE: {b['bookingCode']}</p>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"Cancella {b['bookingCode']}", key=b['id']):
                     st.session_state.bookings.remove(b)
                     st.rerun()

# --- MAIN ROUTER ---
if st.session_state.auth['user'] is None:
    view_login()
elif st.session_state.auth['role'] == 'ADMIN':
    view_admin()
elif st.session_state.auth['role'] == 'HOST':
    view_host()
elif st.session_state.auth['role'] == 'GUEST':
    view_guest()
