from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List

from scraper.extractor import search_oab
from api.models import OABRequest, OABResponse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.get('/')
async def root():
    return {'message': 'OAB Scraper API is running'}


@app.post('/fetch_oab', response_model=List[OABResponse])
async def fetch_oab(request: OABRequest):
    try:
        results = search_oab(
            inscricao=request.oab,
            nome=request.name,
            uf=request.uf,
            tipo_inscricao=request.categoria,
        )
        return results
        
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Erro interno no servidor: {e}')
    