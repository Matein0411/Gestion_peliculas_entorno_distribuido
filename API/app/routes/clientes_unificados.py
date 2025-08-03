from fastapi import APIRouter, HTTPException
from app.services.clientes_unificados_service import ClientesUnificadosService
from typing import List

router = APIRouter(prefix="/clientes-unificados", tags=["Clientes Unificados"])

@router.get("/", response_model=List[dict])
async def get_clientes_unificados():
    """Obtiene todos los clientes de las tres ciudades (Cuenca, Quito, Guayaquil)"""
    try:
        service = ClientesUnificadosService()
        clientes = await service.get_all_clientes_unificados()
        return clientes
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
