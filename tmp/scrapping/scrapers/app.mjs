import { MongoClient } from 'mongodb';
import axios from 'axios';
import * as cheerio from 'cheerio'; 

const url = 'mongodb://127.0.0.1:27017'; // URL de conexión
const dbName = 'CIDB'; // Nombre de tu base de datos

async function fetchDataAndSave() {
    const client = new MongoClient(url);

    try {
        // Conectar al cliente
        await client.connect();
        console.log('Conectado a MongoDB');

        const db = client.db(dbName);
        const collection = db.collection('productos'); // Definir collection aquí

        // Realizar una solicitud GET
        const response = await axios.get('https://www.falabella.com/falabella-cl/category/cat13720010/Camas?sid=HO_V4_CAM_1560'); 
        console.log('Respuesta de la API:', response.data); // Imprimir la respuesta

        // Usar cheerio para parsear HTML si es necesario
        const $ = cheerio.load(response.data);
        
        const items = []; // Array para almacenar los datos a insertar
        
        $('selector-del-elemento').each((index, element) => {
            const nombre = $(element).find('displayName').text().trim();
            const precio = $(element).find('prices').text().trim();

            items.push({ nombre, precio }); // Agregar objeto al array
        });

        // Guardar cada elemento en la base de datos
        for (const item of items) {
            const result = await collection.insertOne(item);
            console.log(`Documento insertado con el _id: ${result.insertedId}`);
        }

        // Recuperar y mostrar todos los documentos
        const productos = await collection.find({}).toArray();
        console.log('Productos:', productos);
        
    } catch (error) {
        console.error('Error al conectar a MongoDB:', error);
    } finally {
        // Cerrar la conexión
        await client.close();
    }
}

fetchDataAndSave().catch(console.error);