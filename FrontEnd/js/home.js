// Elementos DOM
const searchForm = document.querySelector('.search-container form');
const filterSelect = document.querySelector('.filters-sidebar select');
const priceInputs = document.querySelectorAll('.filters-sidebar input[type="number"]');
const categoryCheckboxes = document.querySelectorAll('.filters-sidebar input[type="checkbox"]');
const btnReportar = document.getElementById('btnReportar');
const btnLogout = document.getElementById('btnLogout');
const addToCartButtons = document.querySelectorAll('.btn-primary.btn-sm');

// Manejador de búsqueda
searchForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const searchTerm = e.target.querySelector('input').value;
    handleSearch(searchTerm);
});

// Manejador de filtros
filterSelect.addEventListener('change', (e) => {
    const selectedFilter = e.target.value;
    applyFilters();
});

// Manejador de rango de precios
priceInputs.forEach(input => {
    input.addEventListener('change', () => {
        applyFilters();
    });
});

// Manejador de categorías
categoryCheckboxes.forEach(checkbox => {
    checkbox.addEventListener('change', () => {
        applyFilters();
    });
});

// Manejador de reportar problema
btnReportar.addEventListener('click', () => {
    reportarProblema();
});

// Manejador de cerrar sesión
btnLogout.addEventListener('click', () => {
    cerrarSesion();
});

// Manejador de agregar al carrito
addToCartButtons.forEach(button => {
    button.addEventListener('click', (e) => {
        const productCard = e.target.closest('.product-card');
        const productInfo = getProductInfo(productCard);
        addToCart(productInfo);
    });
});

// Funciones de manejo
function handleSearch(searchTerm) {
    console.log('Buscando:', searchTerm);
    // Implementar lógica de búsqueda
}

function applyFilters() {
    const selectedFilter = filterSelect.value;
    const minPrice = priceInputs[0].value;
    const maxPrice = priceInputs[1].value;
    const selectedCategories = Array.from(categoryCheckboxes)
        .filter(cb => cb.checked)
        .map(cb => cb.id);

    console.log('Aplicando filtros:', {
        ordenamiento: selectedFilter,
        precioMin: minPrice,
        precioMax: maxPrice,
        categorias: selectedCategories
    });
    // Implementar lógica de filtrado
}

function reportarProblema() {
    console.log('Abriendo formulario de reporte');
    // Implementar lógica de reporte
}

function cerrarSesion() {
    console.log('Cerrando sesión');
    // Implementar lógica de cierre de sesión
}

function getProductInfo(productCard) {
    return {
        nombre: productCard.querySelector('.card-title').textContent,
        precio: productCard.querySelector('.price-tag').textContent,
        tienda: productCard.querySelector('.store-badge').textContent
    };
}

function addToCart(productInfo) {
    console.log('Agregando al carrito:', productInfo);
    // Implementar lógica de agregar al carrito
}
