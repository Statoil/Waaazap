var socket,
    obj,
    url;


$(document).ready(function() {
    url = '/test';
    socket = io.connect(url);
    socket.on('my response', function(msg) {
        $('#log').prepend('<p>Received: ' + msg.data + '</p>');
    });

    socket.on('crap_data', function(msg) {
        $('#log').prepend("<p>Data: " + msg.data + "</p>");
    });

    socket.on('connected', function() {
        $('#log').append('<p>Connected!</p>');
        
    });

    socket.on('happymeter', function(msg) {
        console.log("Got happy signal: ", msg);
        msg = JSON.parse(msg);
        if (msg.status == "ok") {
            console.log("Got an OK signal");
            $('#log').prepend("<p>Button pushed: " + msg.signal + " (#" + msg.value +")</p>");
            updateGraph();
        } else {
            console.log("Bad signal.. ", msg);
        }
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
        return false;
    });
});