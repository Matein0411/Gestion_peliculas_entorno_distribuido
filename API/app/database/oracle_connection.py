import oracledb
from contextlib import asynccontextmanager
import os
import logging

logger = logging.getLogger(__name__)

class OracleConnection:
    """Manejo de conexiones a Oracle Database"""
    
    def __init__(self):
        self.connection_params = {
            "user": os.getenv('ORACLE_USERNAME'),
            "password": os.getenv('ORACLE_PASSWORD'),
            "host": os.getenv('ORACLE_HOST'),
            "port": int(os.getenv('ORACLE_PORT', 1521)),
            "service_name": os.getenv('ORACLE_SERVICE_NAME')
        }
        self._connection = None
    
    def get_connection(self):
        """Obtiene una conexión a Oracle"""
        try:
            if self._connection is None or not self._connection:
                self._connection = oracledb.connect(**self.connection_params)
                print("✅ CONEXIÓN A ORACLE ESTABLECIDA EXITOSAMENTE")
                logger.info("Conexión a Oracle establecida exitosamente")
            return self._connection
        except oracledb.Error as e:
            print(f"❌ ERROR CONECTANDO A ORACLE: {e}")
            logger.error(f"Error conectando a Oracle: {e}")
            raise Exception(f"Error de conexión a Oracle: {str(e)}")
    
    @asynccontextmanager
    async def get_session(self):
        """Context manager para manejo de sesiones Oracle"""
        connection = None
        cursor = None
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            
            # Wrapper para simular comportamiento async
            class OracleSessionWrapper:
                def __init__(self, cursor, connection):
                    self.cursor = cursor
                    self.connection = connection
                
                async def execute(self, query, params=None):
                    if params:
                        if isinstance(params, dict):
                            # Para parámetros nombrados
                            self.cursor.execute(query, params)
                        else:
                            # Para parámetros posicionales
                            self.cursor.execute(query, params)
                    else:
                        self.cursor.execute(query)
                    return self.cursor
                
                async def commit(self):
                    self.connection.commit()
                
                async def rollback(self):
                    self.connection.rollback()
                
                def fetchall(self):
                    return self.cursor.fetchall()
                
                def fetchone(self):
                    return self.cursor.fetchone()
                
                def fetchmany(self, size):
                    return self.cursor.fetchmany(size)
            
            session = OracleSessionWrapper(cursor, connection)
            yield session
            
        except Exception as e:
            if connection:
                connection.rollback()
            logger.error(f"Error en sesión Oracle: {e}")
            raise
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
    
    def close(self):
        """Cierra la conexión"""
        if self._connection:
            self._connection.close()
            self._connection = None
            logger.info("Conexión a Oracle cerrada")
    
    async def test_connection(self):
        """Prueba la conexión a Oracle"""
        try:
            async with self.get_session() as session:
                await session.execute("SELECT 1 FROM DUAL")
                result = session.fetchone()
                return result is not None
        except Exception as e:
            logger.error(f"Test de conexión Oracle falló: {e}")
            return False
