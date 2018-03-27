# -*- coding: utf-8 -*-
"""
    Calculator
    ~~~~~~~~~~~~~~

    A simple Calculator made by Flask and jQuery.

    :copyright: (c) 2015 by Grey li.
    :license: MIT, see LICENSE for more details.
"""
import re
from flask import Flask, jsonify, render_template, request

#@app.route('/_calculate')
def calculate():
    a = request.args.get('number1', '0')
    operator = request.args.get('operator', '+')
    b = request.args.get('number2', '0')
    m = re.match('-?\d+', a)
    n = re.match('-?\d+', b)
    if m is None or n is None or operator not in '+-*/':
        return jsonify(result='I Catch a BUG!')
    if operator == '/':
        result = eval(a + operator + str(float(b)))
    else:
        result = eval(a + operator + b)
    return jsonify(result=result)


#@app.route('/')
def index():
    return render_template('index.html')

def create_app():
    app = Flask(__name__)
    app.add_url_rule('/', 'index', view_func=index)
    app.view_functions['index'] = index
    app.add_url_rule('/_calculate', 'calculate', view_func=calculate)
    app.view_functions['calculate'] = calculate
    return app

app = create_app()

if '__main__' == __name__:
    app.run()

    #app.run()
