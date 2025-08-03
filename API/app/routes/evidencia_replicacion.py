from fastapi import APIRouter, HTTPException
from app.services.promociones_service import PromocionesService
from typing import Dict

router = APIRouter(tags=["Replicación Bidireccional"])

@router.post("/replicacion-bidireccional")
async def evidenciar_replicacion_bidireccional(
    nodo_para_insertar: str,
    cantidad_registros: int
):
    """ EVIDENCIA REPLICACIÓN BIDIRECCIONAL: Consulta ambos promociones GYE - UIO ANTES/DESPUÉS de insertar"""
    try:
        if nodo_para_insertar not in ["Quito", "Guayaquil"]:
            raise HTTPException(status_code=400, detail="NodoParaInsertar debe ser 'Quito' o 'Guayaquil'")
        
        if cantidad_registros < 1 or cantidad_registros > 50:
            raise HTTPException(status_code=400, detail="Cantidad debe estar entre 1 y 50")
            
        service = PromocionesService(nodo_insercion=nodo_para_insertar)
        evidencia = await service.evidenciar_replicacion_bidireccional(cantidad_registros)
        return evidencia
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
