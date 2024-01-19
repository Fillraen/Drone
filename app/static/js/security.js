var canvas = document.getElementById('monCanvas');
var context = canvas.getContext('2d');
var radioCarre = document.getElementById('radioCarre');
var radioCercle = document.getElementById('radioCercle');
var tailleInfo = document.getElementById('tailleInfo');
var isDrawing = false;
var startX, startY;
function pixelsToCm(pixels) {
    return pixels / dpi * 2.54;
}

function resetCanvas() {
    context.clearRect(0, 0, canvas.width, canvas.height);
    tailleInfo.textContent = '';
}

canvas.addEventListener('mousedown', function(e) {
    isDrawing = true;
    startX = e.offsetX;
    startY = e.offsetY;
});

canvas.addEventListener('mousemove', function(e) {
    if (isDrawing === true) {
        drawShape(e.offsetX, e.offsetY);
    }
});

canvas.addEventListener('mouseup', function(e) {
    if (isDrawing === true) {
        drawShape(e.offsetX, e.offsetY);
        isDrawing = false;
    }
});

function drawShape(x, y) {
    var width = x - startX;
    var height = y - startY;
    var size = Math.min(Math.abs(width), Math.abs(height));

    if (width < 0) startX = x;
    if (height < 0) startY = y;

    context.clearRect(0, 0, canvas.width, canvas.height);
    context.strokeStyle = 'black';

    if (radioCarre.checked) {
        context.strokeRect(startX, startY, size, size);
        var tailleCm = pixelsToCm(size).toFixed(2);
        tailleInfo.textContent = 'Taille du côté du carré : ' + tailleCm + ' cm';
        print("taille : ", tailleCm)
        sendSecurityCommand(tailleCm)
    } else if (radioCercle.checked) {
        var radius = size / 2;
        var centerX = startX + radius;
        var centerY = startY + radius;
        context.beginPath();
        context.arc(centerX, centerY, radius, 0, 2 * Math.PI);
        context.stroke();
        var tailleCm = pixelsToCm(2 * radius).toFixed(2);
        tailleInfo.textContent = 'Diamètre du cercle : ' + diametreCm  + ' cm';
        print("taille : ", tailleCm)
        sendSecurityCommand(tailleCm)
    }
    
    
}var dpi = 96; // Valeur DPI standard; vous pouvez permettre aux utilisateurs de la modifier





function showStep(stepNumber) {
    // Hide all steps
    document.getElementById('step1').style.display = 'none';
    document.getElementById('step2').style.display = 'none';
    document.getElementById('step3').style.display = 'none';

    // Show the requested step
    document.getElementById('step' + stepNumber).style.display = 'block';
    /*
    switch('step' + stepNumber){
        case "step1":
            sendSecurityCommand("etape1")
        case "step2":
            sendSecurityCommand("etape2")
        case "step3":
            sendSecurityCommand("etape3")
    }
    */
  }

  function sendSecurityCommand(command) {
    fetch(`/securityCommand/${command}`)
        .then(response => response.json())
        .then(data => console.log(data))
        .catch(error => console.error('Erreur:', error));
}
