import streamlit as st
import datetime
import pandas as pd
import google.generativeai as genai

# --- 1. CONFIGURAZIONE E STILE LUSSO ---
st.set_page_config(page_title="Hadriano Concierge", page_icon="🛎️", layout="wide")

st.markdown("""
    <style>
    /* Importazione Font Serif per il lusso */
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&display=swap');
    
    .stApp { background-color: #FDFDFD; color: #1A1A1A; }
    
    /* Titoli */
    h1, h2, h3, h4 { 
        font-family: 'Playfair Display', serif; 
        font-style: italic; 
        color: #1A1A1A; 
    }
    
    /* Testo "Gold" per etichette */
    .gold-label { 
        color: #D4AF37; 
        font-weight: 800; 
        text-transform: uppercase; 
        letter-spacing: 2px; 
        font-size: 10px;
        margin-bottom: 5px;
    }
    
    /* Box stile Card */
    .card-box {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #F0F0F0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.02);
        margin-bottom: 15px;
    }
    
    /* Bottoni */
    .stButton>button {
        background-color: #1A1A1A; 
        color: #D4AF37; 
        border-radius: 8px; 
        text-transform: uppercase; 
        font-size: 11px; 
        font-weight: bold; 
        border: 1px solid #D4AF37;
        width: 100%;
    }
    .stButton>button:hover { 
        background-color: #D4AF37; 
        color: white; 
        border-color: #D4AF37;
    }
    
    /* Input Fields */
    .stTextInput>div>div>input {
        background-color: #FAFAFA;
        border-radius: 10px;
        border: 1px solid #EEE;
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. GESTIONE DATI (SIMIL-DATABASE) ---
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
                'houseRules': 'No smoking. No parties.',
                'wifiName': 'Boutique_Guest', 'wifiPassword': 'milano-luxury',
                'videoUrl': 'https://www.w3schools.com/html/mov_bbb.mp4',
                'hostId': 'h1', 'lat': 45.4518, 'lon': 9.1678,
                'recommendations': [
                    {'id': 'r1', 'name': 'Langosteria', 'category': 'Ristorante', 'desc': 'Best seafood in Milan.', 'map': 'https://maps.google.com'}
                ]
            }
        ]
    
    if 'bookings' not in st.session_state:
        st.session_state.bookings = [
             {'id': 'b0', 'apartmentId': 'a1', 'guestName': 'Ospite Demo', 'bookingCode': 'WELCOME', 'checkInDate': str(datetime.date.today()), 'status': 'ACTIVE'}
        ]
        
    if 'auth' not in st.session_state:
        st.session_state.auth = {'user': None, 'role': None}
        
    # Variabile per gestire quale appartamento stiamo modificando (L'Album)
    if 'editing_apt_id' not in st.session_state:
        st.session_state.editing_apt_id = None

init_data()

# --- 3. FUNZIONI LOGICHE ---
def get_user_name(user_id):
    user = next((u for u in st.session_state.users if u['id'] == user_id), None)
    return user['fullName'] if user else "Nessuno"

def get_apt_name(apt_id):
    apt = next((a for a in st.session_state.apartments if a['id'] == apt_id), None)
    return apt['name'] if apt else "Sconosciuto"

# --- 4. LOGIN SYSTEM ---
def login_screen():
    c1, c2, c3 = st.columns([1,2,1])
    with c2:
        st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
        st.markdown("<p class='gold-label'>PREMIUM HOSPITALITY</p>", unsafe_allow_html=True)
        st.title("Hadriano Concierge")
        st.markdown("</div>", unsafe_allow_html=True)
        
        tab_guest, tab_staff = st.tabs(["ACCESSO OSPITE", "AREA STAFF"])
        
        with tab_guest:
            code = st.text_input("Codice di Accesso (es. WELCOME)", key="guest_code")
            if st.button("ENTRA NELLA SUITE", use_container_width=True):
                code = code.upper().strip()
                booking = next((b for b in st.session_state.bookings if b['bookingCode'] == code), None)
                if code == "WELCOME": # Demo Backdoor
                     # Se non esiste la prenotazione welcome, creala al volo per evitare errori
                     demo_exists = next((b for b in st.session_state.bookings if b['bookingCode'] == 'WELCOME'), None)
                     if not demo_exists:
                         st.session_state.bookings.append({'id': 'b0', 'apartmentId': 'a1', 'guestName': 'Ospite Demo', 'bookingCode': 'WELCOME', 'checkInDate': str(datetime.date.today()), 'status': 'ACTIVE'})
                     st.session_state.auth = {'user': {'id': 'demo', 'fullName': 'Ospite Eccellente'}, 'role': 'GUEST'}
                     st.session_state.active_booking_code = 'WELCOME'
                     st.rerun()
                elif booking:
                    st.session_state.auth = {'user': {'id': booking['id'], 'fullName': booking['guestName']}, 'role': 'GUEST'}
                    st.session_state.active_booking_code = booking['bookingCode']
                    st.rerun()
                else:
                    st.error("Codice non valido.")

        with tab_staff:
            email = st.text_input("Email Staff")
            pwd = st.text_input("Password", type="password")
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
                        st.error("Credenziali errate.")

def logout():
    st.session_state.auth = {'user': None, 'role': None}
    st.session_state.editing_apt_id = None
    st.rerun()

# --- 5. DASHBOARD ADMIN ---
def view_admin():
    st.sidebar.title("Admin Panel")
    if st.sidebar.button("Logout"): logout()
    
    menu = st.sidebar.radio("Navigazione", ["Gestione Immobili & Guida", "Gestione Host"])
    
    st.title("Admin Dashboard")
    
    if menu == "Gestione Immobili & Guida":
        st.markdown("### 🏨 Le Tue Proprietà")
        
        # --- SEZIONE CREAZIONE ---
        with st.expander("➕ AGGIUNGI NUOVO APPARTAMENTO"):
            with st.form("new_apt"):
                c1, c2 = st.columns(2)
                name = c1.text_input("Nome Appartamento")
                addr = c2.text_input("Indirizzo")
                wifi_n = c1.text_input("Nome WiFi")
                wifi_p = c2.text_input("Password WiFi")
                video = st.text_input("URL Video Istruzioni")
                rules = st.text_area("Regole della Casa")
                
                # Selezione Host
                hosts = [u for u in st.session_state.users if u['role'] == 'HOST']
                host_map = {h['fullName']: h['id'] for h in hosts}
                host_name = st.selectbox("Assegna Host", list(host_map.keys()))
                
                if st.form_submit_button("CREA PROPRIETÀ"):
                    new_id = f"a{len(st.session_state.apartments) + 1}"
                    st.session_state.apartments.append({
                        'id': new_id, 'name': name, 'address': addr, 'wifiName': wifi_n, 'wifiPassword': wifi_p,
                        'videoUrl': video, 'houseRules': rules, 'hostId': host_map[host_name],
                        'lat': 45.4642, 'lon': 9.1900, 'recommendations': []
                    })
                    st.success("Appartamento creato!")
                    st.rerun()

        st.divider()
        
        # --- LISTA APPARTAMENTI (CON GESTIONE "ALBUM") ---
        for apt in st.session_state.apartments:
            # Layout Carta Appartamento
            with st.container():
                st.markdown(f"""
                <div class="card-box">
                    <h3 style="margin:0;">{apt['name']}</h3>
                    <p style="color:grey; font-size:12px;">{apt['address']} • Host: {get_user_name(apt['hostId'])}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Pulsante per aprire "L'Album" (Modifica Guida)
                c1, c2 = st.columns([1, 4])
                if c1.button(f"📂 GESTISCI GUIDA", key=f"btn_edit_{apt['id']}"):
                    st.session_state.editing_apt_id = apt['id']
                    st.rerun()
            
            # --- INTERFACCIA MODIFICA GUIDA (ALBUM) ---
            if st.session_state.editing_apt_id == apt['id']:
                st.info(f"Stai modificando la Guida Ospiti per: **{apt['name']}**")
                
                # Tabella Raccomandazioni Esistenti
                if apt['recommendations']:
                    for rec in apt['recommendations']:
                        c_img, c_info, c_del = st.columns([1, 3, 1])
                        c_info.markdown(f"**{rec['category']}**: {rec['name']}")
                        c_info.caption(rec['desc'])
                        if c_del.button("❌", key=f"del_{apt['id']}_{rec['id']}"):
                            apt['recommendations'].remove(rec)
                            st.rerun()
                else:
                    st.caption("Nessun consiglio inserito. L'album è vuoto.")
                
                # Form per Aggiungere Nuova Raccomandazione
                st.markdown("#### Aggiungi Consiglio all'Album")
                with st.form(key=f"add_rec_{apt['id']}"):
                    r_cat = st.selectbox("Categoria", ["Ristorante", "Bar", "Supermarket", "Farmacia", "Cultura", "Svago"])
                    r_name = st.text_input("Nome Luogo")
                    r_desc = st.text_area("Descrizione / Perché andare?")
                    r_map = st.text_input("Link Google Maps")
                    
                    if st.form_submit_button("AGGIUNGI ALLA GUIDA"):
                        new_rec = {
                            'id': f"r{len(apt['recommendations'])+100}",
                            'category': r_cat, 'name': r_name, 'desc': r_desc, 'map': r_map
                        }
                        apt['recommendations'].append(new_rec)
                        st.success("Aggiunto!")
                        st.rerun()
                
                if st.button("CHIUDI MODIFICA"):
                    st.session_state.editing_apt_id = None
                    st.rerun()
                st.divider()

    elif menu == "Gestione Host":
        st.subheader("👥 Il tuo Staff")
        with st.form("new_host"):
            c1, c2 = st.columns(2)
            n = c1.text_input("Nome")
            e = c2.text_input("Email")
            p = st.text_input("Password")
            if st.form_submit_button("REGISTRA HOST"):
                st.session_state.users.append({'id': f"h{len(st.session_state.users)+1}", 'fullName': n, 'email': e, 'password': p, 'role': 'HOST', 'isContactAvailable': True})
                st.success("Host aggiunto!")
                st.rerun()
        
        st.table(pd.DataFrame([
            {"Nome": u['fullName'], "Email": u['email'], "Password": u['password']} 
            for u in st.session_state.users if u['role'] == 'HOST'
        ]))

# --- 6. DASHBOARD HOST ---
def view_host():
    me = st.session_state.auth['user']
    st.sidebar.title(f"Ciao, {me['fullName']}")
    
    # Toggle Disponibilità
    st.sidebar.markdown("---")
    st.sidebar.write("Stato Attuale:")
    if st.sidebar.button(f"{'🟢 DISPONIBILE' if me['isContactAvailable'] else '🔴 NON DISPONIBILE'}"):
        # Aggiorniamo lo stato
        for u in st.session_state.users:
            if u['id'] == me['id']:
                u['isContactAvailable'] = not u['isContactAvailable']
        st.rerun()
    st.sidebar.caption("Clicca per cambiare stato")
    
    if st.sidebar.button("Logout"): logout()

    st.title("Portale Host")
    
    # I miei appartamenti
    my_apts = [a for a in st.session_state.apartments if a['hostId'] == me['id']]
    
    c1, c2 = st.columns([1, 1])
    
    with c1:
        st.markdown("### 🔑 Genera Accesso")
        with st.form("host_booking"):
            apt_sel = st.selectbox("Appartamento", [a['name'] for a in my_apts])
            g_name = st.text_input("Nome Ospite")
            if st.form_submit_button("CREA CODICE"):
                import random, string
                code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
                sel_id = next(a['id'] for a in my_apts if a['name'] == apt_sel)
                st.session_state.bookings.append({
                    'id': f"b{len(st.session_state.bookings)+1}",
                    'apartmentId': sel_id, 'guestName': g_name,
                    'bookingCode': code, 'checkInDate': str(datetime.date.today()), 'status': 'ACTIVE'
                })
                st.success(f"CODICE CREATO: {code}")
                st.rerun()

    with c2:
        st.markdown("### 📅 Prenotazioni Attive")
        my_apt_ids = [a['id'] for a in my_apts]
        active_b = [b for b in st.session_state.bookings if b['apartmentId'] in my_apt_ids]
        
        if not active_b:
            st.info("Nessun ospite attivo.")
        
        for b in active_b:
            st.markdown(f"""
            <div class="card-box">
                <h4 style="color:#D4AF37;">{b['bookingCode']}</h4>
                <p><b>{b['guestName']}</b><br>
                {get_apt_name(b['apartmentId'])}<br>
                <span style="font-size:10px;">Check-in: {b['checkInDate']}</span></p>
            </div>
            """, unsafe_allow_html=True)

# --- 7. VISTA OSPITE (CLIENTE) ---
def view_guest():
    user = st.session_state.auth['user']
    code = st.session_state.get('active_booking_code')
    booking = next((b for b in st.session_state.bookings if b['bookingCode'] == code), None)
    
    if not booking:
        st.error("Errore sessione.")
        if st.button("Esci"): logout()
        return

    apt = next((a for a in st.session_state.apartments if a['id'] == booking['apartmentId']), None)
    host = next((u for u in st.session_state.users if u['id'] == apt['hostId']), None)

    # Header Elegante
    st.markdown(f"<p class='gold-label' style='text-align:center;'>BENVENUTO A MILANO</p>", unsafe_allow_html=True)
    st.markdown(f"<h1 style='text-align:center;'>{apt['name']}</h1>", unsafe_allow_html=True)
    st.markdown("---")

    # Navigazione
    tabs = st.tabs(["🏠 HOME", "🗺️ GUIDA LOCAL", "🤖 CONCIERGE AI", "👤 CONTATTI"])

    with tabs[0]: # HOME
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"**Indirizzo:** {apt['address']}")
            st.markdown("### 📶 WiFi")
            st.code(f"Rete: {apt['wifiName']}\nPass: {apt['wifiPassword']}")
            st.markdown("### 📜 Regole")
            st.info(apt['houseRules'])
        with c2:
            if apt['videoUrl']:
                st.video(apt['videoUrl'])
            else:
                st.image("https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?w=800", caption="Il tuo soggiorno")

    with tabs[1]: # GUIDA (L'ALBUM)
        st.markdown("### 💎 I Consigli dell'Host")
        if not apt['recommendations']:
            st.warning("L'Host non ha ancora curato la guida per questa zona.")
        else:
            for rec in apt['recommendations']:
                with st.expander(f"{rec['category']} | {rec['name']}"):
                    st.write(rec['desc'])
                    if rec.get('map'):
                        st.markdown(f"[📍 Vedi su Mappa]({rec['map']})")

    with tabs[2]: # AI
        st.markdown("### 🛎️ Chiedi ad Hadriano")
        q = st.chat_input("Consigli su cena, taxi, o sulla casa...")
        if q:
            try:
                # Recupera la chiave dai Secrets in modo sicuro
                if "GEMINI_API_KEY" in st.secrets:
                    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    context = f"Sei un concierge di lusso per l'appartamento {apt['name']} a Milano. Regole: {apt['houseRules']}. Consigli Host: {apt['recommendations']}."
                    res = model.generate_content(f"{context} Domanda utente: {q}")
                    st.markdown(f"**Hadriano:** {res.text}")
                else:
                    st.error("Chiave API mancante. Configura i Secrets.")
            except:
                st.error("Hadriano è momentaneamente occupato.")

    with tabs[3]: # CONTATTI
        st.markdown("### 🆘 Assistenza")
        if host['isContactAvailable']:
            st.success(f"✅ {host['fullName']} è attualmente DISPONIBILE.")
            st.button("📞 Chiama Host")
            st.button("💬 WhatsApp")
        else:
            st.error(f"⛔ {host['fullName']} non è al momento disturbabile.")
            st.caption("Per emergenze chiama il 112.")
            
    st.markdown("---")
    if st.button("Esci / Logout"): logout()

# --- ROUTER PRINCIPALE ---
if st.session_state.auth['user'] is None:
    login_screen()
elif st.session_state.auth['role'] == 'ADMIN':
    view_admin()
elif st.session_state.auth['role'] == 'HOST':
    view_host()
elif st.session_state.auth['role'] == 'GUEST':
    view_guest()
