import time
import requests
from requests.exceptions import RequestException
from bs4 import BeautifulSoup

from scraper.ocr import ocr_check_status

MAX_RETRIES = 3
BACKOFF_FACTOR = 2


def request_with_retries(session, method, url, **kwargs):
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = session.request(method, url, timeout=10, **kwargs)
            response.raise_for_status()
            return response
        except RequestException as e:
            if attempt == MAX_RETRIES:
                raise
            sleep_time = BACKOFF_FACTOR ** (attempt - 1)
            print(f'Tentativa {attempt} falhou para {url}: {e}. Tentando novamente em {sleep_time}s...')
            time.sleep(sleep_time)


def get_detail_image_url(detail_url, session=None):
    if session is None:
        session = requests.Session()

    full_url = 'https://cna.oab.org.br' + detail_url
    response = request_with_retries(session, 'GET', full_url)

    try:
        data_json = response.json()
    except ValueError:
        print('Resposta JSON inválida em get_detail_image_url')
        return None

    if data_json.get('Success') and 'Data' in data_json:
        detail_img_url = data_json['Data'].get('DetailUrl')
        if detail_img_url:
            return 'https://cna.oab.org.br' + detail_img_url

    return None


def get_verification_token(session, url='https://cna.oab.org.br/'):
    response = request_with_retries(session, 'GET', url)
    soup = BeautifulSoup(response.text, 'html.parser')
    token = soup.find('input', {'name': '__RequestVerificationToken'})
    return token.get('value') if token else None


def search_oab(nome=None, inscricao=None, uf=None, tipo_inscricao=None):
    session = requests.Session()

    token = get_verification_token(session)
    if not token:
        raise Exception('Verification token not found')

    url = 'https://cna.oab.org.br/Home/Search'

    payload = {
        '__RequestVerificationToken': token,
        'IsMobile': 'false',
        'NomeAdvo': nome or "",
        'Insc': inscricao or "",
        'Uf': uf or "",
        'TipoInsc': str(tipo_inscricao) if tipo_inscricao else "",
    }

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Referer': 'https://cna.oab.org.br/',
        'User-Agent': 'Mozilla/5.0 (compatible)'
    }

    response = request_with_retries(session, 'POST', url, data=payload, headers=headers)

    try:
        json_data = response.json()
    except ValueError:
        raise ValueError('Resposta JSON inválida na busca principal.')

    results = json_data.get('Data', [])

    if not results:
        raise ValueError('Nenhum advogado encontrado com os critérios informados.')

    processed = []
    for entry in results:
        detail_url = get_detail_image_url(entry.get('DetailUrl', ""))
        status = ocr_check_status(detail_url) if detail_url else 'STATUS NÃO IDENTIFICADO'

        processed.append({
            'oab': entry.get('Inscricao', ""),
            'nome': entry.get('Nome', ""),
            'uf': entry.get('UF', ""),
            'categoria': entry.get('TipoInscOab', ""),
            'situacao': status
        })

    return processed
