#!/usr/bin/env python3

import argparse
import logging
from flask_restful import Api
from flask import Flask, render_template

from resources.ping import Ping
from resources.InteractionWebhook import InteractionWebhook

app = Flask(__name__)
api = Api(app)


@app.route("/")
@app.route("/<string:name>")
def lmao(name=""):
    return render_template("index.html", name=name)


api.add_resource(Ping, "/ping", "/ping/<string:name>")
api.add_resource(InteractionWebhook, "/interactions", methods=["POST"])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the server")
    parser.add_argument("--host", default="")
    parser.add_argument("--port", default=5000, type=int)
    parser.add_argument("--debug", default=False, action="store_true")
    args = parser.parse_args()
    logging.basicConfig(format='[%(asctime)s] %(levelname)s: %(message)s', level=logging.DEBUG,
                        # filename='data/minecraft_automation.log', encoding='utf-8'
                        )
    app.run(host=args.host, port=args.port, debug=args.debug)
