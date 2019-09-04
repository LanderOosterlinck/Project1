const IP = window.location.hostname + "http://169.254.10.1:5000"
const socket = io.connect('http://172.30.252.30:5000');
let toggleValue;



const init = function () {
    socket.on('connected', function (data) {
        toggleValue = data.value;
        showToggle()
    });
    socket.on('toggle', function (data) {
        console.log(data.value);
        toggleValue = data.value;
        showToggle()
    });
}

document.addEventListener('DOMContentLoaded', function () {
    console.info('DOM geladen');
    init();
});