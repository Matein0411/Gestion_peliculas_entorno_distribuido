from fastapi import APIRouter, HTTPException
from app.services.peliculas_completas_service import PeliculasCompletasService
from typing import List

router = APIRouter(prefix="/peliculas-completas", tags=["Películas Completas"])

@router.get("/", response_model=List[dict])
async def get_peliculas_completas():
    """Obtiene todas las películas con información completa (datos de Quito y Guayaquil)"""
    try:
        service = PeliculasCompletasService()
        peliculas = await service.get_all_peliculas_completas()
        return peliculas
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
