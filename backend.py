import gevent

class HappyBackend(object):
    """Interface for registering and updating WebSocket clients."""

    def __init__(self, redis_obj, channel, socketio):
        self.clients = list()
        self.pubsub = redis_obj.pubsub()
        self.pubsub.subscribe(channel)
        self.socketio = socketio
        print("Starting HappyBackend")

    def __iter_data(self):
        for message in self.pubsub.listen():
            print("message: {}".format(message))
            data = message.get('data')
            if message['type'] == 'message':
                #app.logger.info(u'Sending message: {}'.format(data))
                yield data

    def register(self, client):
        """Register a WebSocket connection for Redis updates."""
        print("backend registered client: {}".format(client))
        self.clients.append(client)

    def unregister(self, client):
        """Unregister a WebSocket connection for Redis updates."""
        print("backend unregistered client: {}".format(client))
        self.clients.remove(client)

    def send(self, client, data):
        """Send given data to the registered client.
        Automatically discards invalid connections."""
        try:
            #client.send(data)
            print("Sending to happymeter: {}".format(data))
            #client.emit("happymeter", data, namespace="/test")
            self.socketio.emit("happymeter", data, namespace="/test")
        except Exception, e:
            #self.clients.remove(client)
            print("Exception in Backend: {}".format(e))

    def run(self):
        """Listens for new messages in Redis, and sends them to clients."""
        for data in self.__iter_data():
            #gevent.spawn(self.send, None, data)
            for client in self.clients:
                print("Client: {}".format(client))
                gevent.spawn(self.send, client, data)

    def start(self):
        """Maintains Redis subscription in the background."""
        gevent.spawn(self.run)