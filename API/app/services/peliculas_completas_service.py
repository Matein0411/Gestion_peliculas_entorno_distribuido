from typing import List
from app.database.postgres_connection import PostgresConnection
import logging

logger = logging.getLogger(__name__)

class PeliculasCompletasService:
    """Servicio para consultar la vista de películas completas"""
    
    def __init__(self):
        # Usamos Quito (PostgreSQL 1) donde está la vista
        self.postgres_conn = PostgresConnection(db_number=1)
    
    async def get_all_peliculas_completas(self) -> List[dict]:
        """Obtiene todas las películas con información completa"""
        try:
            async with self.postgres_conn.get_session() as session:
                query = """
                SELECT pelicula_id, titulo, genero, clasificacion, director, 
                       sinopsis, url_poster, fecha_creacion
                FROM vista_peliculas_completas
                ORDER BY fecha_creacion DESC
                """
                result = await session.execute(query)
                rows = result.fetchall()
                
                peliculas = []
                for row in rows:
                    pelicula = {
                        "pelicula_id": row[0],
                        "titulo": row[1],
                        "genero": row[2],
                        "clasificacion": row[3],
                        "director": row[4],
                        "sinopsis": row[5],
                        "url_poster": row[6],
                        "fecha_creacion": row[7]
                    }
                    peliculas.append(pelicula)
                
                return peliculas
                
        except Exception as e:
            logger.error(f"Error obteniendo películas completas: {e}")
            raise Exception(f"Error al consultar vista de películas: {str(e)}")
