import datetime
import pprint

from data import db_session
from data.db_session import global_init
from data.history import History
from data.objects import Object
from data.places import Place
import requests

# global_init('db/inventory_new.db')
# db_sess = db_session.create_session()
# print(db_sess.query(Object).filter(Object.id == 5).first().serial_number)
# log = History(place_id=1, obj_id=3)
# db_sess.add(log)
# db_sess.commit()

pprint.pprint(requests.post('http://127.0.0.1:5000/api/history',
                            json={'place_id': 3,
                                  'date': datetime.datetime(2020, 12, 20).timestamp(),
                                  'obj_id': 3}))
pprint.pprint(requests.get('http://127.0.0.1:5000/api/history').json())
