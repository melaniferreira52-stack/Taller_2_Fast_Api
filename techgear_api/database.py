import os
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

# Cargar variables de entorno del archivo .env
load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL")

# Inicializar el cliente de MongoDB
client = AsyncIOMotorClient(MONGODB_URL)

# Seleccionar la base de datos y colecciones para la tienda
database = client.tienda_db
producto_collection = database.get_collection("productos")
pedido_collection = database.get_collection("pedidos")

# Función para probar la conexión a MongoDB Atlas
async def test_connection():
    try:
        await client.admin.command("ping")
        print(" Conexión a MongoDB Atlas exitosa.")
    except Exception as e:
        print(f" Error al conectar a MongoDB: {e}")

if __name__ == "__main__":
    asyncio.run(test_connection())