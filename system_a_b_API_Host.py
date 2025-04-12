# -*- coding: utf-8 -*-
"""
Created on Sat Apr 12 15:44:16 2025

@author: sally
"""
from flask import Flask, jsonify
import json
import os

app = Flask(__name__)

os.chdir(os.path.join(os.getcwd(), "Sources"))
with open("system_a.json") as f:
    system_a_data = json.load(f)

with open("system_b.json") as f:
    system_b_data = json.load(f)

@app.route("/system-a/companies", methods=["GET"])
def get_companies_a():
    return jsonify(system_a_data)

@app.route("/system-b/companies", methods=["GET"])
def get_companies_b():
    return jsonify(system_b_data)

if __name__ == "__main__":
    app.run(port=5000)