
function toggleForms() {
    const loginForm = document.getElementById('loginForm');
    const registerForm = document.getElementById('registerForm');
    const loginHeader = document.getElementById('loginHeader');
    const registerHeader = document.getElementById('registerHeader');
    
    if (loginForm.style.display === 'none') {
        loginForm.style.display = 'block';
        registerForm.style.display = 'none';
        loginHeader.style.opacity = '1';
        registerHeader.style.opacity = '0';
    } else {
        loginForm.style.display = 'none';
        registerForm.style.display = 'block';
        loginHeader.style.opacity = '0';
        registerHeader.style.opacity = '1';
    }
}

document.getElementById('loginForm').addEventListener('submit', function(e) {
    e.preventDefault(); // Prevenir el envío por defecto del formulario
    window.location.href = 'home.html'; // Redirigir a home.html
});