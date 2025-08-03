from fastapi import APIRouter, HTTPException
from app.services.replicacion_unidireccional_service import ReplicacionUnidireccionalService

router = APIRouter(prefix="/replicacion-unidireccional", tags=["Replicación Unidireccional"])

@router.post("/test-peliculas")
async def test_replicacion_unidireccional_peliculas(
    cantidad_peliculas: int = 2
):
    """🎬 TEST REPLICACIÓN UNIDIRECCIONAL: Guayaquil → Quito (películas)"""
    try:
        if cantidad_peliculas < 1 or cantidad_peliculas > 10:
            raise HTTPException(status_code=400, detail="Cantidad debe estar entre 1 y 10")
            
        service = ReplicacionUnidireccionalService()
        resultado = await service.evidenciar_replicacion_unidireccional(cantidad_peliculas)
        return resultado
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
