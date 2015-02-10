var socket,
    obj,
    url;

var colors = ["#98abc5", "#8a89a6", "#7b6888", "#6b486b", "#a05d56", "#d0743c", "#ff8c00"];

$(document).ready(function() {
    url = 'wss' + 
        '://' + document.location.hostname + 
        (document.location.port? ':' + document.location.port : '') + '/test';

    url = '/test';
    console.log("url: ", url);
    socket = io.connect(url);
    socket.on('my response', function(msg) {
        $('#log').prepend('<p>Received: ' + msg.data + '</p>');
    });

    socket.on('crap_data', function(msg) {
        $('#log').prepend("<p>Data: " + msg.data + "</p>");
    });

    socket.on('connected', function() {
        $('#log').append('<p>Connected!</p>');
        $.getJSON("/happymeter/test1")
            .done(function(json) {
                console.log("json: ", json);
                obj = json;
                var keys = Object.keys(json.test1);
                var color = d3.scale.ordinal()
                    .domain(keys)
                    .range(colors.slice(0,keys.length));
                var labels = color.domain();
                labels.map(function(label){
                    console.log("label -> " + label);
                    console.log("value -> " + json.test1[label]);
                    return {
                        label: label, 
                        value: json.test1[label]
                    }
                });

                changeGraph(labels);
            })
            .fail(function(json) {
                console.log("get data failed!");
            });
    });

    socket.on('happymeter', function(msg) {
        console.log("Got happy signal: ", msg);
        msg = JSON.parse(msg);
        if (msg.status == "ok") {
            console.log("Got an OK signal");
            $('#log').prepend("<p>Button pushed: " + msg.signal + " (#" + msg.value +")</p>");

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

        //socket.emit('my broadcast event', {data: $('#emit_data').val()});
        return false;
    });
});