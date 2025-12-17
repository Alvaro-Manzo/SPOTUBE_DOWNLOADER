// API Configuration
const API_URL = 'http://localhost:5000/api';

// Estado global
let currentTaskId = null;
let checkInterval = null;

// Inicializar particles.js
particlesJS('particles-js', {
    particles: {
        number: {
            value: 80,
            density: {
                enable: true,
                value_area: 800
            }
        },
        color: {
            value: '#1db954'
        },
        shape: {
            type: 'circle'
        },
        opacity: {
            value: 0.5,
            random: false
        },
        size: {
            value: 3,
            random: true
        },
        line_linked: {
            enable: true,
            distance: 150,
            color: '#1db954',
            opacity: 0.4,
            width: 1
        },
        move: {
            enable: true,
            speed: 2,
            direction: 'none',
            random: false,
            straight: false,
            out_mode: 'out',
            bounce: false
        }
    },
    interactivity: {
        detect_on: 'canvas',
        events: {
            onhover: {
                enable: true,
                mode: 'repulse'
            },
            onclick: {
                enable: true,
                mode: 'push'
            },
            resize: true
        }
    },
    retina_detect: true
});

// Smooth scroll
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Download button handler
document.getElementById('downloadBtn').addEventListener('click', async () => {
    const url = document.getElementById('playlistUrl').value.trim();
    const name = document.getElementById('zipName').value.trim() || 'Mi_Musica';
    const quality = document.getElementById('quality').value;
    
    if (!url) {
        showError('Por favor ingresa una URL de Spotify');
        return;
    }
    
    if (!url.includes('spotify.com/playlist/')) {
        showError('URL inválida. Debe ser un link de playlist de Spotify');
        return;
    }
    
    await startDownload(url, name, quality);
});

async function startDownload(url, name, quality) {
    const downloadBtn = document.getElementById('downloadBtn');
    const buttonText = downloadBtn.querySelector('.button-text');
    const buttonLoader = downloadBtn.querySelector('.button-loader');
    const progressSection = document.getElementById('progressSection');
    const successSection = document.getElementById('successSection');
    
    // Reset UI
    successSection.classList.add('hidden');
    progressSection.classList.remove('hidden');
    downloadBtn.disabled = true;
    buttonText.textContent = '⏳ Descargando...';
    buttonLoader.classList.remove('hidden');
    
    try {
        // Iniciar descarga
        const response = await fetch(`${API_URL}/download`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                url: url,
                name: name,
                quality: quality,
                threads: 3
            })
        });
        
        if (!response.ok) {
            throw new Error('Error al iniciar la descarga');
        }
        
        const data = await response.json();
        currentTaskId = data.task_id;
        
        // Iniciar polling para verificar progreso
        startProgressCheck();
        
    } catch (error) {
        console.error('Error:', error);
        showError('Error al conectar con el servidor. Asegúrate de que el backend está corriendo.');
        resetUI();
    }
}

function startProgressCheck() {
    // Limpiar intervalo anterior si existe
    if (checkInterval) {
        clearInterval(checkInterval);
    }
    
    // Verificar progreso cada 2 segundos
    checkInterval = setInterval(async () => {
        try {
            const response = await fetch(`${API_URL}/status/${currentTaskId}`);
            const data = await response.json();
            
            updateProgress(data);
            
            if (data.status === 'completed') {
                clearInterval(checkInterval);
                showSuccess(data);
            } else if (data.status === 'error') {
                clearInterval(checkInterval);
                showError(data.error || 'Error durante la descarga');
                resetUI();
            }
        } catch (error) {
            console.error('Error checking status:', error);
        }
    }, 2000);
}

function updateProgress(data) {
    const progressFill = document.querySelector('.progress-fill');
    const progressPercentage = document.querySelector('.progress-percentage');
    const progressText = document.getElementById('progressText');
    
    let percentage = 0;
    let statusText = 'Preparando descarga...';
    
    if (data.status === 'downloading') {
        if (data.total_songs > 0) {
            percentage = Math.round((data.downloaded_songs / data.total_songs) * 90);
            statusText = `Descargando: ${data.downloaded_songs} de ${data.total_songs} canciones`;
        } else {
            percentage = 10;
            statusText = 'Buscando canciones en la playlist...';
        }
    } else if (data.status === 'compressing') {
        percentage = 95;
        statusText = 'Creando archivo ZIP...';
    }
    
    progressFill.style.width = `${percentage}%`;
    progressPercentage.textContent = `${percentage}%`;
    progressText.textContent = statusText;
}

function showSuccess(data) {
    const progressSection = document.getElementById('progressSection');
    const successSection = document.getElementById('successSection');
    const successMessage = document.getElementById('successMessage');
    const downloadZipBtn = document.getElementById('downloadZipBtn');
    
    progressSection.classList.add('hidden');
    successSection.classList.remove('hidden');
    
    successMessage.textContent = `¡${data.downloaded_songs} canciones descargadas exitosamente!`;
    
    downloadZipBtn.onclick = () => {
        window.location.href = `${API_URL}/download/${currentTaskId}`;
    };
    
    resetUI();
}

function showError(message) {
    // Crear notificación de error
    const notification = document.createElement('div');
    notification.className = 'notification error';
    notification.innerHTML = `
        <div style="background: rgba(220, 38, 38, 0.9); color: white; padding: 20px; border-radius: 12px; margin: 20px auto; max-width: 600px; text-align: center; box-shadow: 0 10px 30px rgba(0,0,0,0.5);">
            <strong>❌ Error</strong><br>
            ${message}
        </div>
    `;
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.remove();
    }, 5000);
}

function resetUI() {
    const downloadBtn = document.getElementById('downloadBtn');
    const buttonText = downloadBtn.querySelector('.button-text');
    const buttonLoader = downloadBtn.querySelector('.button-loader');
    
    downloadBtn.disabled = false;
    buttonText.textContent = '⬇️ Descargar Playlist';
    buttonLoader.classList.add('hidden');
}

// Verificar si el servidor está corriendo
async function checkServerHealth() {
    try {
        const response = await fetch(`${API_URL}/health`);
        if (response.ok) {
            console.log('✅ Servidor conectado');
        }
    } catch (error) {
        console.warn('⚠️ Servidor no disponible. Inicia el backend con: python api.py');
        showError('Servidor no disponible. Por favor inicia el backend ejecutando: python api.py');
    }
}

// Verificar servidor al cargar la página
checkServerHealth();

// Easter egg: Konami Code
let konamiCode = [];
const konamiPattern = ['ArrowUp', 'ArrowUp', 'ArrowDown', 'ArrowDown', 'ArrowLeft', 'ArrowRight', 'ArrowLeft', 'ArrowRight', 'b', 'a'];

document.addEventListener('keydown', (e) => {
    konamiCode.push(e.key);
    konamiCode = konamiCode.slice(-10);
    
    if (konamiCode.join('') === konamiPattern.join('')) {
        activateEasterEgg();
    }
});

function activateEasterEgg() {
    document.body.style.animation = 'rainbow 2s infinite';
    setTimeout(() => {
        document.body.style.animation = '';
    }, 10000);
}

// Animación rainbow para easter egg
const style = document.createElement('style');
style.textContent = `
    @keyframes rainbow {
        0% { filter: hue-rotate(0deg); }
        100% { filter: hue-rotate(360deg); }
    }
`;
document.head.appendChild(style);

// Log ASCII Art en consola
console.log(`
    ╔════════════════════════════════════════╗
    ║                                        ║
    ║    🎵  SPOTIFY DOWNLOADER PRO  🎵     ║
    ║                                        ║
    ║    El Mejor del Mundo 🌎              ║
    ║    Made by Alvaro Manzo                ║
    ║                                        ║
    ╚════════════════════════════════════════╝
`);
