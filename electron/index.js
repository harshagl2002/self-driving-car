document.onkeydown = updateKey;
document.onkeyup = resetKey;

var server_port = 65432;
var server_addr = "192.168.3.49";   // the IP address of your Raspberry PI

function client_runner() {
    const net = require('net');
    var input = document.getElementById('message').value;

    const client = net.createConnection({ port: server_port, host: server_addr }, () => {
        console.log('connected to server!');
        client.write(`${input}\r\n`);
    });
    
    client.on('data', (data) => {
        var receivedData = data.toString(); // Convert received data to string
        updateDOM(receivedData); // Update the DOM with received data
        client.end();
        client.destroy();
    });

    client.on('end', () => {
        console.log('disconnected from server');
    });
    resetKey();
}

function updateDOM(data) {
    // Update the Bluetooth element with the received data
    document.getElementById("bluetooth").textContent = data;
}

// for detecting which key is been pressed w,a,s,d

function updateKey(e) {

    e = e || window.event;
    if (e.keyCode == '87') {
        // up (w)
        document.getElementById("upArrow").style.color = "green";
        document.getElementById('message').value = "up";
    }
    else if (e.keyCode == '83') {
        // down (s)
        document.getElementById("downArrow").style.color = "green";
        document.getElementById('message').value = "down";
    }
    else if (e.keyCode == '65') {
        // left (a)
        document.getElementById("leftArrow").style.color = "green";
        document.getElementById('message').value = "left";
    }
    else if (e.keyCode == '68') {
        // right (d)
        document.getElementById("rightArrow").style.color = "green";
        document.getElementById('message').value = "right";
    } 
}

// reset the key to the start state 
function resetKey(e) {

    // e = e || window.event;
    document.getElementById("upArrow").style.color = "grey";
    document.getElementById("downArrow").style.color = "grey";
    document.getElementById("leftArrow").style.color = "grey";
    document.getElementById("rightArrow").style.color = "grey";
    document.getElementById('message').value = "none";
}



function update_data() {
    client_runner();
    setTimeout(update_data, 50);
}

