import base64
import datetime
import io
from pprint import pprint

import PIL.Image
import numpy as np
import openpyxl
import qrcode
from PIL import Image

from data import db_session
from data.db_session import global_init
from data.history import History
from data.objects import Object
from data.places import Place
import requests

# global_init('db/inventory_new.db')
# db_sess = db_session.create_session()
# objects = db_sess.query(Object)
# places = db_sess.query(Place)
# # pprint(objects)
# places_with_objects = [[place, [obj.name for obj in objects.filter(Object.obj_place == place.id).all()]]
#                        for place in places]
# pprint(places_with_objects)
# print(db_sess.query(Object).filter(Object.id == 5).first().serial_number)
# log = History(place_id=1, obj_id=3)
# db_sess.add(log)
# db_sess.commit()

# pprint.pprint(requests.post('http://127.0.0.1:5000/api/history',
#                             json={'place_id': 3,
#                                   'date': datetime.datetime(2020, 12, 20).timestamp(),
#                                   'obj_id': 3}))
# print(bytes("b'ads'", 'utf-8'))
# img = requests.get('http://127.0.0.1:5000/api/get_json_qr', json={'id': ['2']}).json()['qr_codes']['2']['qr']
#
# new_image = Image.fromarray(np.array(img))
# new_image.save('out.png')
#
# requests.get('http://127.0.0.1:5000/api/get_xlsx_qr', json={'id': [str(i) for i in range(1, 100)]})

# import openpyxl
#
# wb = openpyxl.Workbook()
# ws = wb.worksheets[0]
# img = openpyxl.drawing.image.Image('out.png')
# print(img.width)
# ws.column_dimensions["A"].width = 20
# ws.row_dimensions[1].height = 80
# ws.add_image(img, 'A1')
# wb.save('out.xlsx')
