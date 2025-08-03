from fastapi import APIRouter, HTTPException
from app.services.empleados_vista_completa_service import EmpleadosVistaCompletaService
from typing import List

router = APIRouter(prefix="/empleados-vista-completa", tags=["Empleados Vista Completa"])

@router.get("/", response_model=List[dict])
async def get_empleados_vista_completa():
    """Obtiene empleados con fragmentos verticales unidos (Quito + Guayaquil)"""
    try:
        service = EmpleadosVistaCompletaService()
        empleados = await service.get_all_empleados_completos()
        return empleados
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
