
from transformers import pipeline
import socketserver
import sys
import time
from time import sleep
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

class RequestHandler(socketserver.ThreadingMixIn, SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

with SimpleXMLRPCServer(('0.0.0.0', 9000), requestHandler=RequestHandler) as server:
    print("Listening on port 9000")
    server.register_introspection_functions()
    server.register_multicall_functions()

    # Register a function under a different name
    @server.register_function(name='get_topic')
    def get_topic(str):
        print("New request arrived!")
        arrival_time = time.time()
        classifier = pipeline('zero-shot-classification', model='facebook/bart-large-mnli')
        labels = ["world", "sport", "business", "science/tech"]
        hypothesis_template = 'This text is about {}.'
        prediction = classifier(str, labels, hypothesis_template=hypothesis_template, multi_class=True)
        end_time = time.time()
        tot = end_time - arrival_time
        print(tot)
        print(prediction)
        return prediction["labels"][0], prediction["scores"][0]

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nKeyboard interrupt received, exiting.")
        sys.exit(0)