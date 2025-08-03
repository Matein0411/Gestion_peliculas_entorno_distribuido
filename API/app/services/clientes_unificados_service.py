from typing import List
from app.database.postgres_connection import PostgresConnection
import logging

logger = logging.getLogger(__name__)

class ClientesUnificadosService:
    """Servicio para consultar la vista unificada de clientes de todas las ciudades"""
    
    def __init__(self):
        # Usamos Quito (PostgreSQL 1) donde está la vista
        self.postgres_conn = PostgresConnection(db_number=1)
    
    async def get_all_clientes_unificados(self) -> List[dict]:
        """Obtiene todos los clientes de la vista unificada (Cuenca, Quito, Guayaquil)"""
        try:
            async with self.postgres_conn.get_session() as session:
                query = """
                SELECT cliente_id, nombre, apellido, email, telefono, 
                       direccion, ciudad_registro, fecha_creacion
                FROM vista_clientes_unificados
                ORDER BY fecha_creacion DESC
                """
                result = await session.execute(query)
                rows = result.fetchall()
                
                clientes = []
                for row in rows:
                    cliente = {
                        "cliente_id": row[0],
                        "nombre": row[1],
                        "apellido": row[2],
                        "email": row[3],
                        "telefono": row[4],
                        "direccion": row[5],
                        "ciudad_registro": row[6],
                        "fecha_creacion": row[7]
                    }
                    clientes.append(cliente)
                
                return clientes
                
        except Exception as e:
            logger.error(f"Error obteniendo clientes unificados: {e}")
            raise Exception(f"Error al consultar vista unificada: {str(e)}")
