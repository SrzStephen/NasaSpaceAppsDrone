from flask import Flask
from flask import request
import click
import logging
logger = logging.getLogger(__name__)
app = Flask(__name__)
from .controls import Actuators
Actuators(prop_pin=1, rud_pin=2, el1_pin=3, el2_pin=4, alt_pin=5)

@click.command()
@click.option("-v", "--verbose", default=0, count=True, help="Verbosity to run script at", type=int)
@click.option("-p", "--port", default=6000, help="Port to receive data on", type=int)
def run(verbose, port):
    # set up logging
    logging.basicConfig(level=logging.getLevelName(verbose * 10 + 10))
    app.run(host='0.0.0.0', port=port)


@app.route('/', methods=['POST'])
def post_data():
    data = request._cached_json[0]
    Actuators.set_values(data)
    return "hello there"



if __name__ == "__main__":
    logging.basicConfig(level=logging.getLevelName(0 * 10 + 10))
    app.run(host='0.0.0.0', port=6000)

