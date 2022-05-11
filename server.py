#!/usr/bin/env python3

import logging
from flask_restful import Api
from flask import Flask, render_template

from ping import Ping
from InteractionWebhook import InteractionWebhook

app = Flask(__name__)
api = Api(app)


@app.route("/")
@app.route("/<string:name>")
def lmao(name=""):
    return render_template("index.html", name=name)


api.add_resource(Ping, "/ping", "/ping/<string:name>")
api.add_resource(InteractionWebhook, "/interactions", methods=["POST"])

logging.basicConfig(format='[%(asctime)s] %(levelname)s: %(message)s', level=logging.DEBUG,
                    filename='data/minecraft_automation.log', encoding='utf-8'
                    )
