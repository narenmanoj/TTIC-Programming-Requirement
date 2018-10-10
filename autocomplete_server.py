# implementation adapted from https://www.acmesystems.it/python_http

from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from autocomplete import Autocomplete
import json


PORT_NUMBER = 8080
ac = Autocomplete(load=True)

# This class will handles any incoming request from
# the browser


class AutocompleteServer(BaseHTTPRequestHandler):

    # Handler for the GET requests
    def do_GET(self):
        query = urlparse(self.path).query
        query_components = parse_qs(urlparse(self.path).query)
        if "q" in query_components:
            phrase = query_components["q"][0]
            results = json.dumps(
                {"Completions": ac.generate_completions(phrase)})
            print(results)
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(results.encode())
        print("END OF REQUEST")
        return


try:
    # Create a web server and define the handler to manage the
    # incoming request
    server = HTTPServer(("", PORT_NUMBER), AutocompleteServer)
    print("Started httpserver on port %d" % PORT_NUMBER)

    # Wait forever for incoming htto requests
    server.serve_forever()

except KeyboardInterrupt:
    print("^C received, shutting down the web server")
    server.socket.close()