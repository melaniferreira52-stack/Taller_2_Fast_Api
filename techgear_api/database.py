import os
import asyncio
import certifi
from pymongo import AsyncMongoClient
from dotenv import load_dotenv

load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL")

client = AsyncMongoClient(
    MONGODB_URL,
    tls=True,
    tlsCAFile=certifi.where(),
    serverSelectionTimeoutMS=5000
)

database = client.techgear_db
producto_collection = database.get_collection("productos")
pedido_collection = database.get_collection("pedidos")

async def test_connection():
    try:
        await client.admin.command("ping")
        print("Conexión a MongoDB Atlas exitosa.")
    except Exception as e:
        print(f"Error al conectar a MongoDB: {e}")

if __name__ == "__main__":
    asyncio.run(test_connection())