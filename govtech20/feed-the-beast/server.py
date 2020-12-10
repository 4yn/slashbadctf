#!/usr/bin/env python3

from flask import Flask, Response, request, render_template
from json import loads

app = Flask(__name__, static_folder='.', template_folder='.')

@app.route('/')
def dynamic_feed():
  data = {
    'title': request.args.get('title')
  }
  print(request.args.get('title'))
  xml = render_template('feed.xml', **data)
  return Response(xml, mimetype='application/xml')

@app.route('/static')
def static_feed():
  return app.send_static_file('static.xml')

if __name__ == '__main__':
  app.run(port=3000, debug=True)
