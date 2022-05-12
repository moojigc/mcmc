#!/usr/bin/env python3

import argparse
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

args = argparse.ArgumentParser()
args.add_argument("--debug", action=argparse.BooleanOptionalAction)
args.add_argument("--log-to-file", action=argparse.BooleanOptionalAction)
parsed_args = args.parse_args()
