from typing import List, Dict
from app.database.postgres_connection import PostgresConnection
from app.database.oracle_connection import OracleConnection
import logging
import os

logger = logging.getLogger(__name__)

class ReplicacionQuitoCuencaService:
    """Servicio para evidenciar replicación unidireccional Quito → Cuenca"""
    
    def __init__(self):
        # Conexión a Quito (PostgreSQL - donde se insertan las películas)
        self.quito_conn = PostgresConnection(db_number=1)
        # Conexión a Cuenca (Oracle - donde se replican via trigger)
        self.cuenca_conn = OracleConnection()
    
    async def consultar_peliculas_quito(self) -> List[Dict]:
        """Consulta películas en Quito (PostgreSQL)"""
        logger.info("   → Consultando Quito (PostgreSQL)...")
        try:
            async with self.quito_conn.get_session() as session:
                logger.info("   → Ejecutando query SELECT...")
                query = "SELECT * FROM peliculas_catalogo ORDER BY pelicula_id"
                result = await session.execute(query)
                logger.info("   → Procesando resultados...")
                rows = result.fetchall()
                peliculas = [
                    {
                        "pelicula_id": row[0],
                        "titulo": row[1],
                        "genero": row[2],
                        "clasificacion": row[3],
                        "director": row[4],
                        "sinopsis": row[5],
                        "url_poster": row[6],
                        "fecha_creacion": str(row[7])
                    }
                    for row in rows
                ]
                logger.info(f"   → Consulta Quito exitosa: {len(peliculas)} películas")
                return peliculas
        except Exception as e:
            logger.error(f"   ✗ Error consultando películas en Quito: {e}")
            logger.error(f"   ✗ Tipo de error: {type(e).__name__}")
            return []
    
    async def consultar_peliculas_cuenca(self) -> List[Dict]:
        """Consulta películas en Cuenca (Oracle)"""
        logger.info("   → Consultando Cuenca (Oracle)...")
        try:
                connection = self.cuenca_conn.get_connection().__enter__()
                logger.info("   → Creando cursor...")
                cursor = connection.cursor()
                logger.info("   → Ejecutando query SELECT...")
                query = "SELECT * FROM peliculas_catalogo ORDER BY pelicula_id"
                cursor.execute(query)
                logger.info("   → Obteniendo resultados...")
                result = cursor.fetchall()
                logger.info("   → Procesando resultados...")
                
                peliculas = []
                for i, row in enumerate(result):
                    try:
                        # Convertir cada campo de forma segura
                        logger.info(f"   → Procesando fila {i+1}: tipos = {[type(cell).__name__ for cell in row]}")
                        
                        pelicula = {
                            "pelicula_id": int(row[0]) if row[0] is not None else None,
                            "titulo": str(row[1]) if row[1] is not None else "",
                            "genero": str(row[2]) if row[2] is not None else "",
                            "clasificacion": str(row[3]) if row[3] is not None else "",
                            "director": str(row[4]) if row[4] is not None else "",
                            "sinopsis": str(row[5]) if row[5] is not None else "",
                            "url_poster": str(row[6]) if row[6] is not None else "",
                            "fecha_creacion": str(row[7]) if row[7] is not None else ""
                        }
                        peliculas.append(pelicula)
                    except Exception as row_error:
                        logger.error(f"   ✗ Error procesando fila {i+1}: {row_error}")
                        logger.error(f"   ✗ Tipos de datos: {[type(cell).__name__ for cell in row]}")
                        logger.error(f"   ✗ Valores: {[str(cell)[:50] if cell is not None else 'NULL' for cell in row]}")
                        continue
                
                logger.info(f"   → Consulta Cuenca exitosa: {len(peliculas)} películas")
                return peliculas
        except Exception as e:
            logger.error(f"   ✗ Error consultando películas en Cuenca: {e}")
            logger.error(f"   ✗ Tipo de error: {type(e).__name__}")
            import traceback
            logger.error(f"   ✗ Traceback: {traceback.format_exc()}")
            return []
    
    async def insertar_peliculas_quito(self, cantidad: int) -> List[Dict]:
        """Inserta películas en Quito (se replicarán automáticamente a Cuenca via trigger)"""
        peliculas_insertadas = []
        try:
            async with self.quito_conn.get_session() as session:
                for i in range(cantidad):
                    titulo = f"Película Quito-Cuenca {i+1}"
                    genero = ["Acción", "Drama", "Comedia", "Terror", "Sci-Fi"][i % 5]
                    clasificacion = ["G", "PG", "PG-13", "R"][i % 4]
                    director = f"Director {i+1}"
                    sinopsis = f"Esta es una película de prueba para replicación Quito → Cuenca número {i+1}"
                    url_poster = f"https://ejemplo.com/poster_{i+1}.jpg"
                    
                    query = """
                    INSERT INTO peliculas_catalogo 
                    (titulo, genero, clasificacion, director, sinopsis, url_poster)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    RETURNING pelicula_id, fecha_creacion
                    """
                    
                    result = await session.execute(query, (
                        titulo, genero, clasificacion, director, sinopsis, url_poster
                    ))
                    row = result.fetchone()
                    
                    pelicula_data = {
                        "pelicula_id": row[0],
                        "titulo": titulo,
                        "genero": genero,
                        "clasificacion": clasificacion,
                        "director": director,
                        "sinopsis": sinopsis,
                        "url_poster": url_poster,
                        "fecha_creacion": str(row[1])
                    }
                    peliculas_insertadas.append(pelicula_data)
                    
                await session.commit()
                logger.info(f"Insertadas {cantidad} películas en Quito para replicación a Cuenca")
                
        except Exception as e:
            logger.error(f"Error insertando películas en Quito: {e}")
            await session.rollback()
            raise
        
        return peliculas_insertadas
    
    async def evidenciar_replicacion_quito_cuenca(self, cantidad_peliculas: int = 3) -> Dict:
        """
        Evidencia la replicación unidireccional Quito → Cuenca
        1. Consulta estado inicial en ambos nodos
        2. Inserta películas en Quito
        3. Consulta estado final para verificar replicación
        """
        try:
            logger.info("=== INICIANDO EVIDENCIA REPLICACIÓN QUITO-CUENCA ===")
            
            # Estado inicial
            logger.info("1. Consultando estado inicial en Quito...")
            peliculas_quito_inicial = await self.consultar_peliculas_quito()
            logger.info(f"   ✓ Quito inicial: {len(peliculas_quito_inicial)} películas")
            
            logger.info("2. Consultando estado inicial en Cuenca...")
            peliculas_cuenca_inicial = await self.consultar_peliculas_cuenca()
            logger.info(f"   ✓ Cuenca inicial: {len(peliculas_cuenca_inicial)} películas")
            
            # Insertar en Quito (origen)
            logger.info(f"3. Insertando {cantidad_peliculas} películas en Quito...")
            peliculas_insertadas = await self.insertar_peliculas_quito(cantidad_peliculas)
            logger.info(f"   ✓ Insertadas {len(peliculas_insertadas)} películas en Quito")
            
            # Esperar un momento para la replicación
            logger.info("4. Esperando 2 segundos para replicación...")
            import asyncio
            await asyncio.sleep(2)
            
            # Estado final
            logger.info("5. Consultando estado final en Quito...")
            peliculas_quito_final = await self.consultar_peliculas_quito()
            logger.info(f"   ✓ Quito final: {len(peliculas_quito_final)} películas")
            
            logger.info("6. Consultando estado final en Cuenca...")
            peliculas_cuenca_final = await self.consultar_peliculas_cuenca()
            logger.info(f"   ✓ Cuenca final: {len(peliculas_cuenca_final)} películas")
            
            logger.info("=== EVIDENCIA COMPLETADA EXITOSAMENTE ===")
            
            return {
                "tipo_replicacion": "Unidireccional Quito → Cuenca",
                "descripcion": "Películas insertadas en Quito (PostgreSQL) se replican automáticamente a Cuenca (Oracle) via trigger",
                "estado_inicial": {
                    "quito_count": len(peliculas_quito_inicial),
                    "cuenca_count": len(peliculas_cuenca_inicial),
                    "quito_peliculas": peliculas_quito_inicial,
                    "cuenca_peliculas": peliculas_cuenca_inicial
                },
                "operacion": {
                    "peliculas_insertadas_quito": cantidad_peliculas,
                    "detalles": peliculas_insertadas
                },
                "estado_final": {
                    "quito_count": len(peliculas_quito_final),
                    "cuenca_count": len(peliculas_cuenca_final),
                    "quito_peliculas": peliculas_quito_final,
                    "cuenca_peliculas": peliculas_cuenca_final
                },
                "evidencia_replicacion": {
                    "incremento_quito": len(peliculas_quito_final) - len(peliculas_quito_inicial),
                    "incremento_cuenca": len(peliculas_cuenca_final) - len(peliculas_cuenca_inicial),
                    "replicacion_exitosa": (len(peliculas_quito_final) - len(peliculas_quito_inicial)) == (len(peliculas_cuenca_final) - len(peliculas_cuenca_inicial))
                }
            }
            
        except Exception as e:
            logger.error(f"=== ERROR EN EVIDENCIA REPLICACIÓN ===")
            logger.error(f"Tipo de error: {type(e).__name__}")
            logger.error(f"Mensaje: {str(e)}")
            import traceback
            logger.error(f"Traceback completo: {traceback.format_exc()}")
            raise Exception(f"Error evidenciando replicación: {str(e)}")
