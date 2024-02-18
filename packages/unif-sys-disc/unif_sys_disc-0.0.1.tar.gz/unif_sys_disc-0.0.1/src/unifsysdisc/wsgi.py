import logging
import flask
import paste.translogger

LOG_FORMAT = "%(asctime)s %(message)s"
DATE_FORMAT = "%Y-%m-%dT%H:%M:%S%z"
MSG_FORMAT = (
    "%(REMOTE_ADDR)s - %(REMOTE_USER)s "
    '"%(REQUEST_METHOD)s %(REQUEST_URI)s %(HTTP_VERSION)s" '
    '%(status)s %(bytes)s "%(HTTP_REFERER)s" "%(HTTP_USER_AGENT)s"'
)

logging.basicConfig(format=LOG_FORMAT, datefmt=DATE_FORMAT, level=logging.INFO)
app = flask.Flask("unif-sys-disc")
wsgi = paste.translogger.TransLogger(
    app, format=MSG_FORMAT, setup_console_handler=False
)


@app.post("/graph-model")
def create_graph_model():
    """
    Create a graph model in the SKG.
    """
    return "<p>Created a graph model.</p>"


@app.post("/automaton")
def create_automaton():
    """
    Create an automaton in the SKG.
    """
    return "<p>Created an automaton.</p>"


@app.post("/petri-net")
def create_petri_net():
    """
    Create a petri net in the SKG.
    """
    return "<p>Created a Petri net.</p>"


if __name__ == "__main__":
    import waitress

    waitress.serve(wsgi, host="localhost")
