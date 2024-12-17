import { MongoClient } from 'mongodb';
import { chromium } from 'playwright'; // Asegúrate de haber instalado: npm install playwright

const url = 'mongodb://127.0.0.1:27017';
const dbName = 'CIDB';

async function fetchDataAndSave() {
  const client = new MongoClient(url);

  try {
    await client.connect();
    console.log('Conectado a MongoDB');
    const db = client.db(dbName);
    const collection = db.collection('productos');

    // Lanzar el navegador con Playwright
    const browser = await chromium.launch({ headless: true });
    const page = await browser.newPage();

    // Interceptar solicitudes de red
    page.on('request', request => {
      console.log(`Request: ${request.method()} ${request.url()}`);
    });

    page.on('response', async response => {
      const url = response.url();
      if (url.includes('algún-patrón-que-indique-llamada-de-productos.json')) {
        // Si identificas que esta URL es la que devuelve datos de productos (JSON)
        try {
          const data = await response.json();
          // Asumiendo que data contiene un array de productos
          // Ajusta esto a la estructura real del JSON de Falabella
          const items = data.results.map(item => ({
            nombre: item.displayName,
            precio: item.prices ? item.prices.formattedSalePrice : 'N/A'
          }));

          // Guardar en la BD
          for (const it of items) {
            const result = await collection.insertOne(it);
            console.log(`Documento insertado con _id: ${result.insertedId}`);
          }
        } catch (err) {
          console.error('No se pudo parsear el JSON de productos', err);
        }
      }
    });

    // Navegar a la página
    await page.goto('https://www.falabella.com/falabella-cl/category/cat13720010/Camas?sid=HO_V4_CAM_1560', { waitUntil: 'networkidle' });

    // Esperar a que se cargue y renderice la página por completo
    // Aquí podrías esperar algún selector que indique que la página ya cargó productos
    await page.waitForTimeout(5000); // Ajustar según las necesidades

    // Opcional: puedes intentar extraer desde el DOM, si los datos no aparecen en la respuesta XHR
    // const html = await page.content();
    // Aquí podrías usar cheerio para parsear el HTML resultante si así lo deseas.

    // Ver los productos que acabamos de insertar
    const productos = await collection.find({}).toArray();
    console.log('Productos desde la BD:', productos);

    await browser.close();
  } catch (error) {
    console.error('Error:', error);
  } finally {
    await client.close();
  }
}

fetchDataAndSave().catch(console.error);
