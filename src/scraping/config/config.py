from dotenv import load_dotenv
import os


load_dotenv()

# Configuración de Insuma 
OBUMA_CONFIG = {
    "url_scraping":os.getenv("BASE_URL_OBUMA"),
    "user_obuma": os.getenv("OBUMA_USER"),
    "password": os.getenv("OBUMA_PASSWORD"),
    "user_agent": os.getenv("OBUMA_AGENT")
}

OBUMA_TIKETS = os.getenv("URL_TICKETS")