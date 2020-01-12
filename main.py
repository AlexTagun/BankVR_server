from server import Server

class MyServer(Server):
    def handle(self, message):
        try:
            print("Got: {}".format(message))
        except Exception as e:
            print("Error: {}".format(e))

if __name__ == "__main__":
    print("Alice started.")
    app = MyServer("localhost", 8888)
    app.start_server()
    app.loop()
    app.stop_server()