import random
import tornado.ioloop
import tornado.web
import tornado.websocket

class WebSocketServer(tornado.websocket.WebSocketHandler):
    clients = set()

    def open(self):
        WebSocketServer.clients.add(self)
        print("Client connected")

    def on_close(self):
        WebSocketServer.clients.remove(self)
        print("Client disconnected")

    @classmethod
    def send_message(cls, message: str):
        print(f"Sending message '{message}' to {len(cls.clients)} client(s).")
        for client in cls.clients:
            client.write_message(message)

class RandomWordSelector:
    def __init__(self, word_list):
        self.word_list = word_list

    def sample(self):
        return random.choice(self.word_list)

def main():
    app = tornado.web.Application([
        (r"/websocket/", WebSocketServer)
    ])

    app.listen(8888)
    print("WebSocket server started at ws://localhost:8888/websocket/")

    io_loop = tornado.ioloop.IOLoop.current()
    word_selector = RandomWordSelector(['apple', 'banana', 'orange', 'grape', 'melon'])

    periodic_callback = tornado.ioloop.PeriodicCallback(
        lambda: WebSocketServer.send_message(word_selector.sample()),
        3000  # gửi mỗi 3 giây
    )
    periodic_callback.start()
    io_loop.start()

if __name__ == "__main__":
    main()