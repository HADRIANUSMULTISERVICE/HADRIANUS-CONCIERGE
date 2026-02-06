import streamlit as st
import datetime
import pandas as pd
import google.generativeai as genai

# --- 1. CONFIGURAZIONE E CSS "LUXURY REDESIGN" ---
st.set_page_config(page_title="Hadriano Concierge", page_icon="🛎️", layout="wide")

st.markdown("""
    <style>
    /* --- IMPORTAZIONE FONT PREMIUM --- */
    /* Playfair Display per titoli eleganti, Lato per testi leggibili */
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;0,700;1,400&family=Lato:wght@300;400;700&display=swap');
    
    /* --- SFONDO E BASE --- */
    .stApp {
        background-color: #F8F9FA; /* Grigio perla chiarissimo per profondità */
        color: #2C3E50; /* Grigio scuro elegante invece del nero puro */
        font-family: 'Lato', sans-serif;
    }
    
    /* --- TIPOGRAFIA --- */
    h1, h2, h3 {
        font-family: 'Playfair Display', serif;
        color: #1A1A1A;
        letter-spacing: -0.5px;
    }
    h1 { font-size: 3rem; font-weight: 700; }
    h2 { font-size: 2.2rem; }
    h3 { font-size: 1.8rem; }
    
    /* Testo Accento Oro */
    .gold-accent {
        color: #CFB16D; /* Un oro più sofisticato e meno giallo */
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 2px;
        font-size: 11px;
    }

    /* --- INPUT FIELDS (Risolto problema visibilità) --- */
    /* Forza lo stile dei campi di input di Streamlit */
    div[data-baseweb="input"] {
        background-color: #FFFFFF !important;
        border: 1px solid #E0E0E0 !important; /* Bordo grigio chiaro definito */
        border-radius: 12px !important; /* Angoli arrotondati moderni */
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.03) !important; /* Leggera ombreggiatura interna */
        padding: 5px !important;
    }
    div[data-baseweb="select"] > div {
         background-color: #FFFFFF !important;
         border: 1px solid #E0E0E0 !important;
         border-radius: 12px !important;
    }
    /* Etichette dei campi più visibili */
    label p {
        font-weight: 600 !important;
        color: #555 !important;
        font-size: 14px !important;
        margin-bottom: 8px !important;
    }

    /* --- BOTTONI PREMIUM --- */
    .stButton>button {
        background: linear-gradient(135deg, #2C3E50 0%, #1A1A1A 100%); /* Gradiente scuro elegante */
        color: #CFB16D !important; /* Testo oro */
        border: none !important;
        border-radius: 30px !important; /* A pillola */
        padding: 12px 28px !important;
        font-weight: 700 !important;
        letter-spacing: 1px !important;
        text-transform: uppercase !important;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1) !important;
        transition: all 0.3s ease !important;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 15px rgba(207, 177, 109, 0.3) !important; /*alone dorato al passaggio*/
        background: linear-gradient(135deg, #CFB16D 0%, #BFA05D 100%) !important;
        color: white !important;
    }
    /* Bottoni secondari (es. Elimina/Modifica) */
    div[data-testid="column"] .stButton>button {
        background: white !important;
        border: 1px solid #E0E0E0 !important;
        color: #555 !important;
        box-shadow: none !important;
        padding: 8px 16px !important;
        font-size: 10px !important;
    }
     div[data-testid="column"] .stButton>button:hover {
         border-color: #CFB16D !important;
         color: #CFB16D !important;
         background: #FFF !important;
     }

    /* --- "LUXURY CARDS" (Contenitori per Ospite e Admin) --- */
    .luxury-card {
        background: #FFFFFF;
        padding: 35px;
        border-radius: 24px; /* Angoli molto arrotondati */
        /* Ombra morbida e profonda per effetto "sollevato" */
        box-shadow: 0 10px 30px -5px rgba(0,0,0,0.05), 0 4px 10px -5px rgba(0,0,0,0.02);
        border: 1px solid rgba(255,255,255,0.8);
        margin-bottom: 25px;
    }
    .card-icon { font-size: 32px; margin-bottom: 15px; color: #CFB16D; }
    .card-label { font-size: 11px; font-weight: 700; color: #999; text-transform: uppercase; letter-spacing: 1px; display: block; margin-bottom: 5px;}
    .card-value { font-size: 20px; font-family: 'Playfair Display', serif; color: #1A1A1A; font-weight: 600; }
    .card-link { color: #CFB16D; text-decoration: none; font-weight: 700; font-size: 12px; border-bottom: 2px solid rgba(207, 177, 109, 0.2); padding-bottom: 2px; transition: all 0.2s;}
    .card-link:hover { border-bottom-color: #CFB16D; }

    /* --- TABS (Schede di navigazione) --- */
    .stTabs [data-baseweb="tab-list"] {
        border-bottom: none !important;
        gap: 10px;
        margin-bottom: 30px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        border: none !important;
        color: #999;
        font-weight: 600;
        padding: 10px 20px;
        border-radius: 20px;
        transition: all 0.3s;
    }
    .stTabs [aria-selected="true"] {
        background-color: #1A1A1A !important;
        color: #CFB16D !important;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }
    
    /* Separatori */
    hr { border-color: #E0E0E0; opacity: 0.5; margin: 40px 0; }
    </style>
""", unsafe_allow_html=True)

# --- 2. DATABASE SIMULATO (Invariato) ---
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
                'houseRules': '1. Non fumare.\n2. Silenzio dopo le 22:00.',
                'wifiName': 'Boutique_Guest', 'wifiPassword': 'milano-luxury',
                'videoUrl': 'https://www.w3schools.com/html/mov_bbb.mp4',
                'hostId': 'h1',
                'recommendations': [
                    {'id': 'r1', 'name': 'Langosteria', 'category': 'Ristorante', 'desc': 'Miglior pesce di Milano, atmosfera chic.', 'map': 'https://goo.gl/maps'}
                ]
            }
        ]
    
    if 'bookings' not in st.session_state:
        st.session_state.bookings = [
             {'id': 'b0', 'apartmentId': 'a1', 'guestName': 'Ospite Demo', 'bookingCode': 'WELCOME', 'checkInDate': str(datetime.date.today()), 'status': 'ACTIVE'}
        ]
        
    if 'auth' not in st.session_state:
        st.session_state.auth = {'user': None, 'role': None}
        
    if 'editing_apt_id' not in st.session_state: st.session_state.editing_apt_id = None
    if 'editing_host_id' not in st.session_state: st.session_state.editing_host_id = None
    if 'edit_mode_apt_details' not in st.session_state: st.session_state.edit_mode_apt_details = None

init_data()

# --- 3. UTILITIES (Invariato) ---
def get_user_name(user_id):
    user = next((u for u in st.session_state.users if u['id'] == user_id), None)
    return user['fullName'] if user else "Nessuno"

def logout():
    st.session_state.auth = {'user': None, 'role': None}
    st.rerun()

# --- 4. LOGIN SCREEN (Nuovo Look) ---
def login_screen():
    # Usiamo colonne per centrare il contenuto in una "Card"
    c_left, c_center, c_right = st.columns([1, 2, 1])
    with c_center:
        st.markdown("""
        <div class="luxury-card" style="text-align:center; margin-top: 50px;">
            <span style="font-size: 50px;">🛎️</span>
            <h1 style="margin-top: 20px;">Hadriano Concierge</h1>
            <p class="gold-accent" style="margin-bottom: 40px;">Exclusive Digital Services</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Il contenuto dei tab ora è dentro la card "virtualmente" grazie al CSS
        tab_guest, tab_staff = st.tabs(["OSPITE / GUEST", "AREA STAFF"])
        
        with tab_guest:
            st.markdown("<div class="luxury-card">", unsafe_allow_html=True)
            st.markdown("### 🔑 Accesso Suite")
            st.caption("Inserisci il codice di 6 cifre fornito dal tuo Host.")
            code = st.text_input("Codice Prenotazione", placeholder="Es. WELCOME")
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("ENTRA NELLA SUITE", use_container_width=True):
                code = code.upper().strip()
                if code == "WELCOME": 
                    demo_exists = next((b for b in st.session_state.bookings if b['bookingCode'] == 'WELCOME'), None)
                    if not demo_exists:
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
                    st.error("Codice non trovato. Riprova.")
            st.markdown("</div>", unsafe_allow_html=True)

        with tab_staff:
            st.markdown("<div class="luxury-card">", unsafe_allow_html=True)
            st.markdown("### 🔒 Accesso Riservato")
            email = st.text_input("Email Aziendale")
            pwd = st.text_input("Password Sicurezza", type="password")
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("LOGIN STAFF", use_container_width=True):
                if email == "admin@conciergepro.it" and pwd == "admin123":
                    st.session_state.auth = {'user': {'id': 'admin', 'fullName': 'Super Admin'}, 'role': 'ADMIN'}
                    st.rerun()
                else:
                    user = next((u for u in st.session_state.users if u['email'] == email and u['password'] == pwd and u['role'] == 'HOST'), None)
                    if user:
                        st.session_state.auth = {'user': user, 'role': 'HOST'}
                        st.rerun()
                    else:
                        st.error("Credenziali non valide.")
            st.markdown("</div>", unsafe_allow_html=True)

# --- 5. ADMIN PANEL (Logica Invariata, Stile Applicato) ---
def view_admin():
    st.sidebar.title("Admin Portal")
    st.sidebar.markdown(f"Bentornato, **{st.session_state.auth['user']['fullName']}**")
    if st.sidebar.button("Esci / Logout"): logout()
    
    page = st.sidebar.radio("Menu Navigazione", ["Gestione Immobili", "Gestione Host & Staff"])
    
    st.title("Admin Dashboard")
    st.markdown("<p class='gold-accent'>PANNELLO DI CONTROLLO GLOBALE</p>", unsafe_allow_html=True)
    st.markdown("---")

    if page == "Gestione Immobili":
        # --- AGGIUNTA (Chiusa in un expander pulito) ---
        with st.expander("➕ AGGIUNGI NUOVO APPARTAMENTO", expanded=False):
            st.markdown("<div class='luxury-card'>", unsafe_allow_html=True)
            with st.form("add_apt"):
                st.subheader("Dati Immobile")
                c1, c2 = st.columns(2)
                name = c1.text_input("Nome Commerciale (Es. Brera Design Suite)")
                addr = c2.text_input("Indirizzo Completo")
                
                st.subheader("Configurazione Ospiti")
                c3, c4 = st.columns(2)
                wifi_n = c3.text_input("Nome Rete WiFi (SSID)")
                wifi_p = c4.text_input("Password WiFi")
                video = st.text_input("Link Video Istruzioni (YouTube/Vimeo)")
                rules = st.text_area("Regole della Casa (Markdown supportato)")
                
                st.subheader("Assegnazione")
                hosts = [u for u in st.session_state.users if u['role'] == 'HOST']
                h_map = {h['fullName']: h['id'] for h in hosts}
                h_sel = st.selectbox("Seleziona Property Manager (Host)", list(h_map.keys()) if hosts else [])
                
                st.markdown("<br>", unsafe_allow_html=True)
                if st.form_submit_button("SALVA E PUBBLICA IMMOBILE"):
                    new_id = f"a{len(st.session_state.apartments) + 1}"
                    st.session_state.apartments.append({
                        'id': new_id, 'name': name, 'address': addr, 'wifiName': wifi_n, 'wifiPassword': wifi_p,
                        'videoUrl': video, 'houseRules': rules, 'hostId': h_map.get(h_sel), 'recommendations': []
                    })
                    st.success("Appartamento creato con successo!")
                    st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

        st.divider()
        st.subheader(f"Portfolio Immobili ({len(st.session_state.apartments)})")
        
        # --- LISTA IMMOBILI (Usa le "Luxury Cards") ---
        for apt in st.session_state.apartments:
            # Container esterno per la card
            with st.container():
                # Header della card
                c_info, c_actions = st.columns([3, 2])
                with c_info:
                     st.markdown(f"""
                     <div style="padding: 20px; border-left: 4px solid #CFB16D; background: white; border-radius: 0 12px 12px 0;">
                        <h3 style="margin:0">{apt['name']}</h3>
                        <p style="color:#777; margin: 5px 0;">📍 {apt['address']}</p>
                        <p class="gold-accent">Managed by: {get_user_name(apt['hostId'])}</p>
                     </div>
                     """, unsafe_allow_html=True)

                with c_actions:
                    # Bottoni di azione allineati a destra
                    st.markdown("<div style='text-align:right; padding-top: 20px;'>", unsafe_allow_html=True)
                    ac1, ac2, ac3 = st.columns(3)
                    if ac1.button("⚙️ DATI", key=f"ed_{apt['id']}"):
                        st.session_state.edit_mode_apt_details = apt['id']
                        st.rerun()
                    if ac2.button("📂 GUIDA", key=f"guide_{apt['id']}"):
                        st.session_state.editing_apt_id = apt['id']
                        st.rerun()
                    if ac3.button("🗑️ ELIMINA", key=f"del_apt_{apt['id']}"):
                         st.session_state.apartments.remove(apt)
                         st.rerun()
                    st.markdown("</div>", unsafe_allow_html=True)

                # --- SEZIONE MODIFICA DETTAGLI (Compare sotto se attiva) ---
                if st.session_state.edit_mode_apt_details == apt['id']:
                    st.markdown("<div class='luxury-card' style='background:#F4F4F4; margin-top:20px;'>", unsafe_allow_html=True)
                    st.info(f"✏️ Modifica Dati: {apt['name']}")
                    with st.form(f"edit_form_{apt['id']}"):
                        e_name = st.text_input("Nome", value=apt['name'])
                        e_addr = st.text_input("Indirizzo", value=apt['address'])
                        e_wifi_n = st.text_input("WiFi Name", value=apt['wifiName'])
                        e_wifi_p = st.text_input("WiFi Pass", value=apt['wifiPassword'])
                        e_rules = st.text_area("Regole", value=apt['houseRules'])
                        if st.form_submit_button("SALVA MODIFICHE"):
                            apt['name'] = e_name; apt['address'] = e_addr; apt['wifiName'] = e_wifi_n; apt['wifiPassword'] = e_wifi_p; apt['houseRules'] = e_rules
                            st.session_state.edit_mode_apt_details = None
                            st.rerun()
                    if st.button("CHIUDI", key=f"canc_ed_{apt['id']}"):
                        st.session_state.edit_mode_apt_details = None
                        st.rerun()
                    st.markdown("</div>", unsafe_allow_html=True)

                # --- SEZIONE MODIFICA GUIDA (Compare sotto se attiva) ---
                if st.session_state.editing_apt_id == apt['id']:
                    st.markdown("<div class='luxury-card' style='background:#FFF8E1; margin-top:20px; border-color:#CFB16D;'>", unsafe_allow_html=True)
                    st.warning(f"📂 Gestione Guida Digitale per: **{apt['name']}**")
                    
                    # Tabella esistente stilizzata
                    if apt['recommendations']:
                        for rec in apt['recommendations']:
                            st.markdown(f"""
                            <div style="display:flex; justify-content:space-between; align-items:center; padding: 15px; background:white; border-radius:12px; margin-bottom:10px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
                                <div><span class="gold-accent">{rec['category']}</span><br><b>{rec['name']}</b></div>
                                <div></div>
                            </div>
                            """, unsafe_allow_html=True)
                            # Bottone elimina separato per farlo funzionare in Streamlit
                            if st.button("Elimina Consiglio", key=f"del_rec_{rec['id']}"):
                                apt['recommendations'].remove(rec)
                                st.rerun()
                    
                    st.divider()
                    # Form Aggiunta
                    st.markdown("#### Aggiungi Nuovo Punto di Interesse")
                    with st.form(f"new_rec_{apt['id']}"):
                        c_cat, c_nam = st.columns(2)
                        n_cat = c_cat.selectbox("Categoria", ["Ristorante", "Bar & Nightlife", "Supermarket & Essentials", "Farmacia", "Cultura & Musei", "Shopping", "Trasporti"])
                        n_nam = c_nam.text_input("Nome del Luogo")
                        n_desc = st.text_area("Descrizione Curata (Perché consigliarlo?)")
                        n_map = st.text_input("Link Google Maps (URL)")
                        if st.form_submit_button("AGGIUNGI ALLA GUIDA OSPITI"):
                            apt['recommendations'].append({'id': f"r{len(apt['recommendations'])+99}", 'category': n_cat, 'name': n_nam, 'desc': n_desc, 'map': n_map})
                            st.rerun()
                    
                    if st.button("CHIUDI EDITOR GUIDA", key=f"close_g_{apt['id']}"):
                        st.session_state.editing_apt_id = None
                        st.rerun()
                    st.markdown("</div>", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)

    elif page == "Host & Staff":
        # (Codice Host & Staff invariato nella logica, eredita il nuovo stile CSS)
        with st.expander("➕ REGISTRA NUOVO HOST / MANAGER"):
            st.markdown("<div class='luxury-card'>", unsafe_allow_html=True)
            with st.form("add_host"):
                c1, c2 = st.columns(2)
                h_name = c1.text_input("Nome e Cognome")
                h_email = c2.text_input("Email Aziendale")
                h_pass = st.text_input("Password Provvisoria")
                if st.form_submit_button("CREA ACCOUNT HOST"):
                    st.session_state.users.append({'id': f"h{len(st.session_state.users)+1}", 'fullName': h_name, 'email': h_email, 'password': h_pass, 'role': 'HOST', 'isContactAvailable': True})
                    st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
        
        st.subheader("Team & Staff")
        hosts = [u for u in st.session_state.users if u['role'] == 'HOST']
        for h in hosts:
            with st.markdown("<div class='luxury-card' style='padding: 20px;'>", unsafe_allow_html=True):
                c1, c2, c3, c4 = st.columns([2, 2, 1, 1])
                c1.markdown(f"**{h['fullName']}**")
                c2.caption(h['email'])
                if c3.button("Modifica", key=f"mod_h_{h['id']}"): st.session_state.editing_host_id = h['id']
                if c4.button("🗑️ Elimina", key=f"del_h_{h['id']}"): st.session_state.users.remove(h); st.rerun()
            
            if st.session_state.editing_host_id == h['id']:
                 with st.form(f"edit_h_{h['id']}"):
                     nn=st.text_input("N",h['fullName']); ne=st.text_input("E",h['email']); np=st.text_input("P",h['password'])
                     if st.form_submit_button("Salva"): h['fullName']=nn; h['email']=ne; h['password']=np; st.session_state.editing_host_id=None; st.rerun()
            st.markdown("</div><br>", unsafe_allow_html=True)

# --- 6. HOST VIEW (Logica Invariata, Stile Applicato) ---
def view_host():
    me = st.session_state.auth['user']
    st.sidebar.title("Host Portal")
    st.sidebar.write(f"Account: **{me['fullName']}**")
    st.sidebar.markdown("---")
    # Toggle Disponibilità
    st.sidebar.write("Tuo Stato Attuale:")
    status_color = "green" if me['isContactAvailable'] else "red"
    status_text = "🟢 DISPONIBILE OSPITI" if me['isContactAvailable'] else "🔴 NON DISTURBARE"
    if st.sidebar.button(status_text, use_container_width=True):
        for u in st.session_state.users:
            if u['id'] == me['id']: u['isContactAvailable'] = not u['isContactAvailable']
        st.rerun()
    st.sidebar.caption("Clicca sopra per cambiare la tua visibilità agli ospiti.")
    st.sidebar.markdown("---")
    if st.sidebar.button("Esci"): logout()
    
    st.title("Gestione Operativa")
    st.markdown("<p class='gold-accent'>CONTROL ROOM</p>", unsafe_allow_html=True)

    my_apts = [a for a in st.session_state.apartments if a['hostId'] == me['id']]
    if not my_apts: st.warning("Non hai appartamenti assegnati. Contatta l'Admin."); return

    c_gen, c_list = st.columns([2, 3])

    with c_gen:
        st.markdown("<div class='luxury-card'>", unsafe_allow_html=True)
        st.subheader("🔑 Nuovo Check-in")
        with st.form("new_code"):
            sel_apt = st.selectbox("Seleziona Appartamento", [a['name'] for a in my_apts])
            g_name = st.text_input("Nome e Cognome Ospite")
            st.markdown("<br>", unsafe_allow_html=True)
            if st.form_submit_button("GENERA CODICE D'ACCESSO"):
                import random, string
                code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
                apt_id = next(a['id'] for a in my_apts if a['name'] == sel_apt)
                st.session_state.bookings.append({
                    'id': f"b{len(st.session_state.bookings)+1}", 'apartmentId': apt_id,
                    'guestName': g_name, 'bookingCode': code, 'checkInDate': str(datetime.date.today()), 'status': 'ACTIVE'
                })
                st.success(f"Codice Generato: {code}")
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    with c_list:
        st.subheader("Prenotazioni Attive")
        my_ids = [a['id'] for a in my_apts]
        bookings = [b for b in st.session_state.bookings if b['apartmentId'] in my_ids]
        if not bookings: st.info("Nessuna prenotazione attiva al momento.")
        for b in bookings:
            apt_name = next(a['name'] for a in st.session_state.apartments if a['id'] == b['apartmentId'])
            st.markdown(f"""
            <div class="luxury-card" style="padding: 20px; border-left: 5px solid #1A1A1A; display:flex; justify-content:space-between; align-items:center;">
                <div>
                    <h3 style="margin:0; color:#CFB16D;">{b['bookingCode']}</h3>
                    <p style="margin:5px 0; font-weight:bold;">{b['guestName']}</p>
                    <p class="gold-accent">{apt_name}</p>
                    <span style="font-size:10px; color:#999;">Check-in: {b['checkInDate']}</span>
                </div>
                <div></div>
            </div>
            """, unsafe_allow_html=True)
            # Bottone fuori dall'HTML per funzionare
            if st.button(f"Termina Soggiorno ({b['bookingCode']})", key=b['id']):
                st.session_state.bookings.remove(b); st.rerun()

# --- 7. GUEST VIEW (REVISIONE DESIGN LUSSO COMPLETA) ---
def view_guest():
    user = st.session_state.auth['user']
    code = st.session_state.get('active_booking_code')
    booking = next((b for b in st.session_state.bookings if b['bookingCode'] == code), None)
    if not booking: logout(); return
    apt = next((a for a in st.session_state.apartments if a['id'] == booking['apartmentId']), None)
    host = next((u for u in st.session_state.users if u['id'] == apt['hostId']), None)

    # --- HEADER ---
    st.markdown(f"""
    <div style="text-align: center; padding: 60px 20px; background: linear-gradient(to bottom, #F8F9FA, #FFF);">
        <p class="gold-accent">BENVENUTO A MILANO</p>
        <h1 style="font-size: 3.5rem; margin: 10px 0;">{apt['name']}</h1>
        <p style="font-size: 1.2rem; color: #777; font-family:'Playfair Display', serif; font-style:italic;">Curated for {user['fullName']}</p>
    </div>
    """, unsafe_allow_html=True)

    # --- NAVIGAZIONE ---
    tabs = st.tabs(["🏠 LA TUA SUITE", "🗺️ GUIDA LOCAL", "🤖 CONCIERGE AI", "👤 ASSISTENZA"])

    with tabs[0]: # HOME
        c1, c2 = st.columns([1, 1], gap="large")
        with c1:
            # Card Posizione
            st.markdown(f"""
            <div class="luxury-card">
                <div class="card-icon">📍</div>
                <span class="card-label">Posizione</span>
                <p class="card-value" style="font-size:18px;">{apt['address']}</p>
                <a href="https://maps.google.com/?q={apt['address']}" target="_blank" class="card-link">Vedi sulla Mappa →</a>
            </div>
            """, unsafe_allow_html=True)
            
            # Card WiFi
            st.markdown(f"""
            <div class="luxury-card" style="background-color: #1A1A1A; color: white;">
                <div class="card-icon" style="color:white;">📶</div>
                <span class="card-label" style="color:#999;">High-Speed Internet</span>
                <h3 style="color:white; margin-bottom:5px;">WiFi Access</h3>
                <p style="margin:0;"><span class="gold-accent">RETE:</span> {apt['wifiName']}</p>
                <p style="margin:0;"><span class="gold-accent">PASS:</span> <span style="font-family:monospace; font-size:1.2rem;">{apt['wifiPassword']}</span></p>
            </div>
            """, unsafe_allow_html=True)

        with c2:
             # Card Regole
            st.markdown("""<div class="luxury-card"><div class="card-icon">📜</div><span class="card-label">House Rules & Info</span>""", unsafe_allow_html=True)
            st.info(apt['houseRules'], icon="ℹ️")
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Card Video
            if apt.get('videoUrl'):
                st.markdown("""<div class="luxury-card"><div class="card-icon">🎬</div><span class="card-label">Istruzioni di Accesso</span><h3 style="margin-top:0;">Video Guida</h3>""", unsafe_allow_html=True)
                st.video(apt['videoUrl'])
                st.markdown("</div>", unsafe_allow_html=True)

    with tabs[1]: # GUIDA
        st.markdown("<div style='text-align:center; margin-bottom:40px;'><h2 style='margin-bottom:10px;'>La Selezione dell'Host</h2><p>I migliori indirizzi della zona, scelti per te.</p></div>", unsafe_allow_html=True)
        
        if not apt['recommendations']:
            st.info("Il tuo Host sta ancora curando la selezione per questa zona. Torna presto!")
        
        col_a, col_b = st.columns(2, gap="medium")
        for i, rec in enumerate(apt['recommendations']):
            with col_a if i % 2 == 0 else col_b:
                st.markdown(f"""
                <div class="luxury-card" style="padding: 30px;">
                    <p class="gold-accent" style="margin-bottom:5px;">{rec['category']}</p>
                    <h3 style="margin-top:0; font-size:1.5rem;">{rec['name']}</h3>
                    <p style="color:#555; line-height:1.6;">{rec['desc']}</p>
                    <a href="{rec.get('map', '#')}" target="_blank" class="card-link">NAVIGA QUI →</a>
                </div>
                """, unsafe_allow_html=True)

    with tabs[2]: # AI
        c_ai_intro, c_ai_chat = st.columns([2, 3])
        with c_ai_intro:
             st.markdown("""
             <div class="luxury-card" style="background:#CFB16D; color:white;">
                <div style="font-size:40px;">🤖</div>
                <h2 style="color:white;">Hadriano AI</h2>
                <p>Il tuo concierge digitale personale, attivo 24/7.</p>
                <p style="font-size:14px; opacity:0.8;">Conosce i dettagli di questo appartamento e può darti consigli su misura su Milano.</p>
             </div>
             """, unsafe_allow_html=True)
        
        with c_ai_chat:
            st.markdown("### Come posso aiutarti oggi?")
            q = st.chat_input("Es: Dove posso trovare una farmacia aperta?")
            if q:
                with st.spinner("Hadriano sta elaborando..."):
                    try:
                        if "GEMINI_API_KEY" in st.secrets:
                            genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
                            model = genai.GenerativeModel('gemini-1.5-flash')
                            ctx = f"Sei Hadriano, un concierge di lusso sofisticato ed educato. L'ospite {user['fullName']} si trova nell'appartamento '{apt['name']}' in {apt['address']}. Le regole della casa sono: {apt['houseRules']}. I consigli locali dell'host sono: {apt['recommendations']}. Rispondi in modo breve, utile ed elegante."
                            res = model.generate_content(f"{ctx} Domanda dell'ospite: {q}")
                            st.markdown(f"""
                            <div class="luxury-card" style="background:#FAFAFA; border-left: 4px solid #CFB16D;">
                                <p class="gold-accent">HADRIANO RISPONDE:</p>
                                <p style="font-family:'Playfair Display', serif; font-size:1.1rem; color:#1A1A1A;">{res.text}</p>
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.error("⚠️ Chiave AI non configurata nei Secrets.")
                    except:
                        st.error("Servizio momentaneamente non disponibile.")

    with tabs[3]: # CONTATTI
        st.markdown("""<div style='text-align:center; margin-bottom:30px;'><h2>Supporto & Assistenza</h2></div>""", unsafe_allow_html=True)
        c1, c2 = st.columns([1, 2])
        with c1:
             st.markdown(f"""
             <div class="luxury-card" style="text-align:center;">
                 <div style="font-size:60px; margin-bottom:20px;">👤</div>
                 <span class="card-label">Il tuo Host</span>
                 <h3>{host['fullName']}</h3>
             </div>
             """, unsafe_allow_html=True)
        with c2:
            st.markdown(f"""<div class="luxury-card"><h3>Stato Disponibilità</h3>""", unsafe_allow_html=True)
            if host['isContactAvailable']:
                st.success(f"✅ **{host['fullName']} è attualmente DISPONIBILE** per assistenza.")
                st.markdown("<p>Puoi utilizzare i canali diretti qui sotto per richieste urgenti.</p>", unsafe_allow_html=True)
                bc1, bc2 = st.columns(2)
                bc1.button("📞 Chiama Ora", use_container_width=True)
                bc2.button("💬 Apri WhatsApp", use_container_width=True)
            else:
                st.error(f"⛔ **{host['fullName']} non è al momento disturbabile.**")
                st.markdown("<p style='color:#777;'>Per favore, riprova più tardi o consulta la guida.</p>", unsafe_allow_html=True)
                st.warning("Per emergenze gravi (sanitarie o di pubblica sicurezza), chiama sempre il **112**.")
            st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("<div style='text-align:center;'><small>© 2026 Hadriano Concierge Services. All rights reserved.</small></div>", unsafe_allow_html=True)
    c_out1, c_out2, c_out3 = st.columns([1,1,1])
    with c_out2:
        if st.button("🔒 Esci dalla Suite (Logout)", use_container_width=True): logout()

# --- MAIN ROUTER ---
if st.session_state.auth['user'] is None:
    login_screen()
elif st.session_state.auth['role'] == 'ADMIN':
    view_admin()
elif st.session_state.auth['role'] == 'HOST':
    view_host()
elif st.session_state.auth['role'] == 'GUEST':
    view_guest()
