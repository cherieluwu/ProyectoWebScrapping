// Importar módulos necesarios
import axios from 'axios';
import * as cheerio from 'cheerio';
import { MongoClient } from 'mongodb'; // Importar MongoClient para conectar a MongoDB
import { scrapeParis } from './parisScraper.mjs'; // Importar la función scrapeParis desde el scraper específico

async function main() {
    await scrapeParis(); // Ejecuta el scraper de Paris
    // Llama a otros scrapers aquí si los tienes
}

main().catch(console.error);