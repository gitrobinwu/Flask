#-*- coding:utf-8 -*- 
from flask import render_template

@app.errorhandler(404)
def page_not_found(e):
	renter render_template('404.html'),404

{% extends "layout.html" %}	
{% block title %}Page Not Found{% endblock %}
{% block body %}
<h1>Page Not Found</h1>
<p>What you were looking for is just not there.
<p><a href="{{ url_for('index') }}">go somewhere nice</a>
{% endblock %}


