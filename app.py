import streamlit as st
import datetime
import pandas as pd
import google.generativeai as genai

# --- 1. CONFIGURAZIONE E STILE (FIX VISIBILITÀ + LUSSO) ---
st.set_page_config(page_title="Hadriano Concierge", page_icon="🛎️", layout="wide")

st.markdown("""
    <style>
    /* FONT LUSSO */
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;0,800;1,400&family=Lato:wght@300;400;700&display=swap');
    
    /* SFONDO GENERALE */
    .stApp { background-color: #FAFAFA; color: #1A1A1A; }
    
    /* TITOLI */
    h1, h2, h3 { font-family: 'Playfair Display', serif; color: #111; }
    h4, h5, h6 { font-family: 'Lato', sans-serif; font-weight: 700; letter-spacing: 1px; text-transform: uppercase; }
    
    /* --- FIX IMPORTANTE: CAMPI DI INPUT VISIBILI --- */
    /* Questo forza i campi di testo ad avere un bordo e uno sfondo visibile */
    div[data-baseweb="input"] > div {
        background-color: #FFFFFF !important;
        border: 1px solid #B0B0B0 !important;
        border-radius: 8px !important;
        color: #000 !important;
    }
    /* Colore del testo dentro gli input */
    input { color: black !important; }
    /* Etichette sopra gli input */
    label p { font-weight: bold !important; color: #333 !important; font-size: 14px !important; }

    /* --- STILE OSPITE (LUXURY CARDS) --- */
    .guest-card {
        background: white;
        padding: 25px;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        border: 1px solid #EAEAEA;
        margin-bottom: 20px;
        text-align: center;
    }
    .guest-title { font-family: 'Playfair Display', serif; font-size: 22px; color: #111; margin-bottom: 10px; }
    .guest-data { font-family: 'Lato', sans-serif; font-size: 18px; color: #555; }
    .guest-gold { color: #D4AF37; font-weight: bold; letter-spacing: 1px; font-size: 12px; text-transform: uppercase; }
    .guest-icon { font-size: 30px; margin-bottom: 10px; color: #D4AF37; }

    /* BOTTONI */
    .stButton>button {
        border-radius: 8px;
        font-weight: bold;
        text-transform: uppercase;
        border: 1px solid #D4AF37;
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. DATABASE SIMULATO ---
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
                'houseRules': '1. No smoking inside.\n2. Silence after 10PM.',
                'wifiName': 'Boutique_Guest', 'wifiPassword': 'milano-luxury',
                'videoUrl': 'https://www.w3schools.com/html/mov_bbb.mp4',
                'hostId': 'h1',
                'recommendations': [
                    {'id': 'r1', 'name': 'Langosteria', 'category': 'Ristorante', 'desc': 'Best seafood in Milan.', 'map': 'https://goo.gl/maps'}
                ]
            }
        ]
    
    if 'bookings' not in st.session_state:
        st.session_state.bookings = [
             {'id': 'b0', 'apartmentId': 'a1', 'guestName': 'Ospite Demo', 'bookingCode': 'WELCOME', 'checkInDate': str(datetime.date.today()), 'status': 'ACTIVE'}
        ]
        
    if 'auth' not in st.session_state:
        st.session_state.auth = {'user': None, 'role': None}
        
    # Stati per Modifica
    if 'editing_apt_id' not in st.session_state: st.session_state.editing_apt_id = None
    if 'editing_host_id' not in st.session_state: st.session_state.editing_host_id = None
    if 'edit_mode_apt_details' not in st.session_state: st.session_state.edit_mode_apt_details = None

init_data()

# --- 3. UTILITIES ---
def get_user_name(user_id):
    user = next((u for u in st.session_state.users if u['id'] == user_id), None)
    return user['fullName'] if user else "Nessuno"

def logout():
    st.session_state.auth = {'user': None, 'role': None}
    st.rerun()

# --- 4. LOGIN ---
def login_screen():
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        st.markdown("<div style='text-align: center; margin-top: 50px;'>", unsafe_allow_html=True)
        st.title("Hadriano Concierge")
        st.markdown("<p style='color:#D4AF37; font-weight:bold; letter-spacing:2px;'>PREMIUM ACCESS</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        tab_guest, tab_staff = st.tabs(["OSPITE / GUEST", "STAFF ONLY"])
        
        with tab_guest:
            st.info("Inserisci il codice ricevuto dal tuo Host.")
            code = st.text_input("Codice Prenotazione", placeholder="Es. WELCOME")
            if st.button("ENTRA NELLA SUITE", use_container_width=True):
                code = code.upper().strip()
                # Demo Check
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
                    st.error("Codice non trovato.")

        with tab_staff:
            email = st.text_input("Email Aziendale")
            pwd = st.text_input("Password Sicurezza", type="password")
            if st.button("ACCESSO STAFF", use_container_width=True):
                if email == "admin@conciergepro.it" and pwd == "admin123":
                    st.session_state.auth = {'user': {'id': 'admin', 'fullName': 'Super Admin'}, 'role': 'ADMIN'}
                    st.rerun()
                else:
                    user = next((u for u in st.session_state.users if u['email'] == email and u['password'] == pwd and u['role'] == 'HOST'), None)
                    if user:
                        st.session_state.auth = {'user': user, 'role': 'HOST'}
                        st.rerun()
                    else:
                        st.error("Accesso Negato.")

# --- 5. ADMIN PANEL (FIX: Modifica/Elimina + Contrasto) ---
def view_admin():
    st.sidebar.title("Admin")
    if st.sidebar.button("Esci"): logout()
    page = st.sidebar.radio("Menu", ["Appartamenti", "Host & Staff"])
    
    st.title("Admin Dashboard")

    if page == "Appartamenti":
        # --- AGGIUNTA ---
        with st.expander("➕ AGGIUNGI NUOVO APPARTAMENTO", expanded=False):
            with st.form("add_apt"):
                st.markdown("#### Dati Immobile")
                c1, c2 = st.columns(2)
                name = c1.text_input("Nome Appartamento (Es. Brera Suite)")
                addr = c2.text_input("Indirizzo Completo")
                wifi_n = c1.text_input("Nome Rete WiFi")
                wifi_p = c2.text_input("Password WiFi")
                video = st.text_input("Link Video YouTube/Drive")
                rules = st.text_area("Regole della Casa")
                
                hosts = [u for u in st.session_state.users if u['role'] == 'HOST']
                h_map = {h['fullName']: h['id'] for h in hosts}
                h_sel = st.selectbox("Assegna a Host", list(h_map.keys()) if hosts else [])
                
                if st.form_submit_button("SALVA APPARTAMENTO"):
                    new_id = f"a{len(st.session_state.apartments) + 1}"
                    st.session_state.apartments.append({
                        'id': new_id, 'name': name, 'address': addr, 'wifiName': wifi_n, 'wifiPassword': wifi_p,
                        'videoUrl': video, 'houseRules': rules, 'hostId': h_map.get(h_sel), 'recommendations': []
                    })
                    st.success("Appartamento creato!")
                    st.rerun()

        st.divider()
        st.subheader("Gestione Immobili Esistenti")
        
        # --- LISTA E MODIFICA ---
        for apt in st.session_state.apartments:
            with st.container():
                # Visualizzazione "chiusa"
                c1, c2, c3, c4 = st.columns([3, 1, 1, 0.5])
                c1.markdown(f"### {apt['name']}")
                c1.caption(f"{apt['address']} • Host: {get_user_name(apt['hostId'])}")
                
                # Bottoni Azione
                if c2.button("✏️ DETTAGLI", key=f"ed_{apt['id']}"):
                    st.session_state.edit_mode_apt_details = apt['id']
                    st.rerun()
                    
                if c3.button("📂 GUIDA", key=f"guide_{apt['id']}"):
                    st.session_state.editing_apt_id = apt['id']
                    st.rerun()
                    
                if c4.button("🗑️", key=f"del_apt_{apt['id']}"):
                    st.session_state.apartments.remove(apt)
                    st.rerun()
                
                # --- MODIFICA DETTAGLI ---
                if st.session_state.edit_mode_apt_details == apt['id']:
                    st.info(f"Modifica Dati: {apt['name']}")
                    with st.form(f"edit_form_{apt['id']}"):
                        e_name = st.text_input("Nome", value=apt['name'])
                        e_addr = st.text_input("Indirizzo", value=apt['address'])
                        e_wifi_n = st.text_input("WiFi Name", value=apt['wifiName'])
                        e_wifi_p = st.text_input("WiFi Pass", value=apt['wifiPassword'])
                        e_rules = st.text_area("Regole", value=apt['houseRules'])
                        if st.form_submit_button("SALVA MODIFICHE"):
                            apt['name'] = e_name
                            apt['address'] = e_addr
                            apt['wifiName'] = e_wifi_n
                            apt['wifiPassword'] = e_wifi_p
                            apt['houseRules'] = e_rules
                            st.session_state.edit_mode_apt_details = None
                            st.rerun()
                    if st.button("ANNULLA", key=f"canc_ed_{apt['id']}"):
                        st.session_state.edit_mode_apt_details = None
                        st.rerun()

                # --- MODIFICA GUIDA (ALBUM) ---
                if st.session_state.editing_apt_id == apt['id']:
                    st.warning(f"Modifica Guida Ospiti per: {apt['name']}")
                    # Tabella esistente
                    if apt['recommendations']:
                        for rec in apt['recommendations']:
                            rc1, rc2 = st.columns([4, 1])
                            rc1.write(f"**{rec['category']}**: {rec['name']}")
                            if rc2.button("Elimina", key=f"del_rec_{rec['id']}"):
                                apt['recommendations'].remove(rec)
                                st.rerun()
                    
                    # Aggiungi nuovo
                    with st.form(f"new_rec_{apt['id']}"):
                        c_cat, c_nam = st.columns(2)
                        n_cat = c_cat.selectbox("Categoria", ["Ristorante", "Bar", "Supermarket", "Farmacia", "Svago"])
                        n_nam = c_nam.text_input("Nome Luogo")
                        n_desc = st.text_area("Descrizione")
                        n_map = st.text_input("Link Google Maps")
                        if st.form_submit_button("AGGIUNGI CONSIGLIO"):
                            apt['recommendations'].append({
                                'id': f"r{len(apt['recommendations'])+9}",
                                'category': n_cat, 'name': n_nam, 'desc': n_desc, 'map': n_map
                            })
                            st.rerun()
                    
                    if st.button("CHIUDI GUIDA", key=f"close_g_{apt['id']}"):
                        st.session_state.editing_apt_id = None
                        st.rerun()
                
            st.markdown("---")

    elif page == "Host & Staff":
        # --- AGGIUNTA HOST ---
        with st.expander("➕ REGISTRA NUOVO HOST"):
            with st.form("add_host"):
                c1, c2 = st.columns(2)
                h_name = c1.text_input("Nome e Cognome")
                h_email = c2.text_input("Email")
                h_pass = st.text_input("Password")
                if st.form_submit_button("CREA HOST"):
                    st.session_state.users.append({
                        'id': f"h{len(st.session_state.users)+1}", 'fullName': h_name, 
                        'email': h_email, 'password': h_pass, 'role': 'HOST', 'isContactAvailable': True
                    })
                    st.rerun()
        
        st.subheader("Elenco Staff")
        # Tabella con Azioni
        hosts = [u for u in st.session_state.users if u['role'] == 'HOST']
        for h in hosts:
            c1, c2, c3, c4 = st.columns([2, 2, 1, 0.5])
            c1.write(f"**{h['fullName']}**")
            c2.caption(h['email'])
            
            # Modifica Host
            if c3.button("Modifica", key=f"mod_h_{h['id']}"):
                st.session_state.editing_host_id = h['id']
            
            # Elimina Host
            if c4.button("🗑️", key=f"del_h_{h['id']}"):
                st.session_state.users.remove(h)
                st.rerun()
            
            # Form Modifica
            if st.session_state.editing_host_id == h['id']:
                with st.form(f"edit_h_form_{h['id']}"):
                    new_n = st.text_input("Nome", value=h['fullName'])
                    new_e = st.text_input("Email", value=h['email'])
                    new_p = st.text_input("Password", value=h['password'])
                    if st.form_submit_button("SALVA"):
                        h['fullName'] = new_n
                        h['email'] = new_e
                        h['password'] = new_p
                        st.session_state.editing_host_id = None
                        st.rerun()
            st.markdown("---")

# --- 6. HOST VIEW (INVARIATO COME RICHIESTO) ---
def view_host():
    me = st.session_state.auth['user']
    st.sidebar.title(f"Host: {me['fullName']}")
    if st.sidebar.button("Logout"): logout()
    
    st.title("Gestione Prenotazioni")
    
    my_apts = [a for a in st.session_state.apartments if a['hostId'] == me['id']]
    if not my_apts: st.warning("Nessun appartamento assegnato."); return

    with st.form("new_code"):
        st.markdown("#### Crea Codice Ospite")
        sel_apt = st.selectbox("Appartamento", [a['name'] for a in my_apts])
        g_name = st.text_input("Nome Ospite")
        if st.form_submit_button("GENERA CODICE"):
            import random, string
            code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
            apt_id = next(a['id'] for a in my_apts if a['name'] == sel_apt)
            st.session_state.bookings.append({
                'id': f"b{len(st.session_state.bookings)+1}", 'apartmentId': apt_id,
                'guestName': g_name, 'bookingCode': code, 'checkInDate': str(datetime.date.today()), 'status': 'ACTIVE'
            })
            st.success(f"Codice: {code}")
            st.rerun()
    
    st.divider()
    st.write("Prenotazioni Attive:")
    my_ids = [a['id'] for a in my_apts]
    bookings = [b for b in st.session_state.bookings if b['apartmentId'] in my_ids]
    for b in bookings:
        st.info(f"Ospite: {b['guestName']} | Codice: **{b['bookingCode']}**")
        if st.button(f"Cancella {b['bookingCode']}", key=b['id']):
            st.session_state.bookings.remove(b)
            st.rerun()

# --- 7. GUEST VIEW (NUOVO DESIGN LUSSO) ---
def view_guest():
    user = st.session_state.auth['user']
    code = st.session_state.get('active_booking_code')
    booking = next((b for b in st.session_state.bookings if b['bookingCode'] == code), None)
    if not booking: logout(); return

    apt = next((a for a in st.session_state.apartments if a['id'] == booking['apartmentId']), None)
    host = next((u for u in st.session_state.users if u['id'] == apt['hostId']), None)

    # --- HEADER ELEGANTE ---
    st.markdown(f"""
    <div style="text-align: center; padding: 40px 0;">
        <p class="guest-gold">BENVENUTO A MILANO</p>
        <h1 style="font-size: 3rem; margin: 0;">{apt['name']}</h1>
        <p class="guest-data" style="margin-top: 10px;">Ospite: {user['fullName']}</p>
    </div>
    """, unsafe_allow_html=True)

    # --- MENU A SCHEDE STILIZZATO ---
    tabs = st.tabs(["🏠 HOME", "🗺️ GUIDA", "🤖 CONCIERGE", "📞 SUPPORTO"])

    with tabs[0]:
        c1, c2 = st.columns([1, 1])
        with c1:
            st.markdown(f"""
            <div class="guest-card">
                <div class="guest-icon">📍</div>
                <div class="guest-title">Posizione</div>
                <p class="guest-data">{apt['address']}</p>
                <a href="https://maps.google.com/?q={apt['address']}" target="_blank" style="color:#D4AF37; text-decoration:none; font-weight:bold;">Vedi Mappa &rarr;</a>
            </div>
            
            <div class="guest-card">
                <div class="guest-icon">📶</div>
                <div class="guest-title">WiFi</div>
                <p class="guest-gold">RETE</p>
                <p class="guest-data">{apt['wifiName']}</p>
                <p class="guest-gold">PASSWORD</p>
                <p class="guest-data" style="font-weight:bold;">{apt['wifiPassword']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with c2:
            st.markdown("""<div class="guest-card"><div class="guest-icon">📜</div><div class="guest-title">House Rules</div>""", unsafe_allow_html=True)
            st.info(apt['houseRules'])
            st.markdown("</div>", unsafe_allow_html=True)
            
            if apt.get('videoUrl'):
                st.markdown("""<div class="guest-card"><div class="guest-icon">🎬</div><div class="guest-title">Video Accesso</div>""", unsafe_allow_html=True)
                st.video(apt['videoUrl'])
                st.markdown("</div>", unsafe_allow_html=True)

    with tabs[1]:
        st.markdown("<h2 style='text-align:center; margin-bottom:30px;'>La Selezione dell'Host</h2>", unsafe_allow_html=True)
        if not apt['recommendations']:
            st.markdown("<p style='text-align:center;'>Nessun consiglio disponibile al momento.</p>", unsafe_allow_html=True)
        
        col_a, col_b = st.columns(2)
        for i, rec in enumerate(apt['recommendations']):
            with col_a if i % 2 == 0 else col_b:
                st.markdown(f"""
                <div class="guest-card" style="text-align:left;">
                    <p class="guest-gold">{rec['category']}</p>
                    <div class="guest-title">{rec['name']}</div>
                    <p class="guest-data" style="font-size:14px;">{rec['desc']}</p>
                    <a href="{rec.get('map', '#')}" style="color:#1A1A1A; font-weight:bold; font-size:12px;">NAVIGA &rarr;</a>
                </div>
                """, unsafe_allow_html=True)

    with tabs[2]:
        st.markdown("<div class='guest-card'><div class='guest-icon'>🤖</div><div class='guest-title'>Hadriano AI</div><p>Chiedimi qualsiasi cosa sull'appartamento o sulla città.</p></div>", unsafe_allow_html=True)
        
        q = st.chat_input("Esempio: Dove posso mangiare una pizza qui vicino?")
        if q:
            with st.spinner("Hadriano sta pensando..."):
                try:
                    if "GEMINI_API_KEY" in st.secrets:
                        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
                        model = genai.GenerativeModel('gemini-1.5-flash')
                        ctx = f"Sei un concierge di lusso. Appartamento: {apt['name']} in {apt['address']}. Regole: {apt['houseRules']}. Consigli Host: {apt['recommendations']}. Rispondi con tono elegante."
                        res = model.generate_content(f"{ctx} Domanda: {q}")
                        st.markdown(f"""
                        <div style="background-color:#F9F9F9; padding:20px; border-left: 3px solid #D4AF37; margin-top:20px;">
                            <b>Hadriano:</b><br>{res.text}
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.error("Configura la chiave API.")
                except:
                    st.error("Servizio momentaneamente non disponibile.")

    with tabs[3]:
        st.markdown(f"""
        <div class="guest-card">
            <div class="guest-icon">🆘</div>
            <div class="guest-title">Il tuo Host</div>
            <h3>{host['fullName']}</h3>
        </div>
        """, unsafe_allow_html=True)
        
        if host['isContactAvailable']:
            st.success(f"✅ {host['fullName']} è disponibile.")
            c1, c2 = st.columns(2)
            c1.button("📞 Chiama", use_container_width=True)
            c2.button("💬 WhatsApp", use_container_width=True)
        else:
            st.error("⛔ L'Host non è disturbabile al momento.")
            st.caption("Per emergenze mediche o di sicurezza chiama il 112.")

    st.markdown("<br><br><div style='text-align:center'><small>Hadriano Concierge © 2026</small></div>", unsafe_allow_html=True)
    if st.button("Esci / Logout", key="logout_guest"): logout()

# --- MAIN ---
if st.session_state.auth['user'] is None:
    login_screen()
elif st.session_state.auth['role'] == 'ADMIN':
    view_admin()
elif st.session_state.auth['role'] == 'HOST':
    view_host()
elif st.session_state.auth['role'] == 'GUEST':
    view_guest()
