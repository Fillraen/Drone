let keysHeld = {};

document.addEventListener('keydown', function(event) {
    if (!keysHeld[event.key]) {
        keysHeld[event.key] = true;

        switch (event.key) {
            case 't':
                sendCommand('takeoff');
                break;
            case 'l':
                sendCommand('land');
                break;
            case 'c':
                sendCommand('photo');
                break;
            case 'r':
                sendCommand('record');
                break;
            // Commandes avec maintien continu
            case 'z':
                sendCommand('up');
                break;
            case 's':
                sendCommand('down');
                break;
            case 'q':
                sendCommand('counter_clockwise');
                break;
            case 'd':
                sendCommand('clockwise');
                break;
            case 'ArrowUp':
                sendCommand('forward');
                break;
            case 'ArrowDown':
                sendCommand('back');
                break;
            case 'ArrowLeft':
                sendCommand('left');
                break;
            case 'ArrowRight':
                sendCommand('right');
                break;
        }
    }
});

document.addEventListener('keyup', function(event) {
    if (keysHeld[event.key]) {
        keysHeld[event.key] = false;
        // Arrêter le mouvement continu lors du relâchement de la touche
        switch (event.key) {
            case 'z':
                sendCommand('stop');
                break;
            case 's':
                sendCommand('stop');
                break;
            case 'q':
                sendCommand('stop');
                break;
            case 'd':
                sendCommand('stop');
                break;
            case 'ArrowUp':
                sendCommand('stop');
                break;
            case 'ArrowDown':
                sendCommand('stop');
                break;
            case 'ArrowLeft':
                sendCommand('stop');
                break;
            case 'ArrowRight':
                sendCommand('stop');
                break;
        }
    }
});

function sendCommand(command) {
    fetch(`/command/${command}`)
        .then(response => response.json())
        .then(data => console.log(data))
        .catch(error => console.error('Erreur:', error));
}


document.addEventListener('keydown', function(event) {
    const keyMap = {
        'z': 'k90',  // Z key
        'q': 'k81',  // Q key
        's': 'k83',  // S key
        'd': 'k68',  // D key
        't': 'k84',  // T key
        'l': 'k76',  // L key
        'r': 'k82',  // R key
        'e': 'k69',  // E key
        'c': 'k67',
        'ArrowUp': 'k01',    // Up arrow
        'ArrowLeft': 'k02',  // Left arrow
        'ArrowDown': 'k03',  // Down arrow
        'ArrowRight': 'k04', // Right arrow
    };

    let keyID;
    if (event.key.startsWith('Arrow')) {
        keyID = keyMap[event.key];
    } else {
        keyID = keyMap[event.key.toLowerCase()];
    }

    if (keyID) {
        const keyElement = document.getElementById(keyID);
        if (keyElement) {
            keyElement.classList.add('active');
        }
    }
});

document.addEventListener('keyup', function(event) {
    const keyMap = {
        'z': 'k90',
        'q': 'k81',
        's': 'k83',
        'd': 'k68',
        't': 'k84',
        'l': 'k76',
        'r': 'k82',
        'e': 'k69',
        'c': 'k67',
        'ArrowUp': 'k01',
        'ArrowLeft': 'k02',
        'ArrowDown': 'k03',
        'ArrowRight': 'k04',
    };

    let keyID;
    if (event.key.startsWith('Arrow')) {
        keyID = keyMap[event.key];
    } else {
        keyID = keyMap[event.key.toLowerCase()];
    }

    if (keyID) {
        const keyElement = document.getElementById(keyID);
        if (keyElement) {
            keyElement.classList.remove('active');
        }
    }
});