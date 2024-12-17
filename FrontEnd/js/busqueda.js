// Función para navegar a diferentes páginas
function navigateTo(page) {
    window.location.href = page + '.html';
}

// Event listeners para los botones de la barra lateral
document.getElementById('btnHome').addEventListener('click', () => navigateTo('home'));
document.getElementById('btnCategorias').addEventListener('click', () => navigateTo('categorias'));
document.getElementById('btnGuardados').addEventListener('click', () => navigateTo('guardados'));
document.getElementById('btnListaCompras').addEventListener('click', () => navigateTo('listaDeCompras'));

// Event listeners para los botones del menú desplegable
document.getElementById('menuHome').addEventListener('click', () => navigateTo('home'));
document.getElementById('menuCategorias').addEventListener('click', () => navigateTo('categorias'));
document.getElementById('menuGuardados').addEventListener('click', () => navigateTo('guardados'));
document.getElementById('menuListaCompras').addEventListener('click', () => navigateTo('listaDeCompras'));

// Event listeners para botones de reportar y cerrar sesión
document.getElementById('btnReportar').addEventListener('click', () => {
    // Aquí iría la lógica para reportar un problema
    console.log('Reportar problema');
});

document.getElementById('menuReportar').addEventListener('click', () => {
    // Aquí iría la lógica para reportar un problema
    console.log('Reportar problema');
});

document.getElementById('btnCerrarSesion').addEventListener('click', () => {
    // Aquí iría la lógica para cerrar sesión
    console.log('Cerrar sesión');
});

document.getElementById('menuCerrarSesion').addEventListener('click', () => {
    // Aquí iría la lógica para cerrar sesión
    console.log('Cerrar sesión');
});

document.addEventListener('DOMContentLoaded', function() {
    const searchForm = document.getElementById('search-form');
    const searchInput = document.getElementById('search-input');
    const resultsContainer = document.getElementById('results-container');
    
    // Cargar productos recientes al inicio
    cargarProductosRecientes();
    
    searchForm.addEventListener('submit', function(e) {
        e.preventDefault();
        realizarBusqueda(searchInput.value);
    });
    
    async function realizarBusqueda(query) {
        try {
            const response = await fetch(`http://localhost:5000/api/buscar?q=${encodeURIComponent(query)}`);
            const data = await response.json();
            
            if (data.success) {
                mostrarResultados(data.productos);
            } else {
                mostrarError('Error en la búsqueda');
            }
        } catch (error) {
            console.error('Error:', error);
            mostrarError('Error de conexión');
        }
    }
    
    async function cargarProductosRecientes() {
        try {
            const response = await fetch('http://localhost:5000/api/productos/recientes');
            const data = await response.json();
            
            if (data.success) {
                mostrarResultados(data.productos);
            }
        } catch (error) {
            console.error('Error:', error);
        }
    }
    
    function mostrarResultados(productos) {
        resultsContainer.innerHTML = '';
        
        if (productos.length === 0) {
            resultsContainer.innerHTML = '<p class="text-center">No se encontraron productos</p>';
            return;
        }
        
        const grid = document.createElement('div');
        grid.className = 'row row-cols-1 row-cols-md-3 g-4';
        
        productos.forEach(producto => {
            const card = `
                <div class="col">
                    <div class="card h-100">
                        <img src="${producto.imagen}" class="card-img-top" alt="${producto.nombre}" onerror="this.src='img/no-image.png'">
                        <div class="card-body">
                            <h5 class="card-title">${producto.nombre}</h5>
                            <p class="card-text">
                                <strong>Precio:</strong> $${producto.precio}<br>
                                <strong>Tienda:</strong> ${producto.tienda}<br>
                                ${producto.vendedor ? `<strong>Vendedor:</strong> ${producto.vendedor}<br>` : ''}
                                <small class="text-muted">Actualizado: ${producto.ultima_actualizacion}</small>
                            </p>
                            <a href="${producto.url}" class="btn btn-primary" target="_blank">Ver en tienda</a>
                        </div>
                    </div>
                </div>
            `;
            grid.innerHTML += card;
        });
        
        resultsContainer.appendChild(grid);
    }
    
    function mostrarError(mensaje) {
        resultsContainer.innerHTML = `
            <div class="alert alert-danger" role="alert">
                ${mensaje}
            </div>
        `;
    }
});
