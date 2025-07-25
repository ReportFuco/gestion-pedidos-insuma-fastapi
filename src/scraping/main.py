from app.crud.notas_venta import sincronizar_notas_venta
from scraping.scripts.scraper import ScrapingObuma as so
from scraping.config.config import OBUMA_CONFIG
from app.database.db import SessionLocal


data = so(**OBUMA_CONFIG)
df = data.extraer_datos()

if not df.empty:
    db = SessionLocal()
    try:
        sincronizar_notas_venta(df, db)
    finally:
        db.close()
else:
    print("No se obtubo información del Scrapíng")
