from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from playwright.async_api import async_playwright

app = FastAPI()

# Permitir CORS para que el frontend en otro dominio pueda llamar la API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cambia "*" por dominios específicos en producción
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

@app.get("/scrape")
async def scrape(url: str = Query(..., description="URL a scrapear")):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url)
        title = await page.title()
        await browser.close()
    return {"title": title}
