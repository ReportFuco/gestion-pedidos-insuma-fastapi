from app.crud.productos import get_productos_id, insert_productos
from app.crud.notas_venta import get_notas_obuma_id
from bs4 import BeautifulSoup
from io import StringIO
import pandas as pd
import asyncio
import aiohttp


async def fetch_and_parse(session, id_obuma:int, base_url:str):
    url = f"{base_url}?id={id_obuma}"
    try:
        async with session.get(url) as response:
            if response.status != 200:
                print(f"❌ Error al acceder a {url}")
                return None
            html = await response.text()
            soup = BeautifulSoup(html, 'html.parser')
            tabla = soup.find('table', class_='table')
            if tabla:
                df = pd.read_html(StringIO(str(tabla)))[0]
                df['id_obuma'] = id_obuma
                return df
    except Exception as e:
        print(f"❌ Error con nota {id_obuma}: {e}")
        return None

async def scrapear_productos_notas(db, url:str):
    lista_notas = get_notas_obuma_id(db)
    lista_productos = get_productos_id(db)
    faltantes = list(set(lista_notas) - set(lista_productos))
    print(f"🔍 Notas sin productos: {faltantes}")

    if not faltantes:
        print("✅ Todas las notas ya fueron procesadas.")
        return

    async with aiohttp.ClientSession() as session:
        tasks = [fetch_and_parse(session, id_nota, base_url=url) for id_nota in faltantes]
        results = await asyncio.gather(*tasks)

        productos = [df for df in results if df is not None]

        if productos:
            df_global = pd.concat(productos, ignore_index=True)
            df_global.columns = ['item', 'cantidad', 'subtotal', 'id_obuma']

            df_global['subtotal'] = (
                df_global['subtotal']
                .astype(str)
                .str.strip()
                .str.replace('.', '', regex=False)
                .astype(int)
            )

            df_global = df_global[['id_obuma', 'item', 'cantidad', 'subtotal']]

            # ⬇️ Inserta todo el DataFrame
            insert_productos(db, df_global)

            return faltantes

        else:
            print("⚠️ No se encontraron productos.")
