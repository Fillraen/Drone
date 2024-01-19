function showStep(stepNumber) {
    // Hide all steps
    document.getElementById('step1').style.display = 'none';
    document.getElementById('step2').style.display = 'none';
    document.getElementById('step3').style.display = 'none';

    // Show the requested step
    document.getElementById('step' + stepNumber).style.display = 'block';

    switch('step' + stepNumber){
        case "step1":
            sendCommand("etape1")
        case "step2":
            sendCommand("etape2")
        case "step3":
            sendCommand("etape3")
    }
  }

  function sendCommand(command) {
    fetch(`/securityCommand/${command}`)
        .then(response => response.json())
        .then(data => console.log(data))
        .catch(error => console.error('Erreur:', error));
}