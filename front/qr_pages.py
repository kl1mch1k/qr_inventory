import base64

import requests
from flask import redirect, send_file
from flask_login import current_user

from flask_app import app


@app.route('/download_qr')
def download():
    if current_user.is_authenticated:
        file = open('temp/temp.xlsx', 'wb')
        file.write(base64.b64decode(requests.get('http://127.0.0.1:5000/api/get_xlsx_qr').json()['xlsx'][2:-1]))
        return send_file('temp/temp.xlsx', as_attachment=True)
    else:
        return redirect('/login')
