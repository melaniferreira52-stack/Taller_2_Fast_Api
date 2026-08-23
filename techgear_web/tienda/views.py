from django.shortcuts import render
import requests

def catalogo_productos(request):
    url_api = "http://127.0.0.1:8000/productos/"
    productos = []
    
    try:
        response = requests.get(url_api, timeout=5)
        print(f"Status Code de FastAPI: {response.status_code}") # <-- Imprime el estado
        if response.status_code == 200:
            productos = response.json()
    except Exception as e:
        print(f"ERROR EXACTO AL CONECTAR CON FASTAPI: {e}") # <-- Muestra la causa real

    return render(request, 'tienda/catalogo.html', {'productos': productos})