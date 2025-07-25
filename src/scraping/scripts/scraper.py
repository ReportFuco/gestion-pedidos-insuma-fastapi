from bs4 import BeautifulSoup
import requests
import pandas as pd
import re


class ScrapingObuma:
    def __init__(
            self,
            url_scraping:str,
            user_obuma:str,
            password:str,
            user_agent:str
        ):
        
        self.url = url_scraping
        self.user = user_obuma
        self.password = password
        self.agent = user_agent


    @property
    def credencials(self):
        return {
            "rut": self.user,
            "clave": self.password,
            "remember": "1",
            "source": ""
        }
    
    @staticmethod
    def extraer_id_obuma(link_str):
        match = re.search(r'id=(\d+)', str(link_str))
        if match:
            return int(match.group(1))
        return None
    
    @staticmethod
    def extract_table_data(soup):
        """Extrae los datos de la tabla y los devuelve como lista de diccionarios"""
        tabla = soup.find('table', class_='table boo-table table-striped table-hover')
        if not tabla:
            return None
        
        # Extraer encabezados
        headers = [th.get_text(strip=True) for th in tabla.find('thead').find_all('th')]
        
        # Extraer filas de datos
        rows = []
        for tr in tabla.find('tbody').find_all('tr'):
            cells = tr.find_all('td')
            row_data = {}
            
            for i, header in enumerate(headers):
                if i >= len(cells):
                    continue
                    
                cell = cells[i]
                text = cell.get_text(strip=True)
                
                if header == 'CLIENTE RS':
                    link = cell.find('a')
                    if link:
                        row_data['CLIENTE_ID'] = link['href'].split('id=')[-1] if 'id=' in link['href'] else ''
                        text = link.get_text(strip=True)
                
                row_data[header] = text
            
            acciones = cells[-1]
            links = {}
            for a in acciones.find_all('a'):
                if 'popup_pdf' in a.get('class', []):
                    links[a.get_text(strip=True)] = a['href']
            row_data['LINKS'] = links
            
            rows.append(row_data)
        
        return rows
    
    def extraer_datos(self)->pd.DataFrame:
        with requests.session() as session:

            session.headers.update({
                "User-Agent": self.agent,
                "Referer": self.url,
                "Origin": "https://app.obuma.cl"
            })

            session.get(self.url)

            login_response = session.post(f"{self.url}/usuario-login.php", data=self.credencials, allow_redirects=True)

            if "home.php" in login_response.url or "Cerrar sesión" in login_response.text:
                response = session.get(f"{self.url}/home.php?page=mod-ventas/notas-de-venta/listar")
                soup = BeautifulSoup(response.text, 'html.parser')

                table = self.extract_table_data(soup)

                if table:

                    df = pd.DataFrame(table)
                    df["ID_OBUMA"] = df["LINKS"].apply(self.extraer_id_obuma)
                    
                    rename_map = {
                        "FOLIO": "folio",
                        "FECHA": "fecha",
                        "CLIENTE_ID": "cliente_id",
                        "CLIENTE RS": "cliente_rs",
                        "VENDEDOR": "vendedor",
                        "SUCURSAL": "sucursal",
                        "NETO": "neto",
                        "ESTADO": "estado",
                        "ID_OBUMA": "obuma_id"
                    }

                    df = df.rename(columns=rename_map)
                    df = df[list(rename_map.values())]
                    df["fecha"] = pd.to_datetime(df["fecha"], dayfirst=True, errors="coerce").dt.date
                    df["neto"] = (
                        df["neto"]
                        .astype(str)
                        .str.strip()
                        .str.replace(r'[\$,]', '', regex=True)
                        .str.replace('.', '', regex=False)
                        .astype(int)
                    )
                    return df
            else:
                print("❌ Login fallido")
                return pd.DataFrame()