from scraping.scripts.productos import scrapear_productos_notas
from app.crud.notas_venta import sincronizar_notas_venta
from scraping.scripts.scraper import ScrapingObuma as so
from scraping.config.config import OBUMA_CONFIG, OBUMA_TIKETS
from app.database.db import SessionLocal
import asyncio

data = so(**OBUMA_CONFIG)
df = data.extraer_datos()

if not df.empty:
    db = SessionLocal()
    try:
        sincronizar_notas_venta(df, db)
        asyncio.run(scrapear_productos_notas(db, OBUMA_TIKETS))
    finally:
        db.close()
else:
    print("No se obtubo información del Scrapíng")
