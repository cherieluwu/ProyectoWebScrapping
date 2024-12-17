import asyncio
from playwright.async_api import async_playwright

async def main():
    # Iniciar Playwright y lanzar Chromium en modo headless
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()

        page = await context.new_page()

        # Interceptar requests y responses para ver las llamadas XHR
        page.on("request", lambda request: print(f">> {request.method} {request.url}"))
        page.on("response", lambda response: print(f"<< {response.status} {response.url}"))

        # Navegar a la página principal de Jumbo
        await page.goto("https://www.jumbo.cl/", wait_until="networkidle")

        # Esperar un elemento característico (ajustar según el sitio)
        # Por ejemplo, si buscas un elemento del home:
        await page.wait_for_selector("header")

        # Obtener cookies del contexto
        cookies = await context.cookies()
        print("Cookies:")
        for c in cookies:
            print(c)

        # Ejecutar JavaScript en la página para obtener tokens almacenados en localStorage
        # Ajustar según la lógica interna del sitio; este ejemplo asume que puede haber info relevante allí
        local_storage = await page.evaluate("() => { return JSON.stringify(localStorage); }")
        print("LocalStorage:", local_storage)

        # También se pueden obtener headers de las peticiones revisando el último request capturado:
        
        # Ejemplo básico de lectura de headers desde un request específico (suponiendo quieres la primera request XHR):
        # Se puede suscribir a eventos y guardar request en variables globales u obtenerlos en tiempo real.

        # Cerrar el navegador
        await browser.close()

asyncio.run(main())
