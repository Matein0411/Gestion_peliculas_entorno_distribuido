from typing import List, Dict
from app.database.postgres_connection import PostgresConnection
import logging

logger = logging.getLogger(__name__)

class EmpleadosVistaCompletaService:
    """Servicio para consultar empleados con fragmentos verticales unidos (Quito + Guayaquil)"""
    
    def __init__(self):
        # Usar nodo de Quito que tiene la vista que une ambos fragmentos
        self.postgres_conn = PostgresConnection(db_number=1)
    
    async def get_all_empleados_completos(self) -> List[Dict]:
        """
        Obtiene todos los empleados con datos completos usando la vista que une
        fragmentos verticales de Quito (datos principales) y Guayaquil (datos complementarios)
        """
        try:
            async with self.postgres_conn.get_session() as session:
                # Consultar la vista que une los fragmentos verticales
                query = """
                SELECT 
                    empleado_id,
                    nombre,
                    apellido,
                    cargo,
                    ciudad_tienda,
                    salario,
                    fecha_contratacion,
                    contacto_emergencia
                FROM empleados_vista_completa
                ORDER BY empleado_id
                """
                
                result = await session.execute(query)
                empleados = []
                
                for row in result.fetchall():
                    empleado = {
                        "empleado_id": row[0],
                        "nombre": row[1],
                        "apellido": row[2],
                        "cargo": row[3],
                        "ciudad_tienda": row[4],
                        "salario": float(row[5]) if row[5] else None,
                        "fecha_contratacion": str(row[6]) if row[6] else None,
                        "contacto_emergencia": row[7]
                    }
                    empleados.append(empleado)
                
                logger.info(f"✅ Obtenidos {len(empleados)} empleados de la vista completa")
                return empleados
                
        except Exception as e:
            logger.error(f"❌ Error obteniendo empleados completos: {e}")
            raise Exception(f"Error al consultar empleados: {str(e)}")
