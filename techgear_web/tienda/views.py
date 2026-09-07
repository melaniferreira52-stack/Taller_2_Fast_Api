import os
import requests
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages


def catalogo_productos(request):
    url_api = "http://127.0.0.1:8000/productos/"
    productos = []

    try:
        response = requests.get(url_api, timeout=5)
        print(f"Status Code de FastAPI: {response.status_code}")
        if response.status_code == 200:
            productos = response.json()
            for p in productos:
                p['id'] = p.get('_id')
    except Exception as e:
        print(f"ERROR EXACTO AL CONECTAR CON FASTAPI: {e}")

    return render(request, 'tienda/catalogo.html', {'productos': productos})


def panel_admin(request):
    mapa_productos = {}
    pedidos = []
    try:
        resp_prod = requests.get(f"{settings.API_BASE_URL}/productos/", timeout=5)
        if resp_prod.status_code == 200:
            for p in resp_prod.json():
                mapa_productos[p['_id']] = p['nombre']

        resp_ped = requests.get(f"{settings.API_BASE_URL}/pedidos/", timeout=5)
        if resp_ped.status_code == 200:
            for pedido in resp_ped.json():
                nombres = [mapa_productos.get(i['producto_id'], 'Producto eliminado') for i in pedido['items']]
                cantidades = [str(i['cantidad']) for i in pedido['items']]
                pedidos.append({
                    'id': pedido['_id'],
                    'cliente': pedido['cliente'],
                    'producto': ", ".join(nombres),
                    'cantidad': ", ".join(cantidades),
                    'total': pedido['total'],
                })
    except Exception as e:
        messages.error(request, f"No se pudo conectar con la API: {e}")

    return render(request, 'tienda/historial_pedidos.html', {'pedidos': pedidos})


def productos_admin(request):
    productos = []
    try:
        response = requests.get(f"{settings.API_BASE_URL}/productos/", timeout=5)
        if response.status_code == 200:
            productos = response.json()
            for p in productos:
                p['id'] = p.get('_id')
    except Exception as e:
        messages.error(request, f"No se pudo conectar con la API: {e}")

    return render(request, 'tienda/productos_admin.html', {'productos': productos})

def producto_crear(request):
    if request.method == 'POST':
        imagen_url = _guardar_imagen(request.FILES.get('imagen'))

        data = {
            "nombre": request.POST.get('nombre'),
            "descripcion": request.POST.get('descripcion'),
            "precio": float(request.POST.get('precio')),
            "stock": int(request.POST.get('stock')),
            "imagen": imagen_url,
        }
        try:
            response = requests.post(f"{settings.API_BASE_URL}/productos/", json=data, timeout=5)
            if response.status_code == 201:
                messages.success(request, "Producto creado correctamente.")
                return redirect('productos_admin')
            else:
                messages.error(request, f"La API respondió con error: {response.text}")
        except Exception as e:
            messages.error(request, f"No se pudo conectar con la API: {e}")

    return render(request, 'tienda/producto_form.html', {'accion': 'Crear'})


def producto_editar(request, producto_id):
    producto = None
    try:
        response = requests.get(f"{settings.API_BASE_URL}/productos/{producto_id}", timeout=5)
        if response.status_code == 200:
            producto = response.json()
    except Exception as e:
        messages.error(request, f"No se pudo conectar con la API: {e}")

    if request.method == 'POST':
        imagen_url = _guardar_imagen(request.FILES.get('imagen'))
        if not imagen_url:
            imagen_url = request.POST.get('imagen_actual')

        data = {
            "nombre": request.POST.get('nombre'),
            "descripcion": request.POST.get('descripcion'),
            "precio": float(request.POST.get('precio')),
            "stock": int(request.POST.get('stock')),
            "imagen": imagen_url,
        }
        try:
            response = requests.put(f"{settings.API_BASE_URL}/productos/{producto_id}", json=data, timeout=5)
            if response.status_code == 200:
                messages.success(request, "Producto actualizado correctamente.")
                return redirect('productos_admin')
            else:
                messages.error(request, f"La API respondió con error: {response.text}")
        except Exception as e:
            messages.error(request, f"No se pudo conectar con la API: {e}")

    return render(request, 'tienda/producto_form.html', {'accion': 'Editar', 'producto': producto})

def producto_eliminar(request, producto_id):
    try:
        response = requests.delete(f"{settings.API_BASE_URL}/productos/{producto_id}", timeout=5)
        if response.status_code == 204:
            messages.success(request, "Producto eliminado correctamente.")
        else:
            messages.error(request, f"La API respondió con error: {response.text}")
    except Exception as e:
        messages.error(request, f"No se pudo conectar con la API: {e}")

    return redirect('productos_admin')


def _guardar_imagen(archivo):
    if not archivo:
        return None
    carpeta = os.path.join(settings.MEDIA_ROOT, 'productos')
    os.makedirs(carpeta, exist_ok=True)
    ruta_destino = os.path.join(carpeta, archivo.name)
    with open(ruta_destino, 'wb+') as destino:
        for chunk in archivo.chunks():
            destino.write(chunk)
    return f"{settings.MEDIA_URL}productos/{archivo.name}"

def historial_pedidos(request):
    mapa_productos = {}
    pedidos = []
    try:
        resp_prod = requests.get(f"{settings.API_BASE_URL}/productos/", timeout=5)
        if resp_prod.status_code == 200:
            for p in resp_prod.json():
                mapa_productos[p['_id']] = p['nombre']

        resp_ped = requests.get(f"{settings.API_BASE_URL}/pedidos/", timeout=5)
        if resp_ped.status_code == 200:
            for pedido in resp_ped.json():
                nombres = [mapa_productos.get(i['producto_id'], 'Producto eliminado') for i in pedido['items']]
                cantidades = [str(i['cantidad']) for i in pedido['items']]
                pedidos.append({
                    'id': pedido['_id'],
                    'cliente': pedido['cliente'],
                    'producto': ", ".join(nombres),
                    'cantidad': ", ".join(cantidades),
                    'total': pedido['total'],
                })
    except Exception as e:
        messages.error(request, f"No se pudo conectar con la API: {e}")

    return render(request, 'tienda/historial_pedidos.html', {'pedidos': pedidos})


def detalle_pedido(request, pedido_id):
    mapa_productos = {}
    pedido = None
    try:
        resp_prod = requests.get(f"{settings.API_BASE_URL}/productos/", timeout=5)
        if resp_prod.status_code == 200:
            for p in resp_prod.json():
                mapa_productos[p['_id']] = p['nombre']

        resp_ped = requests.get(f"{settings.API_BASE_URL}/pedidos/", timeout=5)
        if resp_ped.status_code == 200:
            for p in resp_ped.json():
                if p['_id'] == pedido_id:
                    for item in p['items']:
                        item['nombre'] = mapa_productos.get(item['producto_id'], 'Producto eliminado')
                    p['id'] = p.pop('_id')
                    pedido = p
                    break
    except Exception as e:
        messages.error(request, f"No se pudo conectar con la API: {e}")

    return render(request, 'tienda/detalle_pedido.html', {'pedido': pedido})

def checkout(request, producto_id):
    producto = None
    try:
        response = requests.get(f"{settings.API_BASE_URL}/productos/{producto_id}", timeout=5)
        if response.status_code == 200:
            producto = response.json()
    except Exception as e:
        messages.error(request, f"No se pudo conectar con la API: {e}")

    if request.method == 'POST' and producto:
        cliente = request.POST.get('cliente')
        cantidad = int(request.POST.get('cantidad', 1))
        total = producto['precio'] * cantidad

        data = {
            "cliente": cliente,
            "items": [
                {"producto_id": producto_id, "cantidad": cantidad}
            ],
            "total": total,
        }
        try:
            resp = requests.post(f"{settings.API_BASE_URL}/pedidos/", json=data, timeout=5)
            if resp.status_code == 201:
                messages.success(request, "¡Pedido realizado con éxito!")
                return redirect('catalogo')
            else:
                messages.error(request, f"La API respondió con error: {resp.text}")
        except Exception as e:
            messages.error(request, f"No se pudo conectar con la API: {e}")

    return render(request, 'tienda/checkout.html', {'producto': producto, 'producto_id': producto_id})