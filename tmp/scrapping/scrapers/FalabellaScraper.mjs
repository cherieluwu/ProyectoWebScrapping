import axios from 'axios';
import * as cheerio from 'cheerio';
import { MongoClient } from 'mongodb';

const mongoUrl = 'mongodb://localhost:27017'; 

export async function scrapeFalabella() {
    const url = 'https://www.falabella.com/falabella-cl'; 

    try {
        const { data } = await axios.get(url);
        const $ = cheerio.load(data);
        
        const results = []; // Array para almacenar los resultados

        $('.product-item').each((index, element) => {
            const title = $(element).find('.product-title').text().trim();
            const id = $(element).find("productId").attr('src');
            const image = $(element).find('mediaUrls').text().trim();
            const price = $(element).find("prices").text().trim();
            const originalprice = $(element).find("originalPrice").text().trim();
            
            results.push({ title, id, image, price, originalprice }); // Agregar al array de resultados
        });

        await saveToDatabase(results); // Guardar en la base de datos

    } catch (error) {
        console.error('Error al realizar scraping:', error);
    }
}

async function saveToDatabase(results) {
    const client = new MongoClient(mongoUrl);
    try {
        await client.connect();
        const database = client.db('miBaseDeDatos'); // Cambia el nombre según sea necesario
        const collection = database.collection('productos');
        
        // Insertar múltiples documentos
        await collection.insertMany(results);
        console.log('Resultados guardados en la base de datos.');
    } finally {
        await client.close();
    }
}