import streamlit as st
import json
import requests
from datetime import datetime, timedelta
import random
import hashlib

# ============================================================================
# CONFIGURAZIONE INIZIALE
# ============================================================================

st.set_page_config(
    page_title="Hadriano Concierge",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================================
# DIZIONARI MULTILINGUA
# ============================================================================

translations = {
    "it": {
        "app_title": "Hadriano Concierge",
        "app_subtitle": "L'arte dell'ospitalità di lusso",
        "login_title": "Accesso Privilegiato",
        "role_select": "Seleziona il tuo ruolo",
        "admin": "Amministratore",
        "host": "Host",
        "guest": "Ospite",
        "username": "Nome utente",
        "password": "Password",
        "login": "Accedi",
        "logout": "Esci",
        "welcome": "Benvenuto",
        "back_to_login": "Torna al login",
        "add_apartment": "Aggiungi Appartamento",
        "apartment_name": "Nome Appartamento",
        "address": "Indirizzo",
        "cover_photo": "URL Foto Copertina",
        "wifi": "WiFi",
        "rules": "Regole della Casa",
        "video": "URL Video Istruzioni",
        "save": "Salva",
        "delete": "Elimina",
        "manage_staff": "Gestisci Staff",
        "add_host": "Aggiungi Host",
        "host_name": "Nome Host",
        "host_email": "Email Host",
        "manage_poi": "Gestisci Punti di Interesse",
        "poi_name": "Nome Punto di Interesse",
        "poi_type": "Tipo",
        "poi_description": "Descrizione",
        "poi_address": "Indirizzo",
        "poi_map": "URL Mappa",
        "generate_codes": "Genera Codici Ospiti",
        "availability": "Disponibilità",
        "available": "Disponibile",
        "busy": "Non Disturbare",
        "status_green": "Stato: Verde - Pronto ad assistere",
        "status_red": "Stato: Rosso - Non disponibile",
        "guest_code": "Inserisci Codice Prenotazione",
        "enter": "Entra",
        "home": "Home",
        "local_guide": "Guida Local",
        "ai_concierge": "Concierge AI",
        "assistance": "Assistenza",
        "house_info": "Informazioni Casa",
        "wifi_details": "Dettagli WiFi",
        "house_rules": "Regole della Casa",
        "video_guide": "Guida Video",
        "restaurants": "Ristoranti",
        "museums": "Musei",
        "shopping": "Shopping",
        "attractions": "Attrazioni",
        "ask_hadriano": "Chiedi a Hadriano",
        "type_question": "Digita la tua domanda...",
        "send": "Invia",
        "host_available": "L'Host è disponibile",
        "call_host": "Chiama Host",
        "whatsapp_host": "WhatsApp Host",
        "contact_support": "Contatta Supporto",
        "change_language": "Cambia Lingua",
        "select_language": "Seleziona Lingua",
        "italian": "Italiano",
        "english": "Inglese",
        "spanish": "Spagnolo",
        "french": "Francese",
        "german": "Tedesco",
        "russian": "Russo",
        "chinese": "Cinese",
        "apartments": "Appartamenti",
        "hosts": "Hosts",
        "points_of_interest": "Punti di Interesse",
        "guest_codes": "Codici Ospiti",
        "no_apartments": "Nessun appartamento aggiunto",
        "no_hosts": "Nessun host aggiunto",
        "no_poi": "Nessun punto di interesse aggiunto",
        "no_codes": "Nessun codice generato",
        "code_generated": "Codice generato con successo",
        "invalid_login": "Credenziali non valide",
        "invalid_code": "Codice prenotazione non valido",
        "error": "Errore",
        "success": "Successo",
        "save_success": "Salvato con successo",
        "delete_success": "Eliminato con successo"
    },
    "en": {
        "app_title": "Hadriano Concierge",
        "app_subtitle": "The Art of Luxury Hospitality",
        "login_title": "Privileged Access",
        "role_select": "Select your role",
        "admin": "Administrator",
        "host": "Host",
        "guest": "Guest",
        "username": "Username",
        "password": "Password",
        "login": "Login",
        "logout": "Logout",
        "welcome": "Welcome",
        "back_to_login": "Back to login",
        "add_apartment": "Add Apartment",
        "apartment_name": "Apartment Name",
        "address": "Address",
        "cover_photo": "Cover Photo URL",
        "wifi": "WiFi",
        "rules": "House Rules",
        "video": "Video Instructions URL",
        "save": "Save",
        "delete": "Delete",
        "manage_staff": "Manage Staff",
        "add_host": "Add Host",
        "host_name": "Host Name",
        "host_email": "Host Email",
        "manage_poi": "Manage Points of Interest",
        "poi_name": "Point of Interest Name",
        "poi_type": "Type",
        "poi_description": "Description",
        "poi_address": "Address",
        "poi_map": "Map URL",
        "generate_codes": "Generate Guest Codes",
        "availability": "Availability",
        "available": "Available",
        "busy": "Do Not Disturb",
        "status_green": "Status: Green - Ready to assist",
        "status_red": "Status: Red - Not available",
        "guest_code": "Enter Booking Code",
        "enter": "Enter",
        "home": "Home",
        "local_guide": "Local Guide",
        "ai_concierge": "AI Concierge",
        "assistance": "Assistance",
        "house_info": "House Information",
        "wifi_details": "WiFi Details",
        "house_rules": "House Rules",
        "video_guide": "Video Guide",
        "restaurants": "Restaurants",
        "museums": "Museums",
        "shopping": "Shopping",
        "attractions": "Attractions",
        "ask_hadriano": "Ask Hadriano",
        "type_question": "Type your question...",
        "send": "Send",
        "host_available": "Host is available",
        "call_host": "Call Host",
        "whatsapp_host": "WhatsApp Host",
        "contact_support": "Contact Support",
        "change_language": "Change Language",
        "select_language": "Select Language",
        "italian": "Italian",
        "english": "English",
        "spanish": "Spanish",
        "french": "French",
        "german": "German",
        "russian": "Russian",
        "chinese": "Chinese",
        "apartments": "Apartments",
        "hosts": "Hosts",
        "points_of_interest": "Points of Interest",
        "guest_codes": "Guest Codes",
        "no_apartments": "No apartments added",
        "no_hosts": "No hosts added",
        "no_poi": "No points of interest added",
        "no_codes": "No codes generated",
        "code_generated": "Code generated successfully",
        "invalid_login": "Invalid credentials",
        "invalid_code": "Invalid booking code",
        "error": "Error",
        "success": "Success",
        "save_success": "Saved successfully",
        "delete_success": "Deleted successfully"
    },
    "es": {
        "app_title": "Hadriano Concierge",
        "app_subtitle": "El Arte de la Hospitalidad de Lujo",
        "login_title": "Acceso Privilegiado",
        "role_select": "Selecciona tu rol",
        "admin": "Administrador",
        "host": "Anfitrión",
        "guest": "Huésped",
        "username": "Nombre de usuario",
        "password": "Contraseña",
        "login": "Iniciar sesión",
        "logout": "Cerrar sesión",
        "welcome": "Bienvenido",
        "back_to_login": "Volver al inicio",
        "add_apartment": "Añadir Apartamento",
        "apartment_name": "Nombre del Apartamento",
        "address": "Dirección",
        "cover_photo": "URL Foto de Portada",
        "wifi": "WiFi",
        "rules": "Reglas de la Casa",
        "video": "URL Video Instrucciones",
        "save": "Guardar",
        "delete": "Eliminar",
        "manage_staff": "Gestionar Personal",
        "add_host": "Añadir Anfitrión",
        "host_name": "Nombre del Anfitrión",
        "host_email": "Email del Anfitrión",
        "manage_poi": "Gestionar Puntos de Interés",
        "poi_name": "Nombre del Punto de Interés",
        "poi_type": "Tipo",
        "poi_description": "Descripción",
        "poi_address": "Dirección",
        "poi_map": "URL Mapa",
        "generate_codes": "Generar Códigos de Huésped",
        "availability": "Disponibilidad",
        "available": "Disponible",
        "busy": "No Molestar",
        "status_green": "Estado: Verde - Listo para asistir",
        "status_red": "Estado: Rojo - No disponible",
        "guest_code": "Introduce Código de Reserva",
        "enter": "Entrar",
        "home": "Inicio",
        "local_guide": "Guía Local",
        "ai_concierge": "Concierge AI",
        "assistance": "Asistencia",
        "house_info": "Información de la Casa",
        "wifi_details": "Detalles WiFi",
        "house_rules": "Reglas de la Casa",
        "video_guide": "Guía en Video",
        "restaurants": "Restaurantes",
        "museums": "Museos",
        "shopping": "Compras",
        "attractions": "Atracciones",
        "ask_hadriano": "Pregunta a Hadriano",
        "type_question": "Escribe tu pregunta...",
        "send": "Enviar",
        "host_available": "El anfitrión está disponible",
        "call_host": "Llamar al Anfitrión",
        "whatsapp_host": "WhatsApp Anfitrión",
        "contact_support": "Contactar Soporte",
        "change_language": "Cambiar Idioma",
        "select_language": "Seleccionar Idioma",
        "italian": "Italiano",
        "english": "Inglés",
        "spanish": "Español",
        "french": "Francés",
        "german": "Alemán",
        "russian": "Ruso",
        "chinese": "Chino",
        "apartments": "Apartamentos",
        "hosts": "Anfitriones",
        "points_of_interest": "Puntos de Interés",
        "guest_codes": "Códigos de Huésped",
        "no_apartments": "No hay apartamentos añadidos",
        "no_hosts": "No hay anfitriones añadidos",
        "no_poi": "No hay puntos de interés añadidos",
        "no_codes": "No hay códigos generados",
        "code_generated": "Código generado con éxito",
        "invalid_login": "Credenciales no válidas",
        "invalid_code": "Código de reserva no válido",
        "error": "Error",
        "success": "Éxito",
        "save_success": "Guardado con éxito",
        "delete_success": "Eliminado con éxito"
    },
    "fr": {
        "app_title": "Hadriano Concierge",
        "app_subtitle": "L'Art de l'Hospitalité de Luxe",
        "login_title": "Accès Privilégié",
        "role_select": "Sélectionnez votre rôle",
        "admin": "Administrateur",
        "host": "Hôte",
        "guest": "Invité",
        "username": "Nom d'utilisateur",
        "password": "Mot de passe",
        "login": "Connexion",
        "logout": "Déconnexion",
        "welcome": "Bienvenue",
        "back_to_login": "Retour à la connexion",
        "add_apartment": "Ajouter un Appartement",
        "apartment_name": "Nom de l'Appartement",
        "address": "Adresse",
        "cover_photo": "URL Photo de Couverture",
        "wifi": "WiFi",
        "rules": "Règles de la Maison",
        "video": "URL Vidéo d'Instructions",
        "save": "Enregistrer",
        "delete": "Supprimer",
        "manage_staff": "Gérer le Personnel",
        "add_host": "Ajouter un Hôte",
        "host_name": "Nom de l'Hôte",
        "host_email": "Email de l'Hôte",
        "manage_poi": "Gérer les Points d'Intérêt",
        "poi_name": "Nom du Point d'Intérêt",
        "poi_type": "Type",
        "poi_description": "Description",
        "poi_address": "Adresse",
        "poi_map": "URL Carte",
        "generate_codes": "Générer des Codes d'Invitation",
        "availability": "Disponibilité",
        "available": "Disponible",
        "busy": "Ne Pas Déranger",
        "status_green": "Statut: Vert - Prêt à aider",
        "status_red": "Statut: Rouge - Non disponible",
        "guest_code": "Entrez le Code de Réservation",
        "enter": "Entrer",
        "home": "Accueil",
        "local_guide": "Guide Local",
        "ai_concierge": "Concierge AI",
        "assistance": "Assistance",
        "house_info": "Informations sur la Maison",
        "wifi_details": "Détails WiFi",
        "house_rules": "Règles de la Maison",
        "video_guide": "Guide Vidéo",
        "restaurants": "Restaurants",
        "museums": "Musées",
        "shopping": "Shopping",
        "attractions": "Attractions",
        "ask_hadriano": "Demandez à Hadriano",
        "type_question": "Tapez votre question...",
        "send": "Envoyer",
        "host_available": "L'hôte est disponible",
        "call_host": "Appeler l'Hôte",
        "whatsapp_host": "WhatsApp Hôte",
        "contact_support": "Contacter le Support",
        "change_language": "Changer de Langue",
        "select_language": "Sélectionner la Langue",
        "italian": "Italien",
        "english": "Anglais",
        "spanish": "Espagnol",
        "french": "Français",
        "german": "Allemand",
        "russian": "Russe",
        "chinese": "Chinois",
        "apartments": "Appartements",
        "hosts": "Hôtes",
        "points_of_interest": "Points d'Intérêt",
        "guest_codes": "Codes d'Invitation",
        "no_apartments": "Aucun appartement ajouté",
        "no_hosts": "Aucun hôte ajouté",
        "no_poi": "Aucun point d'intérêt ajouté",
        "no_codes": "Aucun code généré",
        "code_generated": "Code généré avec succès",
        "invalid_login": "Identifiants invalides",
        "invalid_code": "Code de réservation invalide",
        "error": "Erreur",
        "success": "Succès",
        "save_success": "Enregistré avec succès",
        "delete_success": "Supprimé avec succès"
    },
    "de": {
        "app_title": "Hadriano Concierge",
        "app_subtitle": "Die Kunst der Luxus-Gastfreundschaft",
        "login_title": "Privilegierter Zugang",
        "role_select": "Wählen Sie Ihre Rolle",
        "admin": "Administrator",
        "host": "Gastgeber",
        "guest": "Gast",
        "username": "Benutzername",
        "password": "Passwort",
        "login": "Anmelden",
        "logout": "Abmelden",
        "welcome": "Willkommen",
        "back_to_login": "Zurück zur Anmeldung",
        "add_apartment": "Apartment hinzufügen",
        "apartment_name": "Apartment-Name",
        "address": "Adresse",
        "cover_photo": "Titelbild-URL",
        "wifi": "WiFi",
        "rules": "Hausregeln",
        "video": "Videoanleitung URL",
        "save": "Speichern",
        "delete": "Löschen",
        "manage_staff": "Personal verwalten",
        "add_host": "Gastgeber hinzufügen",
        "host_name": "Gastgeber-Name",
        "host_email": "Gastgeber-E-Mail",
        "manage_poi": "Points of Interest verwalten",
        "poi_name": "Name des Points of Interest",
        "poi_type": "Typ",
        "poi_description": "Beschreibung",
        "poi_address": "Adresse",
        "poi_map": "Karten-URL",
        "generate_codes": "Gast-Codes generieren",
        "availability": "Verfügbarkeit",
        "available": "Verfügbar",
        "busy": "Bitte nicht stören",
        "status_green": "Status: Grün - Bereit zu helfen",
        "status_red": "Status: Rot - Nicht verfügbar",
        "guest_code": "Buchungscode eingeben",
        "enter": "Betreten",
        "home": "Startseite",
        "local_guide": "Lokaler Guide",
        "ai_concierge": "KI-Concierge",
        "assistance": "Assistenz",
        "house_info": "Hausinformationen",
        "wifi_details": "WiFi-Details",
        "house_rules": "Hausregeln",
        "video_guide": "Videoguide",
        "restaurants": "Restaurants",
        "museums": "Museen",
        "shopping": "Einkaufen",
        "attractions": "Sehenswürdigkeiten",
        "ask_hadriano": "Fragen Sie Hadriano",
        "type_question": "Geben Sie Ihre Frage ein...",
        "send": "Senden",
        "host_available": "Gastgeber ist verfügbar",
        "call_host": "Gastgeber anrufen",
        "whatsapp_host": "WhatsApp Gastgeber",
        "contact_support": "Support kontaktieren",
        "change_language": "Sprache ändern",
        "select_language": "Sprache auswählen",
        "italian": "Italienisch",
        "english": "Englisch",
        "spanish": "Spanisch",
        "french": "Französisch",
        "german": "Deutsch",
        "russian": "Russisch",
        "chinese": "Chinesisch",
        "apartments": "Apartments",
        "hosts": "Gastgeber",
        "points_of_interest": "Points of Interest",
        "guest_codes": "Gast-Codes",
        "no_apartments": "Keine Apartments hinzugefügt",
        "no_hosts": "Keine Gastgeber hinzugefügt",
        "no_poi": "Keine Points of Interest hinzugefügt",
        "no_codes": "Keine Codes generiert",
        "code_generated": "Code erfolgreich generiert",
        "invalid_login": "Ungültige Anmeldedaten",
        "invalid_code": "Ungültiger Buchungscode",
        "error": "Fehler",
        "success": "Erfolg",
        "save_success": "Erfolgreich gespeichert",
        "delete_success": "Erfolgreich gelöscht"
    },
    "ru": {
        "app_title": "Hadriano Concierge",
        "app_subtitle": "Искусство Роскошного Гостеприимства",
        "login_title": "Привилегированный доступ",
        "role_select": "Выберите свою роль",
        "admin": "Администратор",
        "host": "Хост",
        "guest": "Гость",
        "username": "Имя пользователя",
        "password": "Пароль",
        "login": "Войти",
        "logout": "Выйти",
        "welcome": "Добро пожаловать",
        "back_to_login": "Вернуться к входу",
        "add_apartment": "Добавить апартаменты",
        "apartment_name": "Название апартаментов",
        "address": "Адрес",
        "cover_photo": "URL обложки",
        "wifi": "WiFi",
        "rules": "Правила дома",
        "video": "URL видеоинструкций",
        "save": "Сохранить",
        "delete": "Удалить",
        "manage_staff": "Управление персоналом",
        "add_host": "Добавить хоста",
        "host_name": "Имя хоста",
        "host_email": "Email хоста",
        "manage_poi": "Управление достопримечательностями",
        "poi_name": "Название достопримечательности",
        "poi_type": "Тип",
        "poi_description": "Описание",
        "poi_address": "Адрес",
        "poi_map": "URL карты",
        "generate_codes": "Сгенерировать коды гостей",
        "availability": "Доступность",
        "available": "Доступен",
        "busy": "Не беспокоить",
        "status_green": "Статус: Зеленый - Готов помочь",
        "status_red": "Статус: Красный - Недоступен",
        "guest_code": "Введите код бронирования",
        "enter": "Войти",
        "home": "Главная",
        "local_guide": "Локальный гид",
        "ai_concierge": "AI Консьерж",
        "assistance": "Помощь",
        "house_info": "Информация о доме",
        "wifi_details": "Детали WiFi",
        "house_rules": "Правила дома",
        "video_guide": "Видеогид",
        "restaurants": "Рестораны",
        "museums": "Музеи",
        "shopping": "Шоппинг",
        "attractions": "Достопримечательности",
        "ask_hadriano": "Спросите Адриана",
        "type_question": "Введите ваш вопрос...",
        "send": "Отправить",
        "host_available": "Хост доступен",
        "call_host": "Позвонить хосту",
        "whatsapp_host": "WhatsApp хоста",
        "contact_support": "Связаться с поддержкой",
        "change_language": "Изменить язык",
        "select_language": "Выберите язык",
        "italian": "Итальянский",
        "english": "Английский",
        "spanish": "Испанский",
        "french": "Французский",
        "german": "Немецкий",
        "russian": "Русский",
        "chinese": "Китайский",
        "apartments": "Апартаменты",
        "hosts": "Хосты",
        "points_of_interest": "Достопримечательности",
        "guest_codes": "Коды гостей",
        "no_apartments": "Нет добавленных апартаментов",
        "no_hosts": "Нет добавленных хостов",
        "no_poi": "Нет добавленных достопримечательностей",
        "no_codes": "Нет сгенерированных кодов",
        "code_generated": "Код успешно сгенерирован",
        "invalid_login": "Неверные учетные данные",
        "invalid_code": "Неверный код бронирования",
        "error": "Ошибка",
        "success": "Успех",
        "save_success": "Успешно сохранено",
        "delete_success": "Успешно удалено"
    },
    "zh": {
        "app_title": "Hadriano Concierge",
        "app_subtitle": "奢华款待的艺术",
        "login_title": "特权访问",
        "role_select": "选择您的角色",
        "admin": "管理员",
        "host": "房东",
        "guest": "客人",
        "username": "用户名",
        "password": "密码",
        "login": "登录",
        "logout": "登出",
        "welcome": "欢迎",
        "back_to_login": "返回登录",
        "add_apartment": "添加公寓",
        "apartment_name": "公寓名称",
        "address": "地址",
        "cover_photo": "封面照片URL",
        "wifi": "WiFi",
        "rules": "房屋规则",
        "video": "视频说明URL",
        "save": "保存",
        "delete": "删除",
        "manage_staff": "管理员工",
        "add_host": "添加房东",
        "host_name": "房东姓名",
        "host_email": "房东邮箱",
        "manage_poi": "管理兴趣点",
        "poi_name": "兴趣点名称",
        "poi_type": "类型",
        "poi_description": "描述",
        "poi_address": "地址",
        "poi_map": "地图URL",
        "generate_codes": "生成客人代码",
        "availability": "可用性",
        "available": "可用",
        "busy": "请勿打扰",
        "status_green": "状态: 绿色 - 准备协助",
        "status_red": "状态: 红色 - 不可用",
        "guest_code": "输入预订代码",
        "enter": "进入",
        "home": "首页",
        "local_guide": "本地指南",
        "ai_concierge": "AI礼宾",
        "assistance": "协助",
        "house_info": "房屋信息",
        "wifi_details": "WiFi详情",
        "house_rules": "房屋规则",
        "video_guide": "视频指南",
        "restaurants": "餐厅",
        "museums": "博物馆",
        "shopping": "购物",
        "attractions": "景点",
        "ask_hadriano": "询问Hadriano",
        "type_question": "输入您的问题...",
        "send": "发送",
        "host_available": "房东可用",
        "call_host": "致电房东",
        "whatsapp_host": "WhatsApp房东",
        "contact_support": "联系支持",
        "change_language": "更改语言",
        "select_language": "选择语言",
        "italian": "意大利语",
        "english": "英语",
        "spanish": "西班牙语",
        "french": "法语",
        "german": "德语",
        "russian": "俄语",
        "chinese": "中文",
        "apartments": "公寓",
        "hosts": "房东",
        "points_of_interest": "兴趣点",
        "guest_codes": "客人代码",
        "no_apartments": "未添加公寓",
        "no_hosts": "未添加房东",
        "no_poi": "未添加兴趣点",
        "no_codes": "未生成代码",
        "code_generated": "代码生成成功",
        "invalid_login": "凭据无效",
        "invalid_code": "预订代码无效",
        "error": "错误",
        "success": "成功",
        "save_success": "保存成功",
        "delete_success": "删除成功"
    }
}

# ============================================================================
# INIZIALIZZAZIONE SESSION STATE
# ============================================================================

def initialize_session_state():
    """Inizializza tutte le variabili di sessione necessarie"""
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'user_role' not in st.session_state:
        st.session_state.user_role = None
    if 'username' not in st.session_state:
        st.session_state.username = None
    if 'current_language' not in st.session_state:
        st.session_state.current_language = 'it'
    if 'current_apartment' not in st.session_state:
        st.session_state.current_apartment = None
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    # Database simulato
    if 'apartments' not in st.session_state:
        st.session_state.apartments = []
    
    if 'hosts' not in st.session_state:
        # Host predefiniti per testing
        st.session_state.hosts = [
            {"username": "host1", "password": "host123", "name": "Marco Rossi", "email": "marco@hadriano.com", "available": True},
            {"username": "host2", "password": "host456", "name": "Anna Bianchi", "email": "anna@hadriano.com", "available": False}
        ]
    
    if 'admin_users' not in st.session_state:
        # Admin predefinito
        st.session_state.admin_users = [
            {"username": "admin", "password": "admin123"}
        ]
    
    if 'points_of_interest' not in st.session_state:
        st.session_state.points_of_interest = []
    
    if 'guest_codes' not in st.session_state:
        st.session_state.guest_codes = {}

# ============================================================================
# FUNZIONI DI SUPPORTO
# ============================================================================

def get_text(key):
    """Restituisce il testo tradotto nella lingua corrente"""
    lang = st.session_state.current_language
    if lang in translations and key in translations[lang]:
        return translations[lang][key]
    # Fallback su italiano
    return translations['it'][key] if key in translations['it'] else key

def get_gemini_response(prompt, language):
    """Simula una risposta da Google Gemini"""
    # In un'implementazione reale, qui si chiamerebbe l'API di Google Gemini
    # Per ora simuliamo risposte in base alla lingua
    
    responses_by_language = {
        'it': [
            "Certamente! La casa dispone di WiFi ad alta velocità. La password è 'HadrianoLuxury2024'. Per qualsiasi problema tecnico, non esiti a contattarci.",
            "Il ristorante più vicino consigliato è 'La Pergola', a soli 10 minuti a piedi. Offre una vista mozzafiato sulla città e una cucina stellata.",
            "Il check-out è previsto per le 11:00. Le chiediamo gentilmente di lasciare le chiavi nell'apposita cassetta di sicurezza.",
            "Nelle vicinanze troverà la Galleria Borghese, uno dei musei più belli di Roma. Consiglio vivamente la prenotazione online per evitare code.",
            "Per la temperatura dell'acqua della doccia, giri la manopola sinistra in senso orario per aumentare il calore. Se dovesse avere problemi, sono a disposizione."
        ],
        'en': [
            "Certainly! The house has high-speed WiFi. The password is 'HadrianoLuxury2024'. For any technical issues, please do not hesitate to contact us.",
            "The nearest recommended restaurant is 'La Pergola', just a 10-minute walk away. It offers a breathtaking view of the city and starred cuisine.",
            "Check-out is scheduled for 11:00 AM. We kindly ask you to leave the keys in the designated safety box.",
            "Nearby you will find the Borghese Gallery, one of the most beautiful museums in Rome. I highly recommend online booking to avoid queues.",
            "For the shower water temperature, turn the left knob clockwise to increase heat. If you have any problems, I am available."
        ],
        'es': [
            "¡Por supuesto! La casa tiene WiFi de alta velocidad. La contraseña es 'HadrianoLuxury2024'. Para cualquier problema técnico, no dude en contactarnos.",
            "El restaurante recomendado más cercano es 'La Pergola', a solo 10 minutos a pie. Ofrece una vista impresionante de la ciudad y una cocina estrellada.",
            "El check-out está programado para las 11:00. Le rogamos que deje las llaves en la caja de seguridad designada.",
            "Cerca encontrará la Galería Borghese, uno de los museos más bellos de Roma. Recomiendo encarecidamente la reserva en línea para evitar colas.",
            "Para la temperatura del agua de la ducha, gire la perilla izquierda en el sentido de las agujas del reloj para aumentar el calor. Si tiene algún problema, estoy disponible."
        ],
        'fr': [
            "Certainement! La maison dispose d'un WiFi haute vitesse. Le mot de passe est 'HadrianoLuxury2024'. Pour tout problème technique, n'hésitez pas à nous contacter.",
            "Le restaurant recommandé le plus proche est 'La Pergola', à seulement 10 minutes à pied. Il offre une vue imprenable sur la ville et une cuisine étoilée.",
            "Le check-out est prévu pour 11h00. Nous vous demandons gentiment de laisser les clés dans la boîte de sécurité désignée.",
            "À proximité, vous trouverez la Galerie Borghese, l'un des plus beaux musées de Rome. Je recommande vivement la réservation en ligne pour éviter les files d'attente.",
            "Pour la température de l'eau de la douche, tournez le bouton gauche dans le sens des aiguilles d'une montre pour augmenter la chaleur. Si vous avez des problèmes, je suis disponible."
        ],
        'de': [
            "Sicherlich! Das Haus verfügt über High-Speed-WLAN. Das Passwort lautet 'HadrianoLuxury2024'. Bei technischen Problemen zögern Sie bitte nicht, uns zu kontaktieren.",
            "Das nächstgelegene empfohlene Restaurant ist 'La Pergola', nur 10 Gehminuten entfernt. Es bietet einen atemberaubenden Blick auf die Stadt und Sterneküche.",
            "Der Check-out ist für 11:00 Uhr geplant. Wir bitten Sie freundlich, die Schlüssel in der dafür vorgesehenen Sicherheitsbox zu hinterlassen.",
            "In der Nähe finden Sie die Galleria Borghese, eines der schönsten Museen Roms. Ich empfehle dringend die Online-Buchung, um Warteschlangen zu vermeiden.",
            "Für die Duschtemperatur drehen Sie den linken Knopf im Uhrzeigersinn, um die Wärme zu erhöhen. Bei Problemen stehe ich zur Verfügung."
        ],
        'ru': [
            "Конечно! В доме есть высокоскоростной WiFi. Пароль 'HadrianoLuxury2024'. По любым техническим вопросам, пожалуйста, не стесняйтесь обращаться к нам.",
            "Ближайший рекомендуемый ресторан - 'La Pergola', всего в 10 минутах ходьбы. Он предлагает захватывающий вид на город и звездную кухню.",
            "Выезд запланирован на 11:00. Мы любезно просим вас оставить ключи в специальном сейфе.",
            "Поблизости вы найдете Галерею Боргезе, один из самых красивых музеев Рима. Настоятельно рекомендую онлайн-бронирование, чтобы избежать очередей.",
            "Для регулировки температуры воды в душе поверните левую ручку по часовой стрелке, чтобы увеличить тепло. Если у вас возникнут проблемы, я к вашим услугам."
        ],
        'zh': [
            "当然！房子有高速WiFi。密码是'HadrianoLuxury2024'。如有任何技术问题，请随时与我们联系。",
            "最近推荐的餐厅是'La Pergola'，步行仅需10分钟。它提供令人惊叹的城市景观和星级美食。",
            "退房时间为上午11:00。我们恳请您将钥匙放在指定的保险箱中。",
            "附近您会发现博尔盖塞美术馆，罗马最美丽的博物馆之一。我强烈建议在线预订以避免排队。",
            "要调节淋浴水温，请顺时针旋转左侧旋钮以增加热量。如果您有任何问题，我随时为您服务。"
        ]
    }
    
    # Seleziona una risposta casuale nella lingua corretta
    import random
    if language in responses_by_language:
        return random.choice(responses_by_language[language])
    else:
        return random.choice(responses_by_language['en'])

def generate_booking_code():
    """Genera un codice prenotazione unico"""
    import uuid
    return str(uuid.uuid4())[:8].upper()

# ============================================================================
# STILI CSS PERSONALIZZATI
# ============================================================================

def inject_custom_css():
    """Inietta CSS personalizzato per un design di lusso"""
    st.markdown("""
    <style>
    /* Stili generali */
    .main {
        background-color: #f8f5f2;
    }
    
    /* Header elegante */
    .luxury-header {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        color: white;
        padding: 2rem;
        border-radius: 0 0 20px 20px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        margin-bottom: 2rem;
    }
    
    /* Card di lusso */
    .luxury-card {
        background-color: white;
        border-radius: 15px;
        padding: 1.5rem;
        box-shadow: 0 5px 20px rgba(0, 0, 0, 0.05);
        border: 1px solid #f0f0f0;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        margin-bottom: 1.5rem;
    }
    
    .luxury-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 30px rgba(0, 0, 0, 0.1);
    }
    
    /* Bottoni eleganti */
    .stButton > button {
        background: linear-gradient(135deg, #8B7355 0%, #A68A6F 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #A68A6F 0%, #8B7355 100%);
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(139, 115, 85, 0.3);
    }
    
    /* Badge di stato */
    .status-badge {
        display: inline-block;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.9rem;
    }
    
    .status-available {
        background-color: #e8f5e9;
        color: #2e7d32;
    }
    
    .status-busy {
        background-color: #ffebee;
        color: #c62828;
    }
    
    /* Input eleganti */
    .stTextInput > div > div > input {
        border-radius: 8px;
        border: 1px solid #e0e0e0;
        padding: 0.75rem;
    }
    
    .stSelectbox > div > div {
        border-radius: 8px;
    }
    
    /* Tabs eleganti */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
        background-color: transparent;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px 8px 0 0;
        padding: 0.75rem 1.5rem;
        font-weight: 500;
    }
    
    /* Immagine di copertina */
    .cover-image {
        width: 100%;
        height: 400px;
        object-fit: cover;
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
    }
    
    /* Chat AI */
    .chat-message {
        padding: 1rem;
        border-radius: 15px;
        margin-bottom: 1rem;
        max-width: 80%;
    }
    
    .user-message {
        background-color: #e8f5e9;
        margin-left: auto;
        border-bottom-right-radius: 5px;
    }
    
    .ai-message {
        background-color: #f5f5f5;
        margin-right: auto;
        border-bottom-left-radius: 5px;
    }
    
    /* Selettore lingua */
    .language-selector {
        background-color: white;
        border-radius: 10px;
        padding: 1rem;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.05);
        margin-bottom: 1.5rem;
    }
    
    /* Font personalizzati */
    h1, h2, h3, .luxury-font {
        font-family: 'Playfair Display', serif;
        color: #1a1a2e;
    }
    
    p, .standard-font {
        font-family: 'Inter', sans-serif;
        color: #555555;
    }
    
    /* Effetti speciali */
    .gold-text {
        background: linear-gradient(135deg, #D4AF37 0%, #FFD700 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem;
        color: #888888;
        font-size: 0.9rem;
        border-top: 1px solid #f0f0f0;
        margin-top: 3rem;
    }
    </style>
    """, unsafe_allow_html=True)

# ============================================================================
# COMPONENTI UI
# ============================================================================

def render_luxury_header(title, subtitle=None):
    """Render un header di lusso"""
    st.markdown(f"""
    <div class="luxury-header">
        <h1 style="margin: 0; font-size: 2.5rem;">{title}</h1>
        {f'<p style="margin: 0.5rem 0 0 0; font-size: 1.2rem; opacity: 0.9;">{subtitle}</p>' if subtitle else ''}
    </div>
    """, unsafe_allow_html=True)

def render_luxury_card(content, title=None):
    """Render una card di lusso"""
    card_html = '<div class="luxury-card">'
    if title:
        card_html += f'<h3 style="margin-top: 0; color: #1a1a2e;">{title}</h3>'
    card_html += f'{content}</div>'
    st.markdown(card_html, unsafe_allow_html=True)

def render_status_badge(available):
    """Render un badge di stato elegante"""
    if available:
        st.markdown('<div class="status-badge status-available">● ' + get_text("available") + '</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="status-badge status-busy">● ' + get_text("busy") + '</div>', unsafe_allow_html=True)

# ============================================================================
# PAGINE DELL'APPLICAZIONE
# ============================================================================

def login_page():
    """Pagina di login elegante"""
    render_luxury_header(get_text("app_title"), get_text("app_subtitle"))
    
    # Crea tre colonne per centrare il form di login
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        render_luxury_card(f"""
        <h2 style="text-align: center; color: #1a1a2e;">{get_text("login_title")}</h2>
        <p style="text-align: center; margin-bottom: 2rem;">{get_text("role_select")}</p>
        """)
        
        # Selezione ruolo
        role = st.selectbox(
            get_text("role_select"),
            [get_text("admin"), get_text("host"), get_text("guest")],
            key="role_select"
        )
        
        # Form di login in base al ruolo
        if role in [get_text("admin"), get_text("host")]:
            username = st.text_input(get_text("username"))
            password = st.text_input(get_text("password"), type="password")
            
            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                if st.button(get_text("login"), use_container_width=True):
                    # Verifica credenziali
                    if role == get_text("admin"):
                        # Verifica admin
                        for admin in st.session_state.admin_users:
                            if admin["username"] == username and admin["password"] == password:
                                st.session_state.logged_in = True
                                st.session_state.user_role = "admin"
                                st.session_state.username = username
                                st.rerun()
                                return
                    else:  # Host
                        # Verifica host
                        for host in st.session_state.hosts:
                            if host["username"] == username and host["password"] == password:
                                st.session_state.logged_in = True
                                st.session_state.user_role = "host"
                                st.session_state.username = username
                                st.rerun()
                                return
                    
                    st.error(get_text("invalid_login"))
            
            with col_btn2:
                if st.button("Demo Login", use_container_width=True):
                    # Accesso demo per testing
                    if role == get_text("admin"):
                        st.session_state.logged_in = True
                        st.session_state.user_role = "admin"
                        st.session_state.username = "admin"
                        st.rerun()
                    else:  # Host
                        st.session_state.logged_in = True
                        st.session_state.user_role = "host"
                        st.session_state.username = "host1"
                        st.rerun()
        
        else:  # Guest
            guest_code = st.text_input(get_text("guest_code"), placeholder="Es: A1B2C3D4")
            
            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                if st.button(get_text("enter"), use_container_width=True):
                    if guest_code in st.session_state.guest_codes:
                        st.session_state.logged_in = True
                        st.session_state.user_role = "guest"
                        st.session_state.current_apartment = st.session_state.guest_codes[guest_code]
                        st.rerun()
                    else:
                        st.error(get_text("invalid_code"))
            
            with col_btn2:
                if st.button("Demo Access", use_container_width=True):
                    # Accesso demo per testing
                    if not st.session_state.apartments:
                        # Crea un appartamento demo
                        demo_apartment = {
                            "id": 1,
                            "name": "Villa Adriana Luxury Suite",
                            "address": "Via Appia Antica, 123, Roma",
                            "cover_photo": "https://images.unsplash.com/photo-1613977257363-707ba9348227?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80",
                            "wifi": "Network: Hadriano_Guest | Password: Luxury2024",
                            "rules": "Check-in: 15:00 | Check-out: 11:00\nNo party\nNo smoking\nPets allowed with prior authorization",
                            "video": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
                        }
                        st.session_state.apartments.append(demo_apartment)
                    
                    demo_code = "DEMO1234"
                    st.session_state.guest_codes[demo_code] = st.session_state.apartments[0]
                    
                    st.session_state.logged_in = True
                    st.session_state.user_role = "guest"
                    st.session_state.current_apartment = st.session_state.apartments[0]
                    st.rerun()

def admin_dashboard():
    """Dashboard Amministratore"""
    render_luxury_header(f"{get_text('welcome')}, {get_text('admin')}", get_text('app_subtitle'))
    
    # Logout button in alto a destra
    col1, col2, col3 = st.columns([3, 1, 1])
    with col3:
        if st.button(get_text("logout")):
            st.session_state.logged_in = False
            st.session_state.user_role = None
            st.session_state.username = None
            st.rerun()
    
    # Tabs per le diverse funzionalità
    tab1, tab2, tab3, tab4 = st.tabs([
        get_text("apartments"),
        get_text("hosts"),
        get_text("points_of_interest"),
        get_text("guest_codes")
    ])
    
    # Tab 1: Gestione Appartamenti
    with tab1:
        st.subheader(get_text("add_apartment"))
        
        with st.form("add_apartment_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input(get_text("apartment_name"))
                address = st.text_area(get_text("address"))
                cover_photo = st.text_input(get_text("cover_photo"))
            
            with col2:
                wifi = st.text_area(get_text("wifi"))
                rules = st.text_area(get_text("rules"), height=150)
                video = st.text_input(get_text("video"))
            
            if st.form_submit_button(get_text("save")):
                if name and address:
                    new_apartment = {
                        "id": len(st.session_state.apartments) + 1,
                        "name": name,
                        "address": address,
                        "cover_photo": cover_photo if cover_photo else "https://images.unsplash.com/photo-1613977257363-707ba9348227?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80",
                        "wifi": wifi,
                        "rules": rules,
                        "video": video
                    }
                    st.session_state.apartments.append(new_apartment)
                    st.success(get_text("save_success"))
                    st.rerun()
        
        # Lista appartamenti esistenti
        st.subheader(get_text("apartments"))
        
        if not st.session_state.apartments:
            st.info(get_text("no_apartments"))
        else:
            for i, apt in enumerate(st.session_state.apartments):
                with st.expander(f"{apt['name']} - {apt['address']}"):
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.write(f"**{get_text('wifi')}:** {apt['wifi']}")
                        st.write(f"**{get_text('rules')}:**")
                        st.write(apt['rules'])
                        if apt['video']:
                            st.write(f"**{get_text('video_guide')}:** {apt['video']}")
                    
                    with col2:
                        if st.button(get_text("delete"), key=f"delete_apt_{i}"):
                            st.session_state.apartments.pop(i)
                            st.rerun()
    
    # Tab 2: Gestione Host
    with tab2:
        st.subheader(get_text("add_host"))
        
        with st.form("add_host_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                host_name = st.text_input(get_text("host_name"))
                host_email = st.text_input(get_text("host_email"))
            
            with col2:
                host_username = st.text_input(get_text("username"))
                host_password = st.text_input(get_text("password"), type="password")
            
            if st.form_submit_button(get_text("save")):
                if host_name and host_username and host_password:
                    new_host = {
                        "username": host_username,
                        "password": host_password,
                        "name": host_name,
                        "email": host_email,
                        "available": True
                    }
                    st.session_state.hosts.append(new_host)
                    st.success(get_text("save_success"))
                    st.rerun()
        
        # Lista host esistenti
        st.subheader(get_text("hosts"))
        
        if not st.session_state.hosts:
            st.info(get_text("no_hosts"))
        else:
            for i, host in enumerate(st.session_state.hosts):
                with st.expander(f"{host['name']} ({host['email']})"):
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.write(f"**{get_text('username')}:** {host['username']}")
                        render_status_badge(host['available'])
                    
                    with col2:
                        if st.button(get_text("delete"), key=f"delete_host_{i}"):
                            st.session_state.hosts.pop(i)
                            st.rerun()
    
    # Tab 3: Gestione Punti di Interesse
    with tab3:
        st.subheader(get_text("add_apartment"))
        
        # Seleziona appartamento per aggiungere POI
        if st.session_state.apartments:
            apt_options = [f"{apt['id']}. {apt['name']}" for apt in st.session_state.apartments]
            selected_apt = st.selectbox("Seleziona Appartamento", apt_options)
            apt_id = int(selected_apt.split(".")[0])
        else:
            st.info(get_text("no_apartments"))
            apt_id = None
        
        if apt_id:
            with st.form("add_poi_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    poi_name = st.text_input(get_text("poi_name"))
                    poi_type = st.selectbox(get_text("poi_type"), 
                                           [get_text("restaurants"), get_text("museums"), 
                                            get_text("shopping"), get_text("attractions")])
                    poi_address = st.text_input(get_text("poi_address"))
                
                with col2:
                    poi_description = st.text_area(get_text("poi_description"), height=150)
                    poi_map = st.text_input(get_text("poi_map"))
                
                if st.form_submit_button(get_text("save")):
                    if poi_name and poi_description:
                        new_poi = {
                            "id": len(st.session_state.points_of_interest) + 1,
                            "apartment_id": apt_id,
                            "name": poi_name,
                            "type": poi_type,
                            "description": poi_description,
                            "address": poi_address,
                            "map_url": poi_map
                        }
                        st.session_state.points_of_interest.append(new_poi)
                        st.success(get_text("save_success"))
                        st.rerun()
            
            # Lista POI per l'appartamento selezionato
            st.subheader(get_text("points_of_interest"))
            
            apt_pois = [poi for poi in st.session_state.points_of_interest if poi["apartment_id"] == apt_id]
            
            if not apt_pois:
                st.info(get_text("no_poi"))
            else:
                for i, poi in enumerate(apt_pois):
                    with st.expander(f"{poi['name']} ({poi['type']})"):
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            st.write(f"**{get_text('address')}:** {poi['address']}")
                            st.write(f"**{get_text('poi_description')}:** {poi['description']}")
                            if poi['map_url']:
                                st.write(f"**{get_text('poi_map')}:** {poi['map_url']}")
                        
                        with col2:
                            if st.button(get_text("delete"), key=f"delete_poi_{i}"):
                                st.session_state.points_of_interest.remove(poi)
                                st.rerun()
    
    # Tab 4: Visualizza Codici Ospiti
    with tab4:
        st.subheader(get_text("guest_codes"))
        
        if not st.session_state.guest_codes:
            st.info(get_text("no_codes"))
        else:
            for code, apartment in st.session_state.guest_codes.items():
                st.write(f"**Codice:** `{code}` → **Appartamento:** {apartment['name']}")

def host_dashboard():
    """Dashboard Host"""
    render_luxury_header(f"{get_text('welcome')}, {st.session_state.username}", get_text('app_subtitle'))
    
    # Logout button in alto a destra
    col1, col2, col3 = st.columns([3, 1, 1])
    with col3:
        if st.button(get_text("logout")):
            st.session_state.logged_in = False
            st.session_state.user_role = None
            st.session_state.username = None
            st.rerun()
    
    # Trova l'host corrente
    current_host = None
    for host in st.session_state.hosts:
        if host["username"] == st.session_state.username:
            current_host = host
            break
    
    if not current_host:
        st.error("Host non trovato")
        return
    
    # Layout a due colonne
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Selettore appartamenti (se l'host gestisce più appartamenti)
        if st.session_state.apartments:
            apt_options = [apt["name"] for apt in st.session_state.apartments]
            selected_apt_name = st.selectbox("Seleziona Appartamento", apt_options)
            selected_apt = next(apt for apt in st.session_state.apartments if apt["name"] == selected_apt_name)
        else:
            st.info(get_text("no_apartments"))
            selected_apt = None
        
        # Genera codici ospiti
        st.subheader(get_text("generate_codes"))
        
        if selected_apt:
            if st.button("Genera Nuovo Codice", use_container_width=True):
                new_code = generate_booking_code()
                st.session_state.guest_codes[new_code] = selected_apt
                st.success(f"{get_text('code_generated')}: **{new_code}**")
                st.code(new_code, language="text")
        
        # Visualizza codici esistenti
        if st.session_state.guest_codes:
            st.subheader("Codici Generati")
            for code, apt in st.session_state.guest_codes.items():
                if apt["name"] == selected_apt_name:
                    st.write(f"`{code}` → {apt['name']}")
    
    with col2:
        # Stato disponibilità
        st.subheader(get_text("availability"))
        
        current_status = current_host.get("available", True)
        
        col_status1, col_status2 = st.columns(2)
        
        with col_status1:
            if st.button("🟢 " + get_text("available"), use_container_width=True, 
                        type="primary" if current_status else "secondary"):
                current_host["available"] = True
                st.success(get_text("status_green"))
                st.rerun()
        
        with col_status2:
            if st.button("🔴 " + get_text("busy"), use_container_width=True,
                        type="primary" if not current_status else "secondary"):
                current_host["available"] = False
                st.success(get_text("status_red"))
                st.rerun()
        
        # Visualizza stato attuale
        st.markdown("---")
        if current_status:
            render_status_badge(True)
            st.write(get_text("status_green"))
        else:
            render_status_badge(False)
            st.write(get_text("status_red"))
        
        # Info host
        st.markdown("---")
        st.subheader("Le Tue Informazioni")
        st.write(f"**Nome:** {current_host['name']}")
        st.write(f"**Email:** {current_host['email']}")

def guest_dashboard():
    """Dashboard Ospite - Con interfaccia multilingua"""
    
    # Selettore lingua solo per gli ospiti
    st.sidebar.markdown('<div class="language-selector">', unsafe_allow_html=True)
    st.sidebar.subheader(get_text("select_language"))
    
    language_options = {
        "it": get_text("italian"),
        "en": get_text("english"),
        "es": get_text("spanish"),
        "fr": get_text("french"),
        "de": get_text("german"),
        "ru": get_text("russian"),
        "zh": get_text("chinese")
    }
    
    current_lang_code = st.session_state.current_language
    
    # Crea pulsanti per ogni lingua
    cols = st.sidebar.columns(3)
    lang_buttons = []
    
    for idx, (code, name) in enumerate(language_options.items()):
        col_idx = idx % 3
        with cols[col_idx]:
            # Evidenzia la lingua corrente
            if code == current_lang_code:
                if st.button(name, use_container_width=True, type="primary"):
                    st.session_state.current_language = code
                    st.rerun()
            else:
                if st.button(name, use_container_width=True):
                    st.session_state.current_language = code
                    st.rerun()
    
    st.sidebar.markdown('</div>', unsafe_allow_html=True)
    
    # Logout button nella sidebar
    st.sidebar.markdown("---")
    if st.sidebar.button(get_text("logout"), use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.user_role = None
        st.session_state.username = None
        st.session_state.current_apartment = None
        st.rerun()
    
    # Contenuto principale
    apartment = st.session_state.current_apartment
    
    if not apartment:
        st.error("Nessun appartamento selezionato")
        return
    
    # Header con immagine di copertina
    render_luxury_header(apartment["name"], get_text("app_subtitle"))
    
    if apartment.get("cover_photo"):
        st.image(apartment["cover_photo"], use_column_width=True, caption=apartment["name"])
    
    # Tabs per le diverse sezioni
    tab1, tab2, tab3, tab4 = st.tabs([
        get_text("home"),
        get_text("local_guide"),
        get_text("ai_concierge"),
        get_text("assistance")
    ])
    
    # Tab 1: Home - Informazioni casa
    with tab1:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            render_luxury_card(f"""
            <h3>{get_text("house_info")}</h3>
            <p><strong>{get_text("address")}:</strong> {apartment["address"]}</p>
            """)
            
            # WiFi in evidenza
            render_luxury_card(f"""
            <h3>🔗 {get_text("wifi_details")}</h3>
            <p style="font-family: monospace; font-size: 1.1rem; background: #f5f5f5; padding: 1rem; border-radius: 8px;">
            {apartment.get("wifi", "Non disponibile")}
            </p>
            """)
        
        with col2:
            # Regole della casa
            render_luxury_card(f"""
            <h3>📋 {get_text("house_rules")}</h3>
            <p style="white-space: pre-line;">{apartment.get("rules", "Nessuna regola specificata")}</p>
            """)
            
            # Video guide
            if apartment.get("video"):
                render_luxury_card(f"""
                <h3>🎥 {get_text("video_guide")}</h3>
                <p><a href="{apartment['video']}" target="_blank">Guarda il video di benvenuto</a></p>
                """)
    
    # Tab 2: Guida Local
    with tab2:
        if st.session_state.points_of_interest:
            # Filtra POI per questo appartamento
            apt_pois = [poi for poi in st.session_state.points_of_interest 
                       if poi.get("apartment_id") == apartment.get("id")]
            
            if apt_pois:
                # Raggruppa per tipo
                poi_by_type = {}
                for poi in apt_pois:
                    poi_type = poi.get("type", get_text("attractions"))
                    if poi_type not in poi_by_type:
                        poi_by_type[poi_type] = []
                    poi_by_type[poi_type].append(poi)
                
                # Visualizza per tipo
                for poi_type, pois in poi_by_type.items():
                    st.subheader(poi_type)
                    
                    for poi in pois:
                        with st.expander(f"📍 {poi['name']}"):
                            st.write(f"**{get_text('address')}:** {poi.get('address', 'N/A')}")
                            st.write(f"**{get_text('poi_description')}:** {poi.get('description', 'Nessuna descrizione')}")
                            
                            if poi.get("map_url"):
                                st.write(f"**{get_text('poi_map')}:** [Apri mappa]({poi['map_url']})")
            else:
                st.info(f"Nessun punto di interesse ancora aggiunto per {apartment['name']}")
        else:
            st.info("L'amministratore non ha ancora aggiunto punti di interesse per questa zona.")
    
    # Tab 3: Concierge AI
    with tab3:
        st.subheader("🤖 Hadriano " + get_text("ai_concierge"))
        st.caption(get_text("ask_hadriano"))
        
        # Area chat
        chat_container = st.container(height=400)
        
        with chat_container:
            for message in st.session_state.chat_history[-10:]:  # Mostra ultimi 10 messaggi
                if message["role"] == "user":
                    st.markdown(f"""
                    <div class="chat-message user-message">
                        <strong>Tu:</strong> {message["content"]}
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="chat-message ai-message">
                        <strong>Hadriano:</strong> {message["content"]}
                    </div>
                    """, unsafe_allow_html=True)
        
        # Input per nuova domanda
        col_input, col_btn = st.columns([4, 1])
        
        with col_input:
            user_question = st.text_input(get_text("type_question"), label_visibility="collapsed", 
                                         placeholder=get_text("type_question"))
        
        with col_btn:
            if st.button(get_text("send"), use_container_width=True) and user_question:
                # Aggiungi domanda alla cronologia
                st.session_state.chat_history.append({
                    "role": "user",
                    "content": user_question
                })
                
                # Simula risposta AI
                ai_response = get_gemini_response(user_question, st.session_state.current_language)
                
                # Aggiungi risposta alla cronologia
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": ai_response
                })
                
                st.rerun()
    
    # Tab 4: Assistenza
    with tab4:
        st.subheader(get_text("assistance"))
        
        # Trova host disponibile
        available_hosts = [host for host in st.session_state.hosts if host.get("available", False)]
        
        if available_hosts:
            host = available_hosts[0]  # Prendi il primo host disponibile
            
            render_luxury_card(f"""
            <h3>✅ {get_text("host_available")}</h3>
            <p><strong>{get_text("host_name")}:</strong> {host.get('name', 'Host')}</p>
            <p><strong>Email:</strong> {host.get('email', 'N/A')}</p>
            """)
            
            # Pulsanti di contatto
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("📞 " + get_text("call_host"), use_container_width=True):
                    st.info(f"Chiamando {host.get('name')}... (simulazione)")
                    # In un'app reale qui si aprirebbe il dialer del telefono
            
            with col2:
                if st.button("💬 " + get_text("whatsapp_host"), use_container_width=True):
                    st.info(f"Apertura WhatsApp per {host.get('name')}... (simulazione)")
                    # In un'app reale qui si aprirebbe WhatsApp
            
            # Informazioni aggiuntive
            st.markdown("---")
            st.info("Per assistenza immediata, puoi anche chiamare il nostro supporto 24/7 al numero: +39 06 1234 5678")
        else:
            render_luxury_card(f"""
            <h3>⏳ {get_text("assistance")}</h3>
            <p>Al momento nessun host è disponibile. Il nostro team ti contatterà appena possibile.</p>
            <p>Per emergenze, chiama il supporto 24/7: <strong>+39 06 1234 5678</strong></p>
            """)

# ============================================================================
# APPLICAZIONE PRINCIPALE
# ============================================================================

def main():
    """Funzione principale dell'applicazione"""
    
    # Inizializza session state
    initialize_session_state()
    
    # Inietta CSS personalizzato
    inject_custom_css()
    
    # Controlla stato login e mostra la pagina appropriata
    if not st.session_state.logged_in:
        login_page()
    else:
        if st.session_state.user_role == "admin":
            admin_dashboard()
        elif st.session_state.user_role == "host":
            host_dashboard()
        elif st.session_state.user_role == "guest":
            guest_dashboard()
    
    # Footer
    st.markdown("""
    <div class="footer">
        <p>Hadriano Concierge © 2024 | Luxury Edition Multilingua</p>
        <p>L'arte dell'ospitalità di lusso</p>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# AVVIO APPLICAZIONE
# ============================================================================

if __name__ == "__main__":
    main()
