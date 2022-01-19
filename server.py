
from transformers import pipeline
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

with SimpleXMLRPCServer(('0.0.0.0', 9000),
                        requestHandler=RequestHandler) as server:
    print("Listening on port 9000")
    server.register_introspection_functions()
    # Register len() function;
    server.register_function(len)
    # Register a function under a different name
    @server.register_function(name='get_topic')
    def get_topic(str):
        classifier = pipeline('zero-shot-classification', model='facebook/bart-large-mnli')
        labels = ["world", "sport", "business", "science/tech"]
        hypothesis_template = 'This text is about {}.'
        prediction = classifier(str, labels, hypothesis_template=hypothesis_template, multi_class=True)
        print(prediction)
        return prediction["labels"][0], prediction["scores"][0]
    server.serve_forever()