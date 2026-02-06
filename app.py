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
    page_title="Luxury Concierge",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================================
# DIZIONARI MULTILINGUA
# ============================================================================

translations = {
    "it": {
        "app_title": "Luxury Concierge",
        "app_subtitle": "L'esperienza dell'ospitalità di lusso",
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
        "ask_hadriano": "Chiedi al Concierge",
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
        "delete_success": "Eliminato con successo",
        "assign_host": "Assegna Host",
        "select_host": "Seleziona Host",
        "unassigned": "Non assegnato"
    },
    "en": {
        "app_title": "Luxury Concierge",
        "app_subtitle": "The Luxury Hospitality Experience",
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
        "ask_hadriano": "Ask the Concierge",
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
        "delete_success": "Deleted successfully",
        "assign_host": "Assign Host",
        "select_host": "Select Host",
        "unassigned": "Unassigned"
    },
    "es": {
        "app_title": "Luxury Concierge",
        "app_subtitle": "La experiencia de hospitalidad de lujo",
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
        "ask_hadriano": "Pregunta al Concierge",
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
        "delete_success": "Eliminado con éxito",
        "assign_host": "Asignar Anfitrión",
        "select_host": "Seleccionar Anfitrión",
        "unassigned": "No asignado"
    },
    "fr": {
        "app_title": "Luxury Concierge",
        "app_subtitle": "L'expérience de l'hospitalité de luxe",
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
        "ask_hadriano": "Demandez au Concierge",
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
        "delete_success": "Supprimé avec succès",
        "assign_host": "Attribuer un Hôte",
        "select_host": "Sélectionner un Hôte",
        "unassigned": "Non attribué"
    },
    "de": {
        "app_title": "Luxury Concierge",
        "app_subtitle": "Das Luxus-Gastfreundschaftserlebnis",
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
        "ask_hadriano": "Fragen Sie den Concierge",
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
        "delete_success": "Erfolgreich gelöscht",
        "assign_host": "Gastgeber zuweisen",
        "select_host": "Gastgeber auswählen",
        "unassigned": "Nicht zugewiesen"
    },
    "ru": {
        "app_title": "Luxury Concierge",
        "app_subtitle": "Опыт роскошного гостеприимства",
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
        "ask_hadriano": "Спросите Консьержа",
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
        "delete_success": "Успешно удалено",
        "assign_host": "Назначить хоста",
        "select_host": "Выбрать хоста",
        "unassigned": "Не назначено"
    },
    "zh": {
        "app_title": "Luxury Concierge",
        "app_subtitle": "奢华款待体验",
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
        "ask_hadriano": "询问礼宾",
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
        "delete_success": "删除成功",
        "assign_host": "分配房东",
        "select_host": "选择房东",
        "unassigned": "未分配"
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
            {"username": "host1", "password": "host123", "name": "Marco Rossi", "email": "marco@luxury.com", "available": True},
            {"username": "host2", "password": "host456", "name": "Anna Bianchi", "email": "anna@luxury.com", "available": False}
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
            "Certamente! La casa dispone di WiFi ad alta velocità. La password è 'LuxuryConcierge2024'. Per qualsiasi problema tecnico, non esiti a contattarci.",
            "Il ristorante più vicino consigliato è 'La Pergola', a soli 10 minuti a piedi. Offre una vista mozzafiato sulla città e una cucina stellata.",
            "Il check-out è previsto per le 11:00. Le chiediamo gentilmente di lasciare le chiavi nell'apposita cassetta di sicurezza.",
            "Nelle vicinanze troverà la Galleria Borghese, uno dei musei più belli di Roma. Consiglio vivamente la prenotazione online per evitare code.",
            "Per la temperatura dell'acqua della doccia, giri la manopola sinistra in senso orario per aumentare il calore. Se dovesse avere problemi, sono a disposizione."
        ],
        'en': [
            "Certainly! The house has high-speed WiFi. The password is 'LuxuryConcierge2024'. For any technical issues, please do not hesitate to contact us.",
            "The nearest recommended restaurant is 'La Pergola', just a 10-minute walk away. It offers a breathtaking view of the city and starred cuisine.",
            "Check-out is scheduled for 11:00 AM. We kindly ask you to leave the keys in the designated safety box.",
            "Nearby you will find the Borghese Gallery, one of the most beautiful museums in Rome. I highly recommend online booking to avoid queues.",
            "For the shower water temperature, turn the left knob clockwise to increase heat. If you have any problems, I am available."
        ],
        'es': [
            "¡Por supuesto! La casa tiene WiFi de alta velocidad. La contraseña es 'LuxuryConcierge2024'. Para cualquier problema técnico, no dude en contactarnos.",
            "El restaurante recomendado más cercano es 'La Pergola', a solo 10 minutos a pie. Ofrece una vista impresionante de la ciudad y una cocina estrellada.",
            "El check-out está programado para las 11:00. Le rogamos que deje las llaves en la caja de seguridad designada.",
            "Cerca encontrará la Galería Borghese, uno de los museos más bellos de Roma. Recomiendo encarecidamente la reserva en línea para evitar colas.",
            "Para la temperatura del agua de la ducha, gire la perilla izquierda en el sentido de las agujas del reloj para aumentar el calor. Si tiene algún problema, estoy disponible."
        ],
        'fr': [
            "Certainement! La maison dispose d'un WiFi haute vitesse. Le mot de passe est 'LuxuryConcierge2024'. Pour tout problème technique, n'hésitez pas à nous contacter.",
            "Le restaurant recommandé le plus proche est 'La Pergola', à seulement 10 minutes à pied. Il offre une vue imprenable sur la ville et une cuisine étoilée.",
            "Le check-out est prévu pour 11h00. Nous vous demandons gentiment de laisser les clés dans la boîte de sécurité désignée.",
            "À proximité, vous trouverez la Galerie Borghese, l'un des plus beaux musées de Rome. Je recommande vivement la réservation en ligne pour éviter les files d'attente.",
            "Pour la température de l'eau de la douche, tournez le bouton gauche dans le sens des aiguilles d'une montre pour augmenter la chaleur. Si vous avez des problèmes, je suis disponible."
        ],
        'de': [
            "Sicherlich! Das Haus verfügt über High-Speed-WLAN. Das Passwort lautet 'LuxuryConcierge2024'. Bei technischen Problemen zögern Sie bitte nicht, uns zu kontaktieren.",
            "Das nächstgelegene empfohlene Restaurant ist 'La Pergola', nur 10 Gehminuten entfernt. Es bietet einen atemberaubenden Blick auf la città e Sterneküche.",
            "Der Check-out ist für 11:00 Uhr geplant. Wir bitten Sie freundlich, die Schlüssel in der dafür vorgesehenen Sicherheitsbox zu hinterlassen.",
            "In der Nähe finden Sie die Galleria Borghese, eines der schönsten Museen Roms. Ich empfehle dringend die Online-Buchung, um Warteschlangen zu vermeiden.",
            "Für die Duschtemperatur drehen Sie den linken Knopf im Uhrzeigersinn, um die Wärme zu erhöhen. Bei Problemen stehe ich zur Verfügung."
        ],
        'ru': [
            "Конечно! В доме есть высокоскоростной WiFi. Пароль 'LuxuryConcierge2024'. По любым техническим вопросам, пожалуйста, не стесняйтесь обращаться к нам.",
            "Ближайший рекомендуемый ресторан - 'La Pergola', всего в 10 минутах ходьбы. Он предлагает захватывающий вид на город и звездную кухню.",
            "Выезд запланирован на 11:00. Мы любезно просим вас оставить ключи в специальном сейфе.",
            "Поблизости вы найдете Галерею Боргезе, один из самых красивых музеев Рима. Настоятельно рекомендую онлайн-бронирование, чтобы избежать очередей.",
            "Для регулировки температуры воды в душе поверните левую ручку по часовой стрелке, чтобы увеличить тепло. Если у вас возникнут проблемы, я к вашим услугам."
        ],
        'zh': [
            "当然！房子有高速WiFi。密码是'LuxuryConcierge2024'。如有任何技术问题，请随时与我们联系。",
            "最近推荐的餐厅是'La Pergola'，步行仅需10分钟。它提供令人惊叹的城市景观和星级美食。",
            "退房时间为上午11:00。我们恳请您将钥匙放在指定的保险箱中。",
            "附近您会发现博尔盖塞美术馆，罗马最美丽的博物馆之一。我强烈建议在线预订以避免排队。",
            "要调节淋浴水温，请顺时针旋转左侧旋钮以增加热量。如果您有任何问题，我随时为您服务。"
        ]
    }
    
    # Seleziona una risposta casuale nella lingua corretta
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
        background: linear-gradient(135deg, #0c0c14 0%, #1a1a2e 100%);
        color: white;
        padding: 2rem;
        border-radius: 0 0 20px 20px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
    }
    
    .luxury-header::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #D4AF37 0%, #FFD700 50%, #D4AF37 100%);
    }
    
    /* Card di lusso */
    .luxury-card {
        background-color: white;
        border-radius: 15px;
        padding: 2rem;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.08);
        border: 1px solid #e8e8e8;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        margin-bottom: 1.5rem;
        position: relative;
        overflow: hidden;
    }
    
    .luxury-card::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 4px;
        background: linear-gradient(90deg, #8B7355 0%, #A68A6F 100%);
    }
    
    .luxury-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.12);
    }
    
    /* Bottoni eleganti */
    .stButton > button {
        background: linear-gradient(135deg, #8B7355 0%, #A68A6F 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.85rem 1.75rem;
        font-weight: 500;
        font-size: 0.95rem;
        transition: all 0.3s ease;
        letter-spacing: 0.5px;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #A68A6F 0%, #8B7355 100%);
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(139, 115, 85, 0.3);
    }
    
    /* Badge di stato */
    .status-badge {
        display: inline-block;
        padding: 0.6rem 1.2rem;
        border-radius: 25px;
        font-weight: 600;
        font-size: 0.9rem;
        letter-spacing: 0.5px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .status-available {
        background: linear-gradient(135deg, #4CAF50 0%, #66BB6A 100%);
        color: white;
    }
    
    .status-busy {
        background: linear-gradient(135deg, #F44336 0%, #EF5350 100%);
        color: white;
    }
    
    /* Input eleganti */
    .stTextInput > div > div > input {
        border-radius: 10px;
        border: 1px solid #e0e0e0;
        padding: 0.85rem;
        font-size: 0.95rem;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #8B7355;
        box-shadow: 0 0 0 2px rgba(139, 115, 85, 0.1);
    }
    
    .stSelectbox > div > div {
        border-radius: 10px;
    }
    
    /* Tabs eleganti */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0;
        background-color: transparent;
        border-bottom: 2px solid #f0f0f0;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px 10px 0 0;
        padding: 1rem 2rem;
        font-weight: 500;
        color: #666;
        transition: all 0.3s ease;
        border-bottom: 3px solid transparent;
    }
    
    .stTabs [aria-selected="true"] {
        color: #8B7355;
        border-bottom: 3px solid #8B7355;
        background-color: rgba(139, 115, 85, 0.05);
    }
    
    /* Immagine di copertina */
    .cover-image {
        width: 100%;
        height: 450px;
        object-fit: cover;
        border-radius: 20px;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.15);
        transition: transform 0.5s ease;
    }
    
    .cover-image:hover {
        transform: scale(1.01);
    }
    
    /* Chat AI */
    .chat-message {
        padding: 1.2rem;
        border-radius: 18px;
        margin-bottom: 1.2rem;
        max-width: 80%;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        line-height: 1.5;
    }
    
    .user-message {
        background: linear-gradient(135deg, #E8F5E9 0%, #F1F8E9 100%);
        margin-left: auto;
        border-bottom-right-radius: 5px;
        border-left: 4px solid #4CAF50;
    }
    
    .ai-message {
        background: linear-gradient(135deg, #F5F5F5 0%, #FAFAFA 100%);
        margin-right: auto;
        border-bottom-left-radius: 5px;
        border-left: 4px solid #8B7355;
    }
    
    /* Selettore lingua con bandierine */
    .language-selector {
        position: fixed;
        top: 20px;
        left: 20px;
        z-index: 1000;
    }
    
    .language-flag {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        background: white;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
        cursor: pointer;
        transition: all 0.3s ease;
        border: 2px solid white;
    }
    
    .language-flag:hover {
        transform: scale(1.1);
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.2);
    }
    
    .language-dropdown {
        position: absolute;
        top: 50px;
        left: 0;
        background: white;
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
        padding: 0.5rem;
        min-width: 180px;
        display: none;
    }
    
    .language-option {
        display: flex;
        align-items: center;
        padding: 0.8rem 1rem;
        border-radius: 10px;
        cursor: pointer;
        transition: all 0.2s ease;
        margin: 0.2rem 0;
    }
    
    .language-option:hover {
        background-color: #f5f5f5;
    }
    
    .language-option.active {
        background-color: rgba(139, 115, 85, 0.1);
        color: #8B7355;
        font-weight: 500;
    }
    
    /* Welcome grande */
    .welcome-title {
        font-size: 4.5rem;
        font-weight: 300;
        color: #1a1a2e;
        text-align: center;
        margin: 2rem 0;
        letter-spacing: 2px;
        position: relative;
    }
    
    .welcome-subtitle {
        font-size: 1.5rem;
        color: #8B7355;
        text-align: center;
        margin-bottom: 3rem;
        font-weight: 400;
        letter-spacing: 1px;
    }
    
    /* Icone di lusso */
    .luxury-icon {
        font-size: 2.5rem;
        margin-bottom: 1rem;
        display: block;
        text-align: center;
    }
    
    /* Info card eleganti */
    .info-card {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 5px 20px rgba(0, 0, 0, 0.05);
        border-left: 4px solid #8B7355;
    }
    
    /* Animazioni */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .fade-in {
        animation: fadeIn 0.6s ease-out;
    }
    
    /* Font personalizzati */
    h1, h2, h3, .luxury-font {
        font-family: 'Playfair Display', serif;
        color: #1a1a2e;
    }
    
    p, .standard-font {
        font-family: 'Inter', sans-serif;
        color: #555555;
        line-height: 1.6;
    }
    
    /* Effetti speciali */
    .gold-text {
        background: linear-gradient(135deg, #D4AF37 0%, #FFD700 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 600;
    }
    
    /* Scrollbar personalizzata */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #8B7355 0%, #A68A6F 100%);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #A68A6F 0%, #8B7355 100%);
    }
    </style>
    """, unsafe_allow_html=True)

# ============================================================================
# COMPONENTI UI
# ============================================================================

def render_luxury_header(title, subtitle=None):
    """Render un header di lusso"""
    st.markdown(f"""
    <div class="luxury-header fade-in">
        <h1 style="margin: 0; font-size: 2.8rem; letter-spacing: 1px;">{title}</h1>
        {f'<p style="margin: 0.5rem 0 0 0; font-size: 1.3rem; opacity: 0.9; font-weight: 300;">{subtitle}</p>' if subtitle else ''}
    </div>
    """, unsafe_allow_html=True)

def render_luxury_card(content, title=None):
    """Render una card di lusso"""
    card_html = '<div class="luxury-card fade-in">'
    if title:
        card_html += f'<h3 style="margin-top: 0; color: #1a1a2e; font-size: 1.4rem; margin-bottom: 1.5rem;">{title}</h3>'
    card_html += f'{content}</div>'
    st.markdown(card_html, unsafe_allow_html=True)

def render_status_badge(available):
    """Render un badge di stato elegante"""
    if available:
        st.markdown('<div class="status-badge status-available">● ' + get_text("available") + '</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="status-badge status-busy">● ' + get_text("busy") + '</div>', unsafe_allow_html=True)

def render_language_selector():
    """Render il selettore lingua con bandierina"""
    flag_emojis = {
        "it": "🇮🇹",
        "en": "🇺🇸",
        "es": "🇪🇸",
        "fr": "🇫🇷",
        "de": "🇩🇪",
        "ru": "🇷🇺",
        "zh": "🇨🇳"
    }
    
    language_names = {
        "it": "Italiano",
        "en": "English",
        "es": "Español",
        "fr": "Français",
        "de": "Deutsch",
        "ru": "Русский",
        "zh": "中文"
    }
    
    current_lang = st.session_state.current_language
    current_flag = flag_emojis.get(current_lang, "🌐")
    
    # Inietta HTML per il selettore lingua
    st.markdown(f"""
    <div class="language-selector">
        <div class="language-flag" id="language-flag">
            {current_flag}
        </div>
        <div class="language-dropdown" id="language-dropdown">
            {"".join([f'''
            <div class="language-option {'active' if lang == current_lang else ''}" data-lang="{lang}">
                <span style="font-size: 1.2rem; margin-right: 10px;">{flag}</span>
                <span>{name}</span>
            </div>
            ''' for lang, flag in flag_emojis.items() for name in [language_names[lang]]])}
        </div>
    </div>
    
    <script>
        const flagElement = document.getElementById('language-flag');
        const dropdown = document.getElementById('language-dropdown');
        
        flagElement.addEventListener('click', function() {{
            dropdown.style.display = dropdown.style.display === 'block' ? 'none' : 'block';
        }});
        
        document.querySelectorAll('.language-option').forEach(option => {{
            option.addEventListener('click', function() {{
                const lang = this.getAttribute('data-lang');
                // Invia il linguaggio selezionato a Streamlit
                const streamlitEvent = new CustomEvent('languageChange', {{ detail: {{ language: lang }} }});
                window.parent.document.dispatchEvent(streamlitEvent);
            }});
        }});
        
        // Chiudi dropdown cliccando fuori
        document.addEventListener('click', function(event) {{
            if (!flagElement.contains(event.target) && !dropdown.contains(event.target)) {{
                dropdown.style.display = 'none';
            }}
        }});
    </script>
    """, unsafe_allow_html=True)
    
    # Ascolta eventi JavaScript per cambiare lingua
    if st.session_state.get('language_changed'):
        st.session_state.current_language = st.session_state.language_changed
        del st.session_state.language_changed
        st.rerun()

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
        <h2 style="text-align: center; color: #1a1a2e; margin-bottom: 0.5rem;">{get_text("login_title")}</h2>
        <p style="text-align: center; margin-bottom: 2rem; color: #666;">{get_text("role_select")}</p>
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
                            "name": "Villa Luxury Suite",
                            "address": "Via Appia Antica, 123, Roma",
                            "cover_photo": "https://images.unsplash.com/photo-1613977257363-707ba9348227?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80",
                            "wifi": "Network: Luxury_Guest | Password: Luxury2024",
                            "rules": "Check-in: 15:00 | Check-out: 11:00\nNo party\nNo smoking\nPets allowed with prior authorization",
                            "video": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                            "host_username": "host1"
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
        if st.button(get_text("logout"), use_container_width=True):
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
                cover_photo = st.text_input(get_text("cover_photo"), 
                                           value="https://images.unsplash.com/photo-1613977257363-707ba9348227?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80")
            
            with col2:
                wifi = st.text_area(get_text("wifi"), value="Network: Luxury_Guest | Password: Luxury2024")
                rules = st.text_area(get_text("rules"), height=150, 
                                    value="Check-in: 15:00 | Check-out: 11:00\nNo party\nNo smoking\nPets allowed with prior authorization")
                video = st.text_input(get_text("video"), value="https://www.youtube.com/watch?v=dQw4w9WgXcQ")
            
            # Assegnazione host
            st.markdown("---")
            st.subheader(get_text("assign_host"))
            
            host_options = [get_text("unassigned")] + [host["username"] for host in st.session_state.hosts]
            selected_host = st.selectbox(get_text("select_host"), host_options)
            
            if st.form_submit_button(get_text("save"), use_container_width=True):
                if name and address:
                    new_apartment = {
                        "id": len(st.session_state.apartments) + 1,
                        "name": name,
                        "address": address,
                        "cover_photo": cover_photo,
                        "wifi": wifi,
                        "rules": rules,
                        "video": video,
                        "host_username": selected_host if selected_host != get_text("unassigned") else None
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
                with st.expander(f"🏠 {apt['name']} - {apt['address']}"):
                    col1, col2, col3 = st.columns([3, 1, 1])
                    with col1:
                        st.write(f"**{get_text('wifi')}:** {apt['wifi']}")
                        st.write(f"**{get_text('rules')}:**")
                        st.write(apt['rules'])
                        if apt['video']:
                            st.write(f"**{get_text('video_guide')}:** {apt['video']}")
                        
                        # Mostra host assegnato
                        if apt.get('host_username'):
                            assigned_host = next((h for h in st.session_state.hosts if h['username'] == apt['host_username']), None)
                            if assigned_host:
                                st.write(f"**{get_text('assign_host')}:** {assigned_host['name']} ({assigned_host['username']})")
                    
                    with col2:
                        if apt.get('cover_photo'):
                            st.image(apt['cover_photo'], width=200)
                    
                    with col3:
                        if st.button(get_text("delete"), key=f"delete_apt_{i}", use_container_width=True):
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
            
            if st.form_submit_button(get_text("save"), use_container_width=True):
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
                with st.expander(f"👤 {host['name']} ({host['email']})"):
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.write(f"**{get_text('username')}:** {host['username']}")
                        render_status_badge(host['available'])
                        
                        # Mostra appartamenti assegnati
                        assigned_apartments = [apt for apt in st.session_state.apartments 
                                              if apt.get('host_username') == host['username']]
                        if assigned_apartments:
                            st.write(f"**Appartamenti assegnati:**")
                            for apt in assigned_apartments:
                                st.write(f"- {apt['name']}")
                    
                    with col2:
                        if st.button(get_text("delete"), key=f"delete_host_{i}", use_container_width=True):
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
                
                if st.form_submit_button(get_text("save"), use_container_width=True):
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
                    with st.expander(f"📍 {poi['name']} ({poi['type']})"):
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            st.write(f"**{get_text('address')}:** {poi['address']}")
                            st.write(f"**{get_text('poi_description')}:** {poi['description']}")
                            if poi['map_url']:
                                st.write(f"**{get_text('poi_map')}:** {poi['map_url']}")
                        
                        with col2:
                            if st.button(get_text("delete"), key=f"delete_poi_{i}", use_container_width=True):
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
    """Dashboard Host - SEMPLIFICATA senza impostazioni"""
    render_luxury_header(f"{get_text('welcome')}, {st.session_state.username}", get_text('app_subtitle'))
    
    # Solo logout in alto a destra, nessun altro menu
    col1, col2 = st.columns([4, 1])
    with col2:
        if st.button(get_text("logout"), use_container_width=True):
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
    
    # Mostra solo gli appartamenti assegnati a questo host
    host_apartments = [apt for apt in st.session_state.apartments 
                      if apt.get('host_username') == st.session_state.username]
    
    if not host_apartments:
        render_luxury_card(f"""
        <div style="text-align: center; padding: 2rem;">
            <div class="luxury-icon">🏠</div>
            <h3>Nessun Appartamento Assegnato</h3>
            <p>Attendi che l'amministratore ti assegni degli appartamenti.</p>
        </div>
        """)
        return
    
    # Layout principale per host
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Selettore appartamenti
        apt_options = [apt["name"] for apt in host_apartments]
        selected_apt_name = st.selectbox("Seleziona Appartamento", apt_options)
        selected_apt = next(apt for apt in host_apartments if apt["name"] == selected_apt_name)
        
        # Genera codici ospiti
        st.subheader(get_text("generate_codes"))
        
        if st.button("Genera Nuovo Codice", use_container_width=True):
            new_code = generate_booking_code()
            st.session_state.guest_codes[new_code] = selected_apt
            st.success(f"{get_text('code_generated')}: **{new_code}**")
        
        # Visualizza codici esistenti per questo appartamento
        if st.session_state.guest_codes:
            st.subheader("Codici Generati")
            for code, apt in st.session_state.guest_codes.items():
                if apt["name"] == selected_apt_name:
                    st.write(f"`{code}`")
    
    with col2:
        # Stato disponibilità - design elegante
        render_luxury_card(f"""
        <div style="text-align: center;">
            <div class="luxury-icon">📱</div>
            <h3>{get_text("availability")}</h3>
        </div>
        """)
        
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

def guest_dashboard():
    """Dashboard Ospite - Interfaccia completamente rinnovata"""
    
    # Selettore lingua con bandierina in alto a sinistra
    render_language_selector()
    
    apartment = st.session_state.current_apartment
    
    if not apartment:
        st.error("Nessun appartamento selezionato")
        return
    
    # Immagine di copertina in grande
    if apartment.get("cover_photo"):
        st.image(apartment["cover_photo"], use_column_width=True, caption=apartment["name"])
    
    # Welcome gigante e elegante
    st.markdown(f"""
    <div class="welcome-title fade-in">
        WELCOME
    </div>
    <div class="welcome-subtitle fade-in">
        to {apartment["name"]}
    </div>
    """, unsafe_allow_html=True)
    
    # Tabs per le diverse sezioni - design migliorato
    tab1, tab2, tab3, tab4 = st.tabs([
        "🏠 " + get_text("home"),
        "🗺️ " + get_text("local_guide"),
        "🤖 " + get_text("ai_concierge"),
        "📞 " + get_text("assistance")
    ])
    
    # Tab 1: Home - Informazioni casa con design migliorato
    with tab1:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Card informazioni casa
            render_luxury_card(f"""
            <div style="display: flex; align-items: center; margin-bottom: 1.5rem;">
                <div style="font-size: 2rem; margin-right: 1rem;">🏡</div>
                <div>
                    <h4 style="margin: 0; color: #1a1a2e;">{get_text("house_info")}</h4>
                    <p style="margin: 0.5rem 0 0 0; color: #666;">{apartment["address"]}</p>
                </div>
            </div>
            """)
            
            # WiFi in evidenza con design elegante
            render_luxury_card(f"""
            <div style="display: flex; align-items: center; margin-bottom: 1.5rem;">
                <div style="font-size: 2rem; margin-right: 1rem;">🌐</div>
                <div>
                    <h4 style="margin: 0; color: #1a1a2e;">{get_text("wifi_details")}</h4>
                </div>
            </div>
            <div style="background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); 
                        padding: 1.5rem; border-radius: 10px; border-left: 4px solid #4CAF50;">
                <p style="margin: 0; font-family: 'Courier New', monospace; font-size: 1.1rem; 
                        font-weight: 500; color: #333;">
                {apartment.get("wifi", "WiFi non disponibile")}
                </p>
            </div>
            """)
        
        with col2:
            # Regole della casa in card elegante
            render_luxury_card(f"""
            <div style="display: flex; align-items: center; margin-bottom: 1.5rem;">
                <div style="font-size: 2rem; margin-right: 1rem;">📋</div>
                <div>
                    <h4 style="margin: 0; color: #1a1a2e;">{get_text("house_rules")}</h4>
                </div>
            </div>
            <div style="background: #f8f9fa; padding: 1rem; border-radius: 8px; max-height: 200px; overflow-y: auto;">
                <p style="white-space: pre-line; margin: 0; color: #555; line-height: 1.6;">
                {apartment.get("rules", get_text("no_apartments"))}
                </p>
            </div>
            """)
            
            # Video guide se disponibile
            if apartment.get("video"):
                render_luxury_card(f"""
                <div style="display: flex; align-items: center; margin-bottom: 1.5rem;">
                    <div style="font-size: 2rem; margin-right: 1rem;">🎥</div>
                    <div>
                        <h4 style="margin: 0; color: #1a1a2e;">{get_text("video_guide")}</h4>
                    </div>
                </div>
                <p style="text-align: center;">
                    <a href="{apartment['video']}" target="_blank" style="
                        display: inline-block;
                        padding: 0.8rem 1.5rem;
                        background: linear-gradient(135deg, #8B7355 0%, #A68A6F 100%);
                        color: white;
                        text-decoration: none;
                        border-radius: 10px;
                        font-weight: 500;
                        transition: all 0.3s ease;
                    " onmouseover="this.style.transform='translateY(-2px)'; this.style.boxShadow='0 5px 15px rgba(139, 115, 85, 0.3)';"
                    onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='none';">
                        ▶️ Guarda il Video
                    </a>
                </p>
                """)
    
    # Tab 2: Guida Local con design migliorato
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
                
                # Visualizza per tipo con design elegante
                for poi_type, pois in poi_by_type.items():
                    st.subheader(f"📍 {poi_type}")
                    
                    for poi in pois:
                        render_luxury_card(f"""
                        <div style="margin-bottom: 1rem;">
                            <h4 style="margin: 0 0 0.5rem 0; color: #1a1a2e;">{poi['name']}</h4>
                            <p style="margin: 0 0 0.5rem 0; color: #666;">
                                <strong>📍 {get_text('address')}:</strong> {poi.get('address', 'N/A')}
                            </p>
                            <p style="margin: 0; color: #555;">{poi.get('description', 'Nessuna descrizione')}</p>
                        </div>
                        {f'<p style="margin-top: 0.5rem;"><a href="{poi["map_url"]}" target="_blank" style="color: #8B7355; text-decoration: none; font-weight: 500;">🗺️ {get_text("poi_map")}</a></p>' if poi.get("map_url") else ''}
                        """, title=None)
            else:
                render_luxury_card(f"""
                <div style="text-align: center; padding: 2rem;">
                    <div class="luxury-icon">🗺️</div>
                    <h3>Guida Local in Arrivo</h3>
                    <p>L'amministratore sta preparando le migliori raccomandazioni per {apartment['name']}.</p>
                </div>
                """)
        else:
            render_luxury_card(f"""
            <div style="text-align: center; padding: 2rem;">
                <div class="luxury-icon">🗺️</div>
                <h3>Scopri la Zona</h3>
                <p>Presto troverai qui i migliori ristoranti, musei e attrazioni della zona.</p>
            </div>
            """)
    
    # Tab 3: Concierge AI con design migliorato
    with tab3:
        render_luxury_card(f"""
        <div style="text-align: center; margin-bottom: 2rem;">
            <div class="luxury-icon">🤖</div>
            <h3>Concierge AI</h3>
            <p style="color: #666;">{get_text("ask_hadriano")}</p>
        </div>
        """)
        
        # Area chat migliorata
        chat_container = st.container(height=400)
        
        with chat_container:
            if not st.session_state.chat_history:
                st.markdown(f"""
                <div style="text-align: center; padding: 3rem 1rem;">
                    <div style="font-size: 3rem; margin-bottom: 1rem;">👋</div>
                    <h4 style="color: #1a1a2e; margin-bottom: 1rem;">Ciao! Sono il tuo Concierge Virtuale</h4>
                    <p style="color: #666; max-width: 500px; margin: 0 auto;">
                        Chiedimi qualsiasi cosa sulla casa, sul WiFi, sulle regole 
                        o sui migliori posti da visitare nella zona. Sono qui per aiutarti!
                    </p>
                </div>
                """, unsafe_allow_html=True)
            else:
                for message in st.session_state.chat_history[-10:]:  # Mostra ultimi 10 messaggi
                    if message["role"] == "user":
                        st.markdown(f"""
                        <div class="chat-message user-message fade-in">
                            <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
                                <div style="width: 32px; height: 32px; border-radius: 50%; 
                                            background: linear-gradient(135deg, #4CAF50 0%, #66BB6A 100%); 
                                            display: flex; align-items: center; justify-content: center; 
                                            margin-right: 10px; color: white; font-weight: bold;">T</div>
                                <strong>Tu</strong>
                            </div>
                            <div style="color: #333;">{message["content"]}</div>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                        <div class="chat-message ai-message fade-in">
                            <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
                                <div style="width: 32px; height: 32px; border-radius: 50%; 
                                            background: linear-gradient(135deg, #8B7355 0%, #A68A6F 100%); 
                                            display: flex; align-items: center; justify-content: center; 
                                            margin-right: 10px; color: white; font-weight: bold;">C</div>
                                <strong>Concierge</strong>
                            </div>
                            <div style="color: #333;">{message["content"]}</div>
                        </div>
                        """, unsafe_allow_html=True)
        
        # Input per nuova domanda con design migliorato
        col_input, col_btn = st.columns([4, 1])
        
        with col_input:
            user_question = st.text_input(
                get_text("type_question"), 
                label_visibility="collapsed", 
                placeholder=get_text("type_question")
            )
        
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
    
    # Tab 4: Assistenza - VUOTA come richiesto
    with tab4:
        # Lasciamo vuoto come richiesto
        pass

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
    
    # NOTA: Footer rimosso come richiesto

# ============================================================================
# AVVIO APPLICAZIONE
# ============================================================================

if __name__ == "__main__":
    main()
