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
