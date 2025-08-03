import asyncpg
import psycopg2
from contextlib import asynccontextmanager
import os
import logging

logger = logging.getLogger(__name__)

class PostgresConnection:
    """Manejo de conexiones a PostgreSQL"""
    
    def __init__(self, db_number=1):
        # Soporte para múltiples bases PostgreSQL
        self.db_number = db_number
        if db_number == 1:
            self.host = os.getenv('POSTGRES_HOST')
            self.port = os.getenv('POSTGRES_PORT', 5432)
            self.database = os.getenv('POSTGRES_DB')
            self.username = os.getenv('POSTGRES_USERNAME')
            self.password = os.getenv('POSTGRES_PASSWORD')
        else:  # db_number == 2
            self.host = os.getenv('POSTGRES2_HOST')
            self.port = os.getenv('POSTGRES2_PORT', 5432)
            self.database = os.getenv('POSTGRES2_DB')
            self.username = os.getenv('POSTGRES2_USERNAME')
            self.password = os.getenv('POSTGRES2_PASSWORD')
            
        self.connection_string = (
            f"postgresql://{self.username}:{self.password}@"
            f"{self.host}:{self.port}/{self.database}"
        )
        self._connection = None
    
    def get_sync_connection(self):
        """Obtiene una conexión síncrona a PostgreSQL"""
        try:
            # Verificar que tenemos todas las credenciales
            if not all([self.host, self.database, self.username, self.password]):
                missing = []
                if not self.host: missing.append(f'POSTGRES{"2" if self.db_number == 2 else ""}_HOST')
                if not self.database: missing.append(f'POSTGRES{"2" if self.db_number == 2 else ""}_DB')
                if not self.username: missing.append(f'POSTGRES{"2" if self.db_number == 2 else ""}_USERNAME')
                if not self.password: missing.append(f'POSTGRES{"2" if self.db_number == 2 else ""}_PASSWORD')
                raise Exception(f"Variables de entorno faltantes: {', '.join(missing)}")
            
            if self._connection is None or self._connection.closed:
                self._connection = psycopg2.connect(
                    host=self.host,
                    port=self.port,
                    database=self.database,
                    user=self.username,
                    password=self.password
                )
                print(f"✅ CONEXIÓN A POSTGRESQL {self.db_number} ESTABLECIDA EXITOSAMENTE")
                logger.info(f"Conexión a PostgreSQL {self.db_number} establecida")
            return self._connection
        except psycopg2.Error as e:
            print(f"❌ ERROR CONECTANDO A POSTGRESQL {self.db_number}: {e}")
            logger.error(f"Error conectando a PostgreSQL {self.db_number}: {e}")
            raise Exception(f"Error de conexión a PostgreSQL {self.db_number}: {str(e)}")
    
    @asynccontextmanager
    async def get_session(self):
        """Context manager para manejo de sesiones PostgreSQL"""
        connection = None
        cursor = None
        try:
            connection = self.get_sync_connection()
            cursor = connection.cursor()
            
            # Wrapper para simular comportamiento async
            class PostgresSessionWrapper:
                def __init__(self, cursor, connection):
                    self.cursor = cursor
                    self.connection = connection
                
                async def execute(self, query, params=None):
                    if params:
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
            
            session = PostgresSessionWrapper(cursor, connection)
            yield session
            
        except Exception as e:
            if connection:
                connection.rollback()
            logger.error(f"Error en sesión PostgreSQL: {e}")
            raise
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
    
    def close(self):
        """Cierra la conexión"""
        try:
            if self._connection and not self._connection.closed:
                self._connection.close()
                logger.info(f"Conexión a PostgreSQL {self.db_number} cerrada correctamente")
            self._connection = None
        except Exception as e:
            logger.error(f"Error cerrando conexión PostgreSQL {self.db_number}: {e}")
            self._connection = None
    
    async def test_connection(self):
        """Prueba la conexión a PostgreSQL"""
        try:
            async with self.get_session() as session:
                await session.execute("SELECT 1")
                result = session.fetchone()
                return result is not None
        except Exception as e:
            logger.error(f"Test de conexión PostgreSQL falló: {e}")
            return False
