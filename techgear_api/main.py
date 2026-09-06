from fastapi import FastAPI, HTTPException, status
from bson import ObjectId
from database import producto_collection, pedido_collection
from models import ProductoCreate, ProductoResponse, PedidoCreate, PedidoResponse
from typing import List

app = FastAPI(
    title="API REST - Tienda Online",
    description="API desarrollada con FastAPI y MongoDB Atlas (Motor)",
    version="1.0.0"
)

# Función auxiliar para convertir la propiedad '_id' de Mongo a formato String
def fix_id(doc):
    if doc and "_id" in doc:
        doc["_id"] = str(doc["_id"])
    return doc


@app.get("/", tags=["Inicio"])
async def root():
    return {"mensaje": "Bienvenido a la API REST de la tienda"}


@app.post("/productos/", response_model=ProductoResponse, status_code=status.HTTP_201_CREATED, tags=["Productos"])
async def crear_producto(producto: ProductoCreate):
    nuevo_prod = producto.model_dump()
    result = await producto_collection.insert_one(nuevo_prod)
    creado = await producto_collection.find_one({"_id": result.inserted_id})
    return fix_id(creado)

@app.get("/productos/", response_model=List[ProductoResponse], tags=["Productos"])
async def listar_productos():
    productos = []
    cursor = producto_collection.find()
    async for doc in cursor:
        productos.append(fix_id(doc))
    return productos

@app.get("/productos/{id}", response_model=ProductoResponse, tags=["Productos"])
async def obtener_producto(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="El ID proporcionado no es válido")
    
    producto = await producto_collection.find_one({"_id": ObjectId(id)})
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return fix_id(producto)

@app.put("/productos/{id}", response_model=ProductoResponse, tags=["Productos"])
async def actualizar_producto(id: str, producto: ProductoCreate):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="El ID proporcionado no es válido")
    
    res = await producto_collection.update_one(
        {"_id": ObjectId(id)}, {"$set": producto.model_dump()}
    )
    if res.matched_count == 0:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    actualizado = await producto_collection.find_one({"_id": ObjectId(id)})
    return fix_id(actualizado)

@app.delete("/productos/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Productos"])
async def eliminar_producto(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="El ID proporcionado no es válido")
    
    res = await producto_collection.delete_one({"_id": ObjectId(id)})
    if res.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return None


@app.post("/pedidos/", response_model=PedidoResponse, status_code=status.HTTP_201_CREATED, tags=["Pedidos"])
async def registrar_pedido(pedido: PedidoCreate):
    nuevo_pedido = pedido.model_dump()
    result = await pedido_collection.insert_one(nuevo_pedido)
    creado = await pedido_collection.find_one({"_id": result.inserted_id})
    return fix_id(creado)

@app.get("/pedidos/", response_model=List[PedidoResponse], tags=["Pedidos"])
async def listar_pedidos():
    pedidos = []
    cursor = pedido_collection.find()
    async for doc in cursor:
        pedidos.append(fix_id(doc))
    return pedidos