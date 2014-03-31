#!/usr/bin/env python
from sbcswebsite.application import app
from sbcswebsite.models import db

db.create_all()