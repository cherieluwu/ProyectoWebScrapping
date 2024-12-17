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

// Validación de formulario de registro
document.getElementById('registerForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const email = document.getElementById('registerEmail').value;
    const username = document.getElementById('registerUsername').value;
    const password = document.getElementById('registerPassword').value;
    const confirmPassword = document.getElementById('confirmPassword').value;

    // Validaciones del lado del cliente
    if (password !== confirmPassword) {
        alert('Las contraseñas no coinciden');
        return;
    }

    try {
        const response = await fetch('http://localhost:5000/api/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
            },
            credentials: 'include',
            body: JSON.stringify({
                email,
                username,
                password
            })
        });

        const data = await response.json();
        
        if (response.ok) {
            alert('Registro exitoso');
            toggleForms(); // Volver al formulario de login
        } else {
            alert(data.error);
        }
    } catch (error) {
        alert('Error al registrar usuario');
        console.error('Error:', error);
    }
});

// Validación de formulario de login
document.getElementById('loginForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const email = document.getElementById('loginEmail').value;
    const password = document.getElementById('loginPassword').value;

    try {
        const response = await fetch('http://localhost:5000/api/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
            },
            credentials: 'include',
            body: JSON.stringify({
                email,
                password
            })
        });

        const data = await response.json();
        
        if (response.ok) {
            // Guardar información del usuario en sessionStorage
            sessionStorage.setItem('username', data.username);
            window.location.href = 'home.html';
        } else {
            alert(data.error);
        }
    } catch (error) {
        alert('Error al iniciar sesión');
        console.error('Error:', error);
    }
});