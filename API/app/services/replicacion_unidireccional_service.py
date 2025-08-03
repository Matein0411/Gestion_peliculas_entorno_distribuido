from typing import List, Dict
from app.database.postgres_connection import PostgresConnection
import logging
import asyncio

logger = logging.getLogger(__name__)

class ReplicacionUnidireccionalService:
    """Servicio para evidenciar replicación unidireccional Guayaquil → Quito"""
    
    def __init__(self):
        # Conexión a Guayaquil (donde se insertan las películas)
        self.guayaquil_conn = PostgresConnection(db_number=2)
        # Conexión a Quito (donde se replican)
        self.quito_conn = PostgresConnection(db_number=1)
    
    async def consultar_peliculas_nodo(self, db_number: int) -> List[Dict]:
        """Consulta películas de un nodo específico"""
        conn = PostgresConnection(db_number=db_number)
        try:
            async with conn.get_session() as session:
                query = "SELECT * FROM peliculas_catalogo ORDER BY pelicula_id"
                result = await session.execute(query)
                return [
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
                    for row in result.fetchall()
                ]
        except Exception as e:
            logger.error(f"Error consultando películas DB{db_number}: {e}")
            return []
        finally:
            conn.close()
    
    async def insertar_peliculas_guayaquil(self, cantidad: int) -> List[Dict]:
        """Inserta películas en Guayaquil (nodo origen)"""
        peliculas_insertadas = []
        try:
            async with self.guayaquil_conn.get_session() as session:
                for i in range(cantidad):
                    titulo = f"Película Replicada {i+1}"
                    genero = ["Acción", "Drama", "Comedia", "Terror"][i % 4]
                    clasificacion = ["PG", "PG-13", "R"][i % 3]
                    director = f"Director {i+1}"
                    sinopsis = f"Sinopsis de la película {i+1} para probar replicación unidireccional"
                    url_poster = f"https://poster{i+1}.jpg"
                    
                    query = """
                    INSERT INTO peliculas_catalogo (titulo, genero, clasificacion, director, sinopsis, url_poster)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    RETURNING pelicula_id
                    """
                    
                    result = await session.execute(query, (titulo, genero, clasificacion, director, sinopsis, url_poster))
                    nuevo_id = result.fetchone()[0]
                    
                    peliculas_insertadas.append({
                        "pelicula_id": nuevo_id,
                        "titulo": titulo,
                        "genero": genero,
                        "clasificacion": clasificacion,
                        "director": director
                    })
                
                await session.commit()
                logger.info(f"✅ Insertadas {cantidad} películas en Guayaquil")
                
        except Exception as e:
            logger.error(f"❌ Error insertando películas en Guayaquil: {e}")
            raise
        
        return peliculas_insertadas
    
    async def evidenciar_replicacion_unidireccional(self, cantidad_peliculas: int) -> Dict:
        """Evidencia completa de replicación unidireccional Guayaquil → Quito"""
        try:
            logger.info(f"🎬 Iniciando replicación unidireccional: Guayaquil → Quito")
            
            # 1. Estado ANTES
            logger.info("📊 Consultando estado ANTES...")
            quito_antes = await self.consultar_peliculas_nodo(1)
            guayaquil_antes = await self.consultar_peliculas_nodo(2)
            
            # 2. INSERCIÓN en Guayaquil
            logger.info(f"📝 Insertando {cantidad_peliculas} películas en Guayaquil...")
            peliculas_nuevas = await self.insertar_peliculas_guayaquil(cantidad_peliculas)
            
            # 3. ESPERAR replicación
            logger.info("⏳ Esperando 5 segundos para replicación...")
            await asyncio.sleep(5)
            
            # 4. Estado DESPUÉS
            logger.info("📊 Consultando estado DESPUÉS...")
            quito_despues = await self.consultar_peliculas_nodo(1)
            guayaquil_despues = await self.consultar_peliculas_nodo(2)
            
            # 5. ANÁLISIS
            incremento_guayaquil = len(guayaquil_despues) - len(guayaquil_antes)
            incremento_quito = len(quito_despues) - len(quito_antes)
            
            replicacion_exitosa = (incremento_guayaquil == cantidad_peliculas and 
                                 incremento_quito == cantidad_peliculas)
            
            return {
                "replicacion_unidireccional": {
                    "direccion": "Guayaquil → Quito",
                    "peliculas_insertadas": cantidad_peliculas,
                    "estado_antes": {
                        "guayaquil_total": len(guayaquil_antes),
                        "quito_total": len(quito_antes)
                    },
                    "estado_despues": {
                        "guayaquil_total": len(guayaquil_despues),
                        "quito_total": len(quito_despues)
                    },
                    "incrementos": {
                        "guayaquil": incremento_guayaquil,
                        "quito": incremento_quito
                    },
                    "peliculas_nuevas": peliculas_nuevas,
                    "replicacion_exitosa": replicacion_exitosa,
                    "diagnostico": "✅ Replicación funcionando" if replicacion_exitosa else f"❌ FALLA: Guayaquil +{incremento_guayaquil}, Quito +{incremento_quito}, esperado +{cantidad_peliculas} en ambos"
                }
            }
            
        except Exception as e:
            logger.error(f"❌ Error en replicación unidireccional: {e}")
            return {"error": str(e)}
