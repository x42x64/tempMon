from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
import json


class HttpProvider(threading.Thread):
    dc = None
    lock = threading.Lock()

    def __init__(self, dataCollector, ip, port):
        threading.Thread.__init__(self)
        self.endRequest = False
        self.ip = ip
        self.port = port
        HttpProvider.dc = dataCollector


    class httpServer_RequestHandler(BaseHTTPRequestHandler):
        # GET
        def do_GET(self):
            # Send response status code
            self.send_response(200)

            # Send headers
            self.send_header('Content-type', 'application/json')
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Access-Control-Expose-Headers", "Access-Control-Allow-Origin")
            self.send_header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept")
            self.end_headers()

            # Send message back to client
            message = json.dumps(HttpProvider.dc.getCurrentData())
            # Write content as utf-8 data
            self.wfile.write(bytes(message, "utf8"))
            return

    def stopRequest(self):
        self.httpd.shutdown()

    def run(self):
        print('starting server...')

        # Server settings
        # Choose port 8080, for port 80, which is normally used for a http server, you need root access
        server_address = (self.ip, self.port)
        self.httpd = HTTPServer(server_address, HttpProvider.httpServer_RequestHandler)
        print('running server...')

        try:
            self.httpd.serve_forever()
        finally:
            self.httpd.server_close()