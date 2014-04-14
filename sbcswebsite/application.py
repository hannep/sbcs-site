import flask
from flask import Flask, request
from flask import render_template, redirect, url_for
from base64 import urlsafe_b64encode as b64encode

import datetime
import os
import sbcswebsite.config

app = Flask("sbcswebsite")
app.config.from_object(sbcswebsite.config.config)

