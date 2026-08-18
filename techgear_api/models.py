from pydantic import BaseModel, Field
from typing import List, Optional

# --- MODELOS DE PRODUCTO ---
class ProductoBase(BaseModel):
    nombre: str = Field(..., example="Base Maquillaje Angel Glow")
    descripcion: Optional[str] = Field(None, example="Base fluida acabado natural")
    precio: float = Field(..., gt=0, example=45000.0)
    stock: int = Field(..., ge=0, example=25)

class ProductoCreate(ProductoBase):
    pass

class ProductoResponse(ProductoBase):
    id: str = Field(..., alias="_id")

    class Config:
        populate_by_name = True


# --- MODELOS DE PEDIDO ---
class ItemPedido(BaseModel):
    producto_id: str = Field(..., example="65d0a2f1e4b0a123456789ab")
    cantidad: int = Field(..., gt=0, example=2)

class PedidoBase(BaseModel):
    cliente: str = Field(..., example="Melani Ferreira")
    items: List[ItemPedido]
    total: float = Field(..., gt=0, example=90000.0)

class PedidoCreate(PedidoBase):
    pass

class PedidoResponse(PedidoBase):
    id: str = Field(..., alias="_id")

    class Config:
        populate_by_name = True