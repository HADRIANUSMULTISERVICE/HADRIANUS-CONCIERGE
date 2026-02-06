import streamlit as st
import datetime
import pandas as pd
import google.generativeai as genai

# --- 1. CONFIGURAZIONE E CSS (Fixed: Leggibilità e Allineamento) ---
st.set_page_config(page_title="Hadriano Concierge", page_icon="🛎️", layout="wide")

st.markdown("""
    <style>
    /* --- FONT --- */
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;0,700;1,400&family=Lato:wght@300;400;700&display=swap');
    
    /* --- BASE --- */
    .stApp {
        background-color: #F9F9F9; /* Grigio chiarissimo elegante */
        color: #333333;
        font-family: 'Lato', sans-serif;
    }
    
    /* --- TITOLI --- */
    h1, h2, h3 {
        font-family: 'Playfair Display', serif;
        color: #111;
    }
    
    /* --- ACCENTI --- */
    .gold-text {
        color: #C5A059;
        font-weight: bold;
        text-transform: uppercase;
        font-size: 12px;
        letter-spacing: 1px;
    }

    /* --- CAMPI DI INPUT (Fixed: Sfondo Bianco, Testo Nero, Allineamento) --- */
    /* Forza lo stile dei campi input standard */
    div[data-baseweb="input"] {
        background-color: #FFFFFF !important;
        border: 1px solid #CCCCCC !important;
        border-radius: 5px !important;
    }
    /* Forza il colore del testo digitato */
    input {
        color: #000000 !important;
    }
    /* Forza lo stile delle select box */
    div[data-baseweb="select"] > div {
        background-color: #FFFFFF !important;
        border: 1px solid #CCCCCC !important;
        color: #000000 !important;
    }
    /* Etichette (Label) ben visibili e allineate a sinistra */
    label p {
        color: #333333 !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        text-align: left !important;
    }

    /* --- BOTTONI --- */
    .stButton>button {
        background-color: #111;
        color: #C5A059 !important;
        border: 1px solid #C5A059;
        border-radius: 0px; /* Squadrati eleganti */
        text-transform: uppercase;
        font-weight: bold;
        padding: 10px 20px;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #C5A059;
        color: white !important;
    }

    /* --- CARDS --- */
    .clean-card {
        background-color: white;
        padding: 30px;
        border: 1px solid #E0E0E0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.02);
        margin-bottom: 20px;
        border-radius: 8px;
    }
    
    /* --- LOGIN BOX --- */
    .login-box {
        background-color: white;
        padding: 40px;
        border-radius: 10px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05);
        border-top: 5px solid #C5A059;
        text-align: left; /* Allineamento interno a sinistra per i campi */
    }

    /* --- TABS --- */
    .stTabs [data-baseweb="tab-list"] { gap: 20px; }
    .stTabs [data-baseweb="tab"] { font-family: 'Playfair Display', serif; font-size: 16px; }
    </style>
""", unsafe_allow_html=True)

# --- 2. DATI (Aggiunto Cover Image) ---
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
                'coverImage': 'https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?q=80&w=2000&auto=format&fit=crop', # Default placeholder
                'houseRules': '1. Vietato fumare.\n2. No feste.',
                'wifiName': 'Tortona_Guest', 'wifiPassword': 'design-milano',
                'videoUrl': '',
                'hostId': 'h1',
                'points_of_interest': [ # Rinominato da recommendations per chiarezza
                    {'id': 'p1', 'name': 'Langosteria', 'category': 'Ristorante', 'desc': 'Cena di pesce raffinata.', 'map': 'https://goo.gl/maps'}
                ]
            }
        ]
    
    if 'bookings' not in st.session_state:
        st.session_state.bookings = [
             {'id': 'b0', 'apartmentId': 'a1', 'guestName': 'Ospite Demo', 'bookingCode': 'WELCOME', 'checkInDate': str(datetime.date.today()), 'status': 'ACTIVE'}
        ]
        
    if 'auth' not in st.session_state: st.session_state.auth = {'user': None, 'role': None}
    
    # Stati temporanei per editing
    if 'editing_apt_id' not in st.session_state: st.session_state.editing_apt_id = None
    if 'editing_host_id' not in st.session_state: st.session_state.editing_host_id = None
    if 'edit_mode_apt_details' not in st.session_state: st.session_state.edit_mode_apt_details = None

init_data()

# --- UTILS ---
def get_user_name(user_id):
    user = next((u for u in st.session_state.users if u['id'] == user_id), None)
    return user['fullName'] if user else "Nessuno"

def logout():
    st.session_state.auth = {'user': None, 'role': None}
    st.rerun()

# --- 3. LOGIN SCREEN (Pulito e Leggibile) ---
def login_screen():
    c1, c2, c3 = st.columns([1, 1.5, 1])
    with c2:
        st.markdown("""
        <div style="text-align: center; margin-bottom: 20px;">
            <h1 style="font-size: 3rem; margin-bottom: 5px;">Hadriano</h1>
            <p class="gold-text">Luxury Concierge Services</p>
        </div>
        """, unsafe_allow_html=True)
        
        tab_guest, tab_staff = st.tabs(["OSPITE", "STAFF"])
        
        with tab_guest:
            st.markdown('<div class="login-box">', unsafe_allow_html=True)
            st.markdown("### Accesso Suite")
            code = st.text_input("Inserisci il Codice Prenotazione", placeholder="Es. WELCOME")
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("ENTRA", use_container_width=True):
                code = code.upper().strip()
                if code == "WELCOME": # Logica Backdoor Demo
                    if not any(b['bookingCode'] == 'WELCOME' for b in st.session_state.bookings):
                         st.session_state.bookings.append({'id': 'b0', 'apartmentId': 'a1', 'guestName': 'Ospite Demo', 'bookingCode': 'WELCOME', 'checkInDate': str(datetime.date.today()), 'status': 'ACTIVE'})
                    st.session_state.auth = {'user': {'id': 'demo', 'fullName': 'Ospite Eccellente'}, 'role': 'GUEST'}
                    st.session_state.active_booking_code = 'WELCOME'
                    st.rerun()
                
                booking = next((b for b in st.session_state.bookings if b['bookingCode'] == code), None)
                if booking:
                    st.session_state.auth = {'user': {'id': booking['id'], 'fullName': booking['guestName']}, 'role': 'GUEST'}
                    st.session_state.active_booking_code = booking['bookingCode']
                    st.rerun()
                else:
                    st.error("Codice non valido.")
            st.markdown("</div>", unsafe_allow_html=True)

        with tab_staff:
            st.markdown('<div class="login-box">', unsafe_allow_html=True)
            st.markdown("### Accesso Riservato")
            email = st.text_input("Email")
            pwd = st.text_input("Password", type="password")
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("LOGIN ADMIN/HOST", use_container_width=True):
                if email == "admin@conciergepro.it" and pwd == "admin123":
                    st.session_state.auth = {'user': {'id': 'admin', 'fullName': 'Super Admin'}, 'role': 'ADMIN'}
                    st.rerun()
                else:
                    user = next((u for u in st.session_state.users if u['email'] == email and u['password'] == pwd and u['role'] == 'HOST'), None)
                    if user:
                        st.session_state.auth = {'user': user, 'role': 'HOST'}
                        st.rerun()
                    else:
                        st.error("Credenziali errate.")
            st.markdown("</div>", unsafe_allow_html=True)

# --- 4. ADMIN PANEL (Con Copertina e Punti Interesse) ---
def view_admin():
    st.sidebar.title("Admin")
    if st.sidebar.button("Logout"): logout()
    page = st.sidebar.radio("Navigazione", ["Immobili & Località", "Gestione Staff"])
    
    st.title("Admin Dashboard")
    st.markdown("---")

    if page == "Immobili & Località":
        # FORM AGGIUNTA
        with st.expander("➕ CREA NUOVO APPARTAMENTO", expanded=False):
            st.markdown('<div class="clean-card">', unsafe_allow_html=True)
            with st.form("add_apt"):
                st.subheader("Dati Principali")
                c1, c2 = st.columns(2)
                name = c1.text_input("Nome Appartamento")
                addr = c2.text_input("Indirizzo")
                
                st.subheader("Media & Contenuti")
                # NUOVO CAMPO COPERTINA
                cover = st.text_input("URL Immagine di Copertina (Link foto)")
                video = st.text_input("Link Video Istruzioni")
                
                st.subheader("Dettagli Tecnici")
                c3, c4 = st.columns(2)
                wifi_n = c3.text_input("WiFi Nome")
                wifi_p = c4.text_input("WiFi Password")
                rules = st.text_area("Regole della Casa")
                
                st.subheader("Assegnazione Host")
                hosts = [u for u in st.session_state.users if u['role'] == 'HOST']
                h_map = {h['fullName']: h['id'] for h in hosts}
                h_sel = st.selectbox("Seleziona Host", list(h_map.keys()) if hosts else [])
                
                if st.form_submit_button("SALVA APPARTAMENTO"):
                    new_id = f"a{len(st.session_state.apartments) + 1}"
                    # Se non mettono foto, usiamo un placeholder elegante
                    final_cover = cover if cover else "https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?auto=format&fit=crop&w=2000&q=80"
                    
                    st.session_state.apartments.append({
                        'id': new_id, 'name': name, 'address': addr, 'coverImage': final_cover,
                        'wifiName': wifi_n, 'wifiPassword': wifi_p, 'videoUrl': video, 
                        'houseRules': rules, 'hostId': h_map.get(h_sel), 
                        'points_of_interest': [] # Lista vuota pronta per Admin
                    })
                    st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("### Lista Immobili")
        for apt in st.session_state.apartments:
            with st.container():
                st.markdown(f"""
                <div class="clean-card" style="border-left: 5px solid #C5A059;">
                    <h3>{apt['name']}</h3>
                    <p>📍 {apt['address']} | 👤 Host: {get_user_name(apt['hostId'])}</p>
                </div>
                """, unsafe_allow_html=True)
                
                c_btn1, c_btn2, c_btn3 = st.columns([1, 1.5, 0.5])
                
                if c_btn1.button("⚙️ MODIFICA DATI", key=f"edit_d_{apt['id']}"):
                    st.session_state.edit_mode_apt_details = apt['id']
                    st.rerun()
                    
                # PULSANTE PUNTI DI INTERESSE (ADMIN ONLY)
                if c_btn2.button("📍 GESTISCI PUNTI DI INTERESSE", key=f"poi_{apt['id']}"):
                    st.session_state.editing_apt_id = apt['id']
                    st.rerun()
                    
                if c_btn3.button("🗑️", key=f"del_{apt['id']}"):
                    st.session_state.apartments.remove(apt)
                    st.rerun()
                
                # --- MODIFICA DATI ---
                if st.session_state.edit_mode_apt_details == apt['id']:
                    st.info(f"Modifica: {apt['name']}")
                    with st.form(f"edit_form_{apt['id']}"):
                        e_n = st.text_input("Nome", apt['name'])
                        e_a = st.text_input("Indirizzo", apt['address'])
                        e_c = st.text_input("URL Copertina", apt.get('coverImage', ''))
                        e_wn = st.text_input("WiFi Nome", apt['wifiName'])
                        e_wp = st.text_input("WiFi Pass", apt['wifiPassword'])
                        e_r = st.text_area("Regole", apt['houseRules'])
                        if st.form_submit_button("AGGIORNA"):
                            apt.update({'name': e_n, 'address': e_a, 'coverImage': e_c, 'wifiName': e_wn, 'wifiPassword': e_wp, 'houseRules': e_r})
                            st.session_state.edit_mode_apt_details = None
                            st.rerun()
                    if st.button("CHIUDI", key=f"close_e_{apt['id']}"):
                        st.session_state.edit_mode_apt_details = None
                        st.rerun()

                # --- GESTIONE PUNTI DI INTERESSE (ADMIN ONLY) ---
                if st.session_state.editing_apt_id == apt['id']:
                    st.markdown('<div class="clean-card" style="background-color: #FFFDF5; border-color: #C5A059;">', unsafe_allow_html=True)
                    st.markdown(f"#### 📍 Località & Punti di Interesse: {apt['name']}")
                    st.caption("Solo l'Admin può aggiungere o rimuovere questi punti.")
                    
                    # Lista esistente
                    current_pois = apt.get('points_of_interest', [])
                    for poi in current_pois:
                        col_text, col_act = st.columns([4, 1])
                        col_text.markdown(f"**{poi['category']}**: {poi['name']}")
                        if col_act.button("Elimina", key=f"del_poi_{poi['id']}"):
                            current_pois.remove(poi)
                            st.rerun()
                    
                    st.markdown("---")
                    st.markdown("**Aggiungi Nuovo Punto**")
                    with st.form(f"new_poi_{apt['id']}"):
                        c_cat, c_nam = st.columns(2)
                        n_cat = c_cat.selectbox("Categoria", ["Ristorante", "Cultura", "Shopping", "Servizi", "Svago"])
                        n_nam = c_nam.text_input("Nome Luogo")
                        n_desc = st.text_area("Descrizione")
                        n_map = st.text_input("Link Google Maps")
                        if st.form_submit_button("AGGIUNGI PUNTO"):
                            new_poi = {'id': f"p{len(current_pois)+99}", 'category': n_cat, 'name': n_nam, 'desc': n_desc, 'map': n_map}
                            current_pois.append(new_poi)
                            apt['points_of_interest'] = current_pois # Assicura salvataggio
                            st.rerun()
                    
                    if st.button("CHIUDI EDITOR", key=f"close_poi_{apt['id']}"):
                        st.session_state.editing_apt_id = None
                        st.rerun()
                    st.markdown("</div>", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)

    elif page == "Gestione Staff":
        with st.expander("➕ AGGIUNGI HOST"):
            with st.form("new_host"):
                n = st.text_input("Nome"); e = st.text_input("Email"); p = st.text_input("Password")
                if st.form_submit_button("CREA"):
                    st.session_state.users.append({'id': f"h{len(st.session_state.users)+1}", 'fullName': n, 'email': e, 'password': p, 'role': 'HOST', 'isContactAvailable': True})
                    st.rerun()
        
        st.markdown("### Elenco Host")
        for h in [u for u in st.session_state.users if u['role'] == 'HOST']:
            st.markdown(f"**{h['fullName']}** ({h['email']})")
            if st.button("🗑️ Rimuovi", key=f"rm_h_{h['id']}"):
                st.session_state.users.remove(h)
                st.rerun()
            st.markdown("---")

# --- 5. HOST VIEW (Semplice, Generazione Codici) ---
def view_host():
    me = st.session_state.auth['user']
    st.sidebar.title("Host")
    st.sidebar.markdown(f"**{me['fullName']}**")
    
    # Toggle Disponibilità
    status = "🟢 DISPONIBILE" if me['isContactAvailable'] else "🔴 NON DISTURBARE"
    if st.sidebar.button(status):
        for u in st.session_state.users:
            if u['id'] == me['id']: u['isContactAvailable'] = not u['isContactAvailable']
        st.rerun()
    if st.sidebar.button("Logout"): logout()
    
    st.title("Gestione Ospiti")
    my_apts = [a for a in st.session_state.apartments if a['hostId'] == me['id']]
    
    if not my_apts: st.warning("Nessun appartamento assegnato."); return

    c1, c2 = st.columns([1, 1])
    with c1:
        st.markdown('<div class="clean-card">', unsafe_allow_html=True)
        st.subheader("Nuovo Ospite")
        with st.form("host_gen"):
            apt_name = st.selectbox("Appartamento", [a['name'] for a in my_apts])
            g_name = st.text_input("Nome Ospite")
            if st.form_submit_button("GENERA CODICE"):
                import random, string
                code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
                apt_id = next(a['id'] for a in my_apts if a['name'] == apt_name)
                st.session_state.bookings.append({
                    'id': f"b{len(st.session_state.bookings)+1}", 'apartmentId': apt_id,
                    'guestName': g_name, 'bookingCode': code, 'checkInDate': str(datetime.date.today()), 'status': 'ACTIVE'
                })
                st.success(f"Codice: {code}")
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
        
    with c2:
        st.markdown('<div class="clean-card">', unsafe_allow_html=True)
        st.subheader("Prenotazioni Attive")
        my_ids = [a['id'] for a in my_apts]
        bs = [b for b in st.session_state.bookings if b['apartmentId'] in my_ids]
        for b in bs:
            st.markdown(f"**{b['guestName']}** | Codice: `{b['bookingCode']}`")
            if st.button("Termina", key=f"end_{b['id']}"):
                st.session_state.bookings.remove(b)
                st.rerun()
            st.markdown("---")
        st.markdown("</div>", unsafe_allow_html=True)

# --- 6. GUEST VIEW (Design Finale con Cover) ---
def view_guest():
    user = st.session_state.auth['user']
    code = st.session_state.get('active_booking_code')
    booking = next((b for b in st.session_state.bookings if b['bookingCode'] == code), None)
    if not booking: logout(); return
    apt = next((a for a in st.session_state.apartments if a['id'] == booking['apartmentId']), None)
    host = next((u for u in st.session_state.users if u['id'] == apt['hostId']), None)

    # --- HERO SECTION (Cover Image) ---
    if apt.get('coverImage'):
        st.image(apt['coverImage'], use_container_width=True)
    
    st.markdown(f"""
    <div style="padding: 20px 0; text-align: center;">
        <h1 style="font-size: 3rem; margin-bottom: 5px;">{apt['name']}</h1>
        <p class="gold-text">BENVENUTO {user['fullName']}</p>
        <p style="color: grey;">{apt['address']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    tabs = st.tabs(["🏠 HOME", "📍 PUNTI DI INTERESSE", "🤖 AI CONCIERGE", "👤 CONTATTI"])
    
    with tabs[0]:
        c1, c2 = st.columns(2)
        with c1:
            st.markdown('<div class="clean-card">', unsafe_allow_html=True)
            st.markdown("### 📶 WiFi")
            st.markdown(f"**Rete:** {apt['wifiName']}")
            st.markdown(f"**Password:** `{apt['wifiPassword']}`")
            st.markdown("</div>", unsafe_allow_html=True)
        with c2:
            st.markdown('<div class="clean-card">', unsafe_allow_html=True)
            st.markdown("### 📜 Regole")
            st.write(apt['houseRules'])
            st.markdown("</div>", unsafe_allow_html=True)
        
        if apt.get('videoUrl'):
            st.markdown("### 🎬 Video Istruzioni")
            st.video(apt['videoUrl'])
            
    with tabs[1]:
        st.markdown("### 📍 Località Selezionate")
        st.caption("I luoghi consigliati per te.")
        
        pois = apt.get('points_of_interest', [])
        if not pois:
            st.info("Nessun punto di interesse segnalato al momento.")
        
        col_a, col_b = st.columns(2)
        for i, poi in enumerate(pois):
            with col_a if i % 2 == 0 else col_b:
                st.markdown(f"""
                <div class="clean-card">
                    <p class="gold-text">{poi['category']}</p>
                    <h3 style="margin-top:0;">{poi['name']}</h3>
                    <p>{poi['desc']}</p>
                    <a href="{poi['map']}" target="_blank" style="color: #C5A059; font-weight: bold; text-decoration: none;">Vedi Mappa →</a>
                </div>
                """, unsafe_allow_html=True)

    with tabs[2]:
        st.markdown("### 🤖 Chiedi ad Hadriano")
        st.caption("Il tuo assistente virtuale personale.")
        
        # Chat Interface
        if "messages" not in st.session_state: st.session_state.messages = []
        
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])
                
        q = st.chat_input("Chiedi qualcosa...")
        if q:
            # User msg
            st.session_state.messages.append({"role": "user", "content": q})
            with st.chat_message("user"): st.write(q)
            
            # AI Reply
            with st.chat_message("assistant"):
                with st.spinner("..."):
                    try:
                        if "GEMINI_API_KEY" in st.secrets:
                            genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
                            model = genai.GenerativeModel('gemini-1.5-flash')
                            # Context robusto
                            ctx = f"""Sei Hadriano, concierge di lusso.
                            Ospite: {user['fullName']}
                            Appartamento: {apt['name']} ({apt['address']})
                            Regole: {apt['houseRules']}
                            Località consigliate: {pois}
                            Host: {host['fullName']}
                            
                            Rispondi in modo breve, utile e cortese."""
                            
                            res = model.generate_content(f"{ctx}\nDomanda: {q}")
                            st.write(res.text)
                            st.session_state.messages.append({"role": "assistant", "content": res.text})
                        else:
                            st.error("Chiave API mancante.")
                    except Exception as e:
                        st.error(f"Errore: {e}")

    with tabs[3]:
        st.markdown('<div class="clean-card" style="text-align: center;">', unsafe_allow_html=True)
        st.markdown(f"### Host: {host['fullName']}")
        if host['isContactAvailable']:
            st.success("✅ DISPONIBILE")
            c_a, c_b = st.columns(2)
            c_a.button("📞 Chiama", use_container_width=True)
            c_b.button("💬 WhatsApp", use_container_width=True)
        else:
            st.error("⛔ NON DISPONIBILE")
            st.caption("Per emergenze chiama il 112")
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br><hr>", unsafe_allow_html=True)
    if st.button("Logout"): logout()

# --- MAIN ---
if st.session_state.auth['user'] is None:
    login_screen()
elif st.session_state.auth['role'] == 'ADMIN':
    view_admin()
elif st.session_state.auth['role'] == 'HOST':
    view_host()
elif st.session_state.auth['role'] == 'GUEST':
    view_guest()
