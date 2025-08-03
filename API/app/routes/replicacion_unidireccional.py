from fastapi import APIRouter, HTTPException, Query
from app.services.replicacion_unidireccional_service import ReplicacionUnidireccionalService
from app.services.replicacion_quito_cuenca_service import ReplicacionQuitoCuencaService

router = APIRouter(prefix="/replicacion-unidireccional", tags=["Replicación Unidireccional"])

@router.post("/quito-cuenca")
async def replicacion_quito_cuenca(
    cantidad: int = Query(default=2, ge=1, le=5, description="Cantidad de películas a insertar en Quito")
):
    """🎬 REPLICACIÓN UNIDIRECCIONAL: Quito → Cuenca (catalogo_peliculas)
    
    - Inserta películas en Quito 
    - Verifica replicación unidireccional hacia Cuenca
    - Retorna contenido completo de ambas tablas antes/después
    """
    try:
        service = ReplicacionQuitoCuencaService()
        resultado = await service.evidenciar_replicacion_quito_cuenca(cantidad_peliculas=cantidad)
        
        return {
            "success": True,
            "message": "Replicación unidireccional Quito → Cuenca completada",
            "tablas_antes": {
                "quito_peliculas": resultado["estado_inicial"]["quito_peliculas"],
                "cuenca_peliculas": resultado["estado_inicial"]["cuenca_peliculas"]
            },
            "operacion": {
                "cantidad_insertada": cantidad,
                "registros_insertados": resultado["operacion"]["detalles"]
            },
            "tablas_despues": {
                "quito_peliculas": resultado["estado_final"]["quito_peliculas"],
                "cuenca_peliculas": resultado["estado_final"]["cuenca_peliculas"]
            },
            "resumen": {
                "quito_antes": len(resultado["estado_inicial"]["quito_peliculas"]),
                "quito_despues": len(resultado["estado_final"]["quito_peliculas"]),
                "cuenca_antes": len(resultado["estado_inicial"]["cuenca_peliculas"]),
                "cuenca_despues": len(resultado["estado_final"]["cuenca_peliculas"]),
                "replicacion_exitosa": resultado["evidencia_replicacion"]["replicacion_exitosa"]
            }
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error en replicación Quito-Cuenca: {str(e)}"
        )

@router.post("/guayaquil-cuenca")
async def replicacion_guayaquil_cuenca(
    cantidad: int = Query(default=2, ge=1, le=5, description="Cantidad de películas a insertar en Guayaquil")
):
    """🎬 REPLICACIÓN UNIDIRECCIONAL: Guayaquil → Cuenca (catalogo_peliculas)
    
    - Inserta películas en Guayaquil
    - Verifica replicación unidireccional hacia Cuenca
    - Retorna contenido completo de ambas tablas antes/después
    """
    try:
        # Para mostrar Guayaquil y Cuenca necesitamos consultar ambas bases
        from app.services.replicacion_quito_cuenca_service import ReplicacionQuitoCuencaService
        
        # Obtener estado inicial de ambas tablas
        service_gye = ReplicacionUnidireccionalService()
        service_cuenca = ReplicacionQuitoCuencaService()
        
        # Estado inicial
        guayaquil_antes = await service_gye.consultar_peliculas_nodo(2)  # DB2 = Guayaquil
        cuenca_antes = service_cuenca.consultar_peliculas_cuenca()
        
        # Insertar en Guayaquil
        peliculas_insertadas = await service_gye.insertar_peliculas_guayaquil(cantidad)
        
        # Esperar replicación
        import asyncio
        await asyncio.sleep(3)
        
        # Estado final
        guayaquil_despues = await service_gye.consultar_peliculas_nodo(2)  # DB2 = Guayaquil
        cuenca_despues = service_cuenca.consultar_peliculas_cuenca()
        
        return {
            "success": True,
            "message": "Replicación unidireccional Guayaquil → Cuenca completada",
            "tablas_antes": {
                "guayaquil_peliculas": guayaquil_antes,
                "cuenca_peliculas": cuenca_antes
            },
            "operacion": {
                "cantidad_insertada": cantidad,
                "registros_insertados": peliculas_insertadas
            },
            "tablas_despues": {
                "guayaquil_peliculas": guayaquil_despues,
                "cuenca_peliculas": cuenca_despues
            },
            "resumen": {
                "guayaquil_antes": len(guayaquil_antes),
                "guayaquil_despues": len(guayaquil_despues),
                "cuenca_antes": len(cuenca_antes),
                "cuenca_despues": len(cuenca_despues),
                "replicacion_exitosa": (len(guayaquil_despues) - len(guayaquil_antes)) == (len(cuenca_despues) - len(cuenca_antes)) == cantidad
            }
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error en replicación Guayaquil-Cuenca: {str(e)}"
        )
