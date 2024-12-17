document.addEventListener('DOMContentLoaded', async () => {
    await cargarProductos();
});

async function cargarProductos() {
    try {
        // Obtener productos de la API
        const response = await fetch('http://localhost:5000/api/productos');
        const productos = await response.json();
        
        const container = document.getElementById('productos-container');
        container.innerHTML = ''; // Limpiar contenedor
        
        productos.forEach(producto => {
            const precios = producto.precios_actuales || {};
            const precioMasBajo = Math.min(...Object.values(precios).filter(p => p > 0));
            
            const productoHTML = `
                <div class="col">
                    <div class="card h-100">
                        <img src="${producto.imagen}" class="card-img-top" alt="${producto.nombre}">
                        <div class="card-body">
                            <h5 class="card-title">${producto.nombre}</h5>
                            <p class="card-text">Desde $${precioMasBajo.toLocaleString()}</p>
                            <a href="vista_producto.html?id=${producto.id}" class="btn btn-primary">Ver detalles</a>
                        </div>
                    </div>
                </div>
            `;
            
            container.innerHTML += productoHTML;
        });
    } catch (error) {
        console.error('Error al cargar productos:', error);
    }
}

// Cargar productos al iniciar la página
document.addEventListener('DOMContentLoaded', cargarProductos);
