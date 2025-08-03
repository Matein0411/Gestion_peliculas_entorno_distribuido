from typing import List, Dict
from app.database.postgres_connection import PostgresConnection
import logging

logger = logging.getLogger(__name__)

class PromocionesService:
    """Servicio para evidenciar replicación bidireccional de promociones"""
    
    def __init__(self, nodo_insercion: str):
        # Conectar al nodo donde se va a insertar
        if nodo_insercion == "Quito":
            self.postgres_conn = PostgresConnection(db_number=1)  # Nodo Quito
        else:  # Guayaquil
            self.postgres_conn = PostgresConnection(db_number=2)  # Nodo Guayaquil
        self.nodo_insercion = nodo_insercion
    
    async def consultar_estado_tablas(self, momento: str) -> Dict:
        """Consulta el estado de las tablas promociones en ambos nodos"""
        try:
            # Consultar desde el nodo actual (donde se inserta)
            async with self.postgres_conn.get_session() as session:
                query = "SELECT * FROM promociones ORDER BY promocion_id"
                result = await session.execute(query)
                promociones_nodo_actual = [
                    {
                        "promocion_id": row[0],
                        "codigo_promo": row[1],
                        "descripcion": row[2],
                        "descuento_porcentaje": float(row[3]) if row[3] else None,
                        "fecha_creacion": row[4],
                        "ciudad": row[5]
                    }
                    for row in result.fetchall()
                ]
            
            # Consultar desde el otro nodo (para evidenciar replicación)
            otro_nodo = "Guayaquil" if self.nodo_insercion == "Quito" else "Quito"
            otro_nodo_num = 2 if self.nodo_insercion == "Quito" else 1
            other_conn = PostgresConnection(db_number=otro_nodo_num)
            
            try:
                async with other_conn.get_session() as session:
                    query = "SELECT * FROM promociones ORDER BY promocion_id"
                    result = await session.execute(query)
                    promociones_otro_nodo = [
                        {
                            "promocion_id": row[0],
                            "codigo_promo": row[1],
                            "descripcion": row[2],
                            "descuento_porcentaje": float(row[3]) if row[3] else None,
                            "fecha_creacion": row[4],
                            "ciudad": row[5]
                        }
                        for row in result.fetchall()
                    ]
            finally:
                other_conn.close()  # Asegurar que se cierre la conexión
            
            return {
                "momento": momento,
                "nodo_insercion": self.nodo_insercion,
                f"promociones_{self.nodo_insercion.lower()}": promociones_nodo_actual,
                f"promociones_{otro_nodo.lower()}": promociones_otro_nodo,
                "total_registros_nodo_insercion": len(promociones_nodo_actual),
                "total_registros_otro_nodo": len(promociones_otro_nodo),
                "replicacion_sincronizada": len(promociones_nodo_actual) == len(promociones_otro_nodo),
                "debug_info": {
                    "nodo_insercion_db": f"DB{1 if self.nodo_insercion == 'Quito' else 2}",
                    "otro_nodo_db": f"DB{otro_nodo_num}",
                    "conexion_nodo_insercion": f"{self.postgres_conn.host}:{self.postgres_conn.port}",
                    "conexion_otro_nodo": f"{other_conn.host}:{other_conn.port}"
                }
            }
                
        except Exception as e:
            print(f"Error al consultar estado de tablas: {e}")
            logger.error(f"Error al consultar estado de tablas: {e}")
            return {
                "error": str(e),
                "detalle": "Error al consultar el estado de las tablas de promociones"
            }
    
    def _validar_replicacion(self, estado_antes: dict, estado_despues: dict, cantidad_insertada: int) -> bool:
        """Valida que la replicación haya funcionado correctamente"""
        try:
            incremento_quito = estado_despues.get("quito", {}).get("total_promociones", 0) - estado_antes.get("quito", {}).get("total_promociones", 0)
            incremento_guayaquil = estado_despues.get("guayaquil", {}).get("total_promociones", 0) - estado_antes.get("guayaquil", {}).get("total_promociones", 0)
            
            # Ambos nodos deben tener el mismo incremento
            return incremento_quito == cantidad_insertada and incremento_guayaquil == cantidad_insertada
        except:
            return False
    
    async def insertar_promociones_automaticas(self, cantidad: int) -> List[Dict]:
        """Inserta promociones automáticas en el nodo especificado"""
        try:
            registros_insertados = []
            async with self.postgres_conn.get_session() as session:
                for i in range(cantidad):
                    codigo_promo = f"REP{self.nodo_insercion.upper()}{i+1:03d}"
                    descripcion = f"Promoción replicada {i+1} desde {self.nodo_insercion}"
                    descuento = 15.0 + (i * 1.5)
                    ciudad = self.nodo_insercion
                    
                    query_insert = """
                    INSERT INTO promociones (codigo_promo, descripcion, descuento_porcentaje, ciudad)
                    VALUES (%s, %s, %s, %s)
                    RETURNING promocion_id
                    """
                    result = await session.execute(query_insert, (codigo_promo, descripcion, descuento, ciudad))
                    nuevo_id = result.fetchone()[0]
                    
                    registros_insertados.append({
                        "promocion_id": nuevo_id,
                        "codigo_promo": codigo_promo,
                        "descripcion": descripcion,
                        "descuento_porcentaje": descuento,
                        "ciudad": ciudad
                    })
                
                # COMMIT EXPLÍCITO para asegurar que los cambios se persistan
                await session.commit()
                logger.info(f"✅ Insertados {cantidad} registros en {self.nodo_insercion} con commit exitoso")
            
            return registros_insertados
                
        except Exception as e:
            logger.error(f"Error insertando promociones en {self.nodo_insercion}: {e}")
            raise Exception(f"Error al insertar promociones: {str(e)}")
    
    async def evidenciar_replicacion_bidireccional(self, cantidad_registros: int) -> Dict:
        """Evidencia completa de replicación bidireccional con tiempo de espera mejorado"""
        try:
            logger.info(f"🔄 Iniciando evidencia de replicación bidireccional - Nodo: {self.nodo_insercion}")
            
            # 1. Estado ANTES
            logger.info("📊 Consultando estado ANTES de la inserción...")
            estado_antes = await self.consultar_estado_tablas("ANTES de la inserción")
            
            # 2. INSERCIÓN
            logger.info(f"📝 Insertando {cantidad_registros} registros en {self.nodo_insercion}...")
            registros_insertados = await self.insertar_promociones_automaticas(cantidad_registros)
            
            # 3. Espera más larga para la replicación
            import asyncio
            logger.info("⏳ Esperando 3 segundos para que se complete la replicación...")
            await asyncio.sleep(3)  # Aumentamos a 3 segundos
            
            # 4. Estado DESPUÉS
            logger.info("📊 Consultando estado DESPUÉS de la inserción...")
            estado_despues = await self.consultar_estado_tablas("DESPUÉS de la inserción")
            
            # 5. Análisis de replicación
            incremento_nodo_insercion = estado_despues["total_registros_nodo_insercion"] - estado_antes["total_registros_nodo_insercion"]
            incremento_otro_nodo = estado_despues["total_registros_otro_nodo"] - estado_antes["total_registros_otro_nodo"]
            
            replicacion_exitosa = (incremento_nodo_insercion == cantidad_registros and 
                                 incremento_otro_nodo == cantidad_registros)
            
            logger.info(f"✅ Evidencia completada - Replicación: {'EXITOSA' if replicacion_exitosa else 'FALLIDA'}")
            
            return {
                "evidencia_replicacion_bidireccional": {
                    "nodo_insercion": self.nodo_insercion,
                    "cantidad_registros_insertados": cantidad_registros,
                    "1_estado_antes": estado_antes,
                    "2_registros_insertados": registros_insertados,
                    "3_estado_despues": estado_despues,
                    "4_verificacion_replicacion": {
                        "registros_antes_nodo_insercion": estado_antes["total_registros_nodo_insercion"],
                        "registros_despues_nodo_insercion": estado_despues["total_registros_nodo_insercion"],
                        "registros_antes_otro_nodo": estado_antes["total_registros_otro_nodo"],
                        "registros_despues_otro_nodo": estado_despues["total_registros_otro_nodo"],
                        "incremento_nodo_insercion": incremento_nodo_insercion,
                        "incremento_otro_nodo": incremento_otro_nodo,
                        "replicacion_funciona": replicacion_exitosa,
                        "ambos_nodos_sincronizados": estado_despues["replicacion_sincronizada"],
                        "diagnostico": {
                            "esperado_incremento": cantidad_registros,
                            "obtenido_nodo_insercion": incremento_nodo_insercion,
                            "obtenido_otro_nodo": incremento_otro_nodo,
                            "problema_detectado": self._diagnosticar_problema_replicacion(
                                cantidad_registros, incremento_nodo_insercion, incremento_otro_nodo
                            )
                        }
                    }
                }
            }
            
        except Exception as e:
            logger.error(f"❌ Error en evidencia bidireccional: {e}")
            raise Exception(f"Error en proceso de evidencia: {str(e)}")
    
    def _diagnosticar_problema_replicacion(self, esperado: int, nodo_insercion: int, otro_nodo: int) -> str:
        """Diagnostica problemas específicos de replicación"""
        if nodo_insercion != esperado and otro_nodo != esperado:
            return "❌ Falló inserción en nodo origen Y replicación"
        elif nodo_insercion == esperado and otro_nodo != esperado:
            return f"❌ Inserción exitosa en {self.nodo_insercion} pero falló replicación al otro nodo"
        elif nodo_insercion != esperado and otro_nodo == esperado:
            return "⚠️ Situación extraña: falló inserción pero aparece en otro nodo"
        else:
            return "✅ Replicación bidireccional funcionando correctamente"
