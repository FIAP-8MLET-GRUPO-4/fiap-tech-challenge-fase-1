# api/services/scraper_service.py
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
import random
import re
import logging
import sys
import os
from sqlalchemy.orm import Session
from api.models.books import Book, Category 

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Configurações locais do scraper
BASE_URL = "http://books.toscrape.com/"
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

DEFAULT_LIMIT = int(os.getenv("SCRAPER_LIMIT", 0))

def get_categories():
    logger.info("--- [1/4] Mapeando categorias... ---")
    try:
        response = requests.get(BASE_URL, headers=HEADERS)
        soup = BeautifulSoup(response.text, "html.parser")
        sidebar = soup.find("div", class_="side_categories")
        links = sidebar.find("ul").find("li").find("ul").find_all("a")
        cat_map = []
        for link in links:
            cat_map.append({"name": link.text.strip(), "url": urljoin(BASE_URL, link["href"])})
        return cat_map
    except Exception as e:
        logger.error(f"Erro ao mapear: {e}")
        return []


def get_books_raw(categories_map, limit=None):
    # Define qual limite usar: O da API (se vier) ou o Padrão do Ambiente
    effective_limit = limit if limit is not None else DEFAULT_LIMIT
    
    logger.info(f"\n--- [2/4] Iniciando Coleta (Limite: {effective_limit if effective_limit > 0 else 'Todos'}) ---")
    
    raw_data = []
    for cat in categories_map:
        count_cat = 0
        current_url = cat['url']
        while True:
            
            if effective_limit > 0 and count_cat >= effective_limit: break
            try:
                resp = requests.get(current_url, headers=HEADERS)
                if resp.status_code != 200:
                    logger.warning(f"Falha ao acessar {current_url}: Status {resp.status_code}")
                    break
                
                soup = BeautifulSoup(resp.text, "html.parser")
                pods = soup.find_all("article", class_="product_pod")
                
                for pod in pods:
                    if effective_limit > 0 and count_cat >= effective_limit: break
                    book_url = urljoin(current_url, pod.h3.a["href"])
                    time.sleep(random.uniform(0.5, 1.0))
                    b_resp = requests.get(book_url, headers=HEADERS)
                    b_resp.encoding = 'utf-8'
                    if b_resp.status_code == 200:
                        bs = BeautifulSoup(b_resp.text, "html.parser")
                        table = bs.find("table", class_="table table-striped")
                        rows = {r.find("th").text: r.find("td").text for r in table.find_all("tr")}
                        desc_div = bs.find("div", id="product_description")

                        title = bs.find("h1").text
                        logger.info(f"   + Coletado: {title[:30]}...") 

                        raw_data.append({
                            'raw_title': title,
                            'raw_upc': rows.get("UPC"),
                            'raw_desc': desc_div.find_next_sibling("p").text if desc_div else None,
                            'raw_price': rows.get("Price (incl. tax)"),
                            'raw_availability': rows.get("Availability"),
                            'raw_rating': bs.find("p", class_="star-rating")["class"][1],
                            'raw_url': book_url,
                            'raw_img': bs.find("div", class_="item active").find("img")["src"],
                            'cat_ref_name': cat['name']
                        })
                        count_cat += 1
                next_tag = soup.find("li", class_="next")
                if next_tag: current_url = urljoin(current_url, next_tag.find("a")["href"])
                else: break
            except Exception as e:
                logger.error(f"Erro durante extração: {e}")
                break
    return raw_data

def exec_etl(raw_data_list):
    logger.info(f"\n--- [3/4] Executando ETL ---")
    clean_data = []
    mapa_stars = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}
    for item in raw_data_list:
        try:
            url_id = int(item['raw_url'].split('_')[-1].split('/')[0])
            preco_str = item['raw_price']
            price = float(re.sub(r'[^\d.]', '', preco_str)) if preco_str else 0.0
            est_str = item['raw_availability']
            match = re.search(r'(\d+)', est_str)
            quantity = int(match.group(1)) if match else 0
            rating = mapa_stars.get(item['raw_rating'], 0)
            img_full_url = urljoin(BASE_URL, item['raw_img'])
            clean_data.append({
                'id': url_id,
                'title': item['raw_title'],
                'upc': item['raw_upc'],
                'description': item['raw_desc'],
                'price': price,
                'rating': rating,
                'quantity': quantity,
                'availability': quantity > 0,
                'imagem_url': img_full_url,
                'category_name': item['cat_ref_name']
            })
        except Exception as e: 
            logger.warning(f"Falha no ETL do item {item.get('raw_title', 'Unknown')}: {e}")
            pass
    return clean_data


def load_database(clean_data, db: Session):
    """
    Recebe os dados limpos e a sessão do banco (injetada pelo FastAPI).
    """
    logger.info("\n--- [4/4] Salvando no Banco de Dados ---")
    try:
        
        cats_unique = set(d['category_name'] for d in clean_data)
        cat_db_map = {}
        
        # Log de progresso
        logger.info(f"Sincronizando {len(cats_unique)} categorias...")

        for c_name in cats_unique:
            
            obj = db.query(Category).filter_by(name=c_name).first()
            if not obj:
                obj = Category(name=c_name)
                db.add(obj)
                db.commit() 
                db.refresh(obj)
            cat_db_map[c_name] = obj.id
            
        logger.info(f"Inserindo/Atualizando {len(clean_data)} livros...")

        count = 0
        for item in clean_data:
            book = Book(
                id=item['id'],
                upc=item['upc'],
                title=item['title'],
                description=item['description'],
                price=item['price'],
                rating=item['rating'],
                quantity=item['quantity'],
                availability=item['availability'],
                imagem_url=item['imagem_url'],
                category_id=cat_db_map[item['category_name']]
            )
            db.merge(book)
            count += 1
            
        db.commit() # Commit final
        logger.info(f"Sucesso! {count} livros salvos.")
        return {"status": "success", "imported": count}
        
    except Exception as e:
        db.rollback()
        logger.critical(f"Erro crítico no banco: {e}")
        return {"status": "error", "detail": str(e)}

# Função Orquestradora
def run_scraper_pipeline(db: Session, limit: int = None):
    cats = get_categories()
    if not cats: return {"status": "error", "detail": "No categories found"}
    
    raw = get_books_raw(cats, limit=limit)
    if not raw: return {"status": "error", "detail": "No books extracted"}
    
    clean = exec_etl(raw)
    result = load_database(clean, db)
    return result