var socket,
    url;
$(document).ready(function() {
    url = 'wss' + 
        '://' + document.location.hostname + 
        (document.location.port? ':' + document.location.port : '') + '/test';

    url = 'wss://waaazap.herokuapp.com/test';
    console.log("url: ", url);
    socket = io.connect(url);
    socket.on('my response', function(msg) {
        $('#log').append('<p>Received: ' + msg.data + '</p>');
    });

    socket.on('crap_data', function(msg) {
        $('#log').append("<p>Data: " + msg.data + "</p>");
    });

    socket.on('connected', function() {
        socket.emit('random_nr');
    });

    $('form#emit').submit(function(event) {
        console.log("emit..");
        socket.emit('my event', {data: $('#emit_name').val()});
        return false;
    });

    $('form#broadcast').submit(function(event) {
        console.log("broadcast..");
        socket.emit('my broadcast event', {data: $('#emit_broadcast').val()});
        return false;
    });


    $('form').submit(function(event) {
        var data = $("#emit_name").val();
        var broadcast = $("#emit_broadcast").val();

        if (data && !broadcast) {
            console.log("my event: ", data);
            socket.emit('my event', {data: data});
        } else if (!data && broadcast) {
            console.log("my broadcast event: ", broadcast);
            socket.emit('my broadcast event', {data: broadcast});
        } else if (data && broadcast) {
            socket.emit('my event', {data: data});
            socket.emit('my broadcast event', {data: broadcast});
        } else {
            console.log("data: ", data);
            console.log("broadcast: ", broadcast);
            $('#log').append('<p>Missing data..</p>');
        }

        //socket.emit('my broadcast event', {data: $('#emit_data').val()});
        return false;
    });
});