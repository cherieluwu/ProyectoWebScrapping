document.addEventListener('DOMContentLoaded', async () => {
    // Obtener el ID del producto de la URL
    const urlParams = new URLSearchParams(window.location.search);
    const productId = decodeURIComponent(urlParams.get('id'));
    
    if (!productId) {
        console.error('ID de producto no encontrado');
        return;
    }

    await loadProductInfo(productId);
});

async function loadProductInfo(productId) {
    try {
        // Obtener información del producto
        const response = await fetch('http://localhost:5000/api/productos');
        const productos = await response.json();
        const producto = productos.find(p => p.id === productId);
        
        if (!producto) {
            console.error('Producto no encontrado');
            return;
        }
        
        // Actualizar título e imagen
        const productTitle = document.getElementById('productTitle');
        productTitle.textContent = producto.nombre;
        
        const productImage = document.querySelector('.product-image');
        if (productImage) {
            productImage.src = producto.imagen;
            productImage.alt = producto.nombre;
        }
        
        // Obtener precios actuales y URLs
        const preciosResponse = await fetch(`http://localhost:5000/api/precios?id=${encodeURIComponent(productId)}&include_urls=true`);
        if (!preciosResponse.ok) {
            throw new Error('Error al obtener precios');
        }
        const data = await preciosResponse.json();
        
        // Guardar las URLs globalmente
        window.storeUrls = data.urls;
        
        // Actualizar precios en la página
        updatePriceRange(data.precios);
        updateStoreList(data.precios);
        
        // Obtener historial de precios
        const historialResponse = await fetch(`http://localhost:5000/api/historial-precios?id=${encodeURIComponent(productId)}`);
        if (historialResponse.ok) {
            const historial = await historialResponse.json();
            // Aquí puedes agregar código para mostrar el historial de precios
            // Por ejemplo, en un gráfico o una tabla
        }
        
    } catch (error) {
        console.error('Error al cargar la información del producto:', error);
    }
}

function goToStore(store) {
    if (window.storeUrls && window.storeUrls[store.toLowerCase()]) {
        window.open(window.storeUrls[store.toLowerCase()], '_blank');
    } else {
        console.error('URL de tienda no encontrada');
    }
}

function formatPrice(price) {
    return new Intl.NumberFormat('es-CL').format(Number(price));
}

function updatePriceRange(precios) {
    const preciosOrdenados = Object.entries(precios)
        .sort(([,a], [,b]) => parseFloat(a) - parseFloat(b));
    
    const precioMasBajo = preciosOrdenados[0][1];
    const precioMasAlto = preciosOrdenados[preciosOrdenados.length - 1][1];
    
    document.querySelector('.min-price').textContent = `$${formatPrice(precioMasBajo)}`;
    document.querySelector('.max-price').textContent = `$${formatPrice(precioMasAlto)}`;
}

function updateStoreList(precios) {
    const storeList = document.querySelector('.store-list');
    const storeNames = {
        'jumbo': 'Jumbo',
        'unimarc': 'Unimarc',
        'santaisabel': 'Santa Isabel'
    };
    
    storeList.innerHTML = '';
    
    Object.entries(precios).forEach(([store, price]) => {
        const storeItem = document.createElement('div');
        storeItem.className = 'store-item';
        
        storeItem.innerHTML = `
            <div class="store-name">${storeNames[store]}</div>
            <div class="store-price">$${formatPrice(price)}</div>
            <button class="btn btn-outline-primary btn-reviews" onclick="showReviews('${store}')">
                <i class="bi bi-chat-text"></i>
            </button>
            <button class="btn btn-primary btn-store" onclick="goToStore('${store}')">
                <i class="bi bi-box-arrow-up-right"></i>
            </button>
        `;
        
        storeList.appendChild(storeItem);
    });
}

// Funciones auxiliares para los botones
function showReviews(store) {
    console.log(`Mostrando reseñas de ${store}`);
    // Implementar lógica para mostrar reseñas
}

// Manejadores de eventos para los botones
document.getElementById('btnAddToList')?.addEventListener('click', () => {
    // Implementar lógica para añadir a lista de compra
    console.log('Añadiendo a lista de compra');
});

document.getElementById('btnSave')?.addEventListener('click', () => {
    // Implementar lógica para guardar
    console.log('Guardando producto');
}); 