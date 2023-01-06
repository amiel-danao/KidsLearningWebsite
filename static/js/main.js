const date = new Date();
document.querySelector('.year').innerHTML = date.getFullYear();


$(document).ready(function () {
    var message = $('#message');
    if (message.length) {
        setTimeout(function () {
            console.log(message);
            message.fadeout('slow')
        }, 3000);
    }
});