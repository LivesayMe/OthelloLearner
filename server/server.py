# server.py
# Author: Hunter Livesay
# Date: 1/6/2023
# Description: A flask server for hosting the othello game
# 
# General Notes
# Black = -1, White = 1, Empty = 0

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


