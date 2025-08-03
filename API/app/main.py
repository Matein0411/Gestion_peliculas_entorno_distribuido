from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from app.routes.clientes_unificados import router as clientes_unificados_router
from app.routes.peliculas_completas import router as peliculas_completas_router
from app.routes.evidencia_replicacion import router as evidencia_replicacion_router

# Cargar variables de entorno
load_dotenv()

# Crear la aplicación FastAPI
app = FastAPI(
    title="API Proyecto IIB",
    description="API para conectar bases de datos de Cuenca (Oracle), Quito (PostgreSQL) y Guayaquil (PostgreSQL)",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominios específicos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(
    clientes_unificados_router,
    prefix="/api/v1",
    tags=["Clientes Unificados"]
)

app.include_router(
    peliculas_completas_router,
    prefix="/api/v1",
    tags=["Películas Completas"]
)

app.include_router(
    evidencia_replicacion_router,
    prefix="/api/v1",
    tags=["Evidencia de Replicación"]
)

@app.get("/")
async def root():
    """Endpoint raíz de la API"""
    return {
        "message": "API Multi-Database Ecuador",
        "version": "1.0.0",
        "databases": {
            "Cuenca": "Oracle",
            "Quito": "PostgreSQL",
            "Guayaquil": "PostgreSQL"
        },
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    """Endpoint para verificar el estado de la API"""
    return {"status": "healthy", "message": "API funcionando correctamente"}

@app.get("/test-oracle")
async def test_oracle_connection():
    """Prueba la conexión a la base de datos de Cuenca (Oracle)"""
    try:
        from app.database.oracle_connection import OracleConnection
        oracle_conn = OracleConnection()
        
        # Solo intentar conectar
        connection = oracle_conn.get_connection()
        connection.close()
        
        return {
            "status": "success", 
            "message": "Conexión a Cuenca exitosa",
            "database": "Cuenca (Oracle)"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error conectando a Cuenca: {str(e)}",
            "database": "Cuenca (Oracle)"
        }

@app.get("/test-postgres1")
async def test_postgres1_connection():
    """Prueba la conexión a la base de datos de Quito (PostgreSQL)"""
    try:
        from app.database.postgres_connection import PostgresConnection
        postgres_conn = PostgresConnection(db_number=1)
        
        # Solo intentar conectar
        connection = postgres_conn.get_sync_connection()
        connection.close()
        
        return {
            "status": "success", 
            "message": "Conexión a Quito exitosa",
            "database": "Quito (PostgreSQL)"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error conectando a Quito: {str(e)}",
            "database": "Quito (PostgreSQL)"
        }

@app.get("/test-postgres2")
async def test_postgres2_connection():
    """Prueba la conexión a la base de datos de Guayaquil (PostgreSQL)"""
    try:
        from app.database.postgres_connection import PostgresConnection
        postgres_conn = PostgresConnection(db_number=2)
        
        # Solo intentar conectar
        connection = postgres_conn.get_sync_connection()
        connection.close()
        
        return {
            "status": "success", 
            "message": "Conexión a Guayaquil exitosa",
            "database": "Guayaquil (PostgreSQL)"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error conectando a Guayaquil: {str(e)}",
            "database": "Guayaquil (PostgreSQL)"
        }
