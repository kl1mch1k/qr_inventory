import sqlite3

from openpyxl import load_workbook
from openpyxl.utils import column_index_from_string


def convert_from_xlsx_to_sqlite(xlsx_name, sheet_name, db_name, columns, take_rows_with_id_only=True):
    # Loading a workbook and required sheet
    wb = load_workbook(xlsx_name, read_only=True)
    sheet = wb[sheet_name]
    if db_name in os.listdir():
        raise FileExistsError

    # Creating a database and cursor
    con = sqlite3.connect(db_name)  # Creating a database and cursor
    cur = con.cursor()

    # Creating main table
    cur.execute('CREATE TABLE objects ('
                'id   INTEGER PRIMARY KEY AUTOINCREMENT,'
                '{},'
                'obj_place INTEGER,'
                'FOREIGN KEY (obj_place) REFERENCES places (id)'
                ');'.format(",".join([str(columns[column]) + " STRING" for column in columns.keys()])))

    # Creating places history table
    cur.execute('CREATE TABLE history ('
                'id       INTEGER PRIMARY KEY AUTOINCREMENT,'
                'old_place_id INTEGER,'
                'new_place_id INTEGER,'
                'date     DATETIME,'
                'obj_id   INTEGER,'
                'FOREIGN KEY (obj_id) REFERENCES objects (id) ON DELETE CASCADE,'
                'FOREIGN KEY (new_place_id) REFERENCES places (id),'
                'FOREIGN KEY (old_place_id) REFERENCES places (id));')

    # Creating places table
    cur.execute('CREATE TABLE places ('
                'id   INTEGER PRIMARY KEY AUTOINCREMENT,'
                'text STRING);')

    # Creating update trigger that sets last place to objects when history table updates
    cur.execute(
        'CREATE TRIGGER UpdateTrigger AFTER INSERT ON '
        'history BEGIN UPDATE objects SET obj_place = (NEW.new_place_id)'
        'WHERE objects.id = NEW.obj_id; END;')

    cur.execute(
        'CREATE TABLE users ('
        'id              INTEGER PRIMARY KEY AUTOINCREMENT,'
        'email           STRING,'
        'hashed_password STRING);')

    cur.execute(
        'CREATE TABLE user_responsibility ('
        'user_id         INTEGER ,'
        'obj_id          INTEGER);')

    # Adding data
    for row in sheet.rows:
        if take_rows_with_id_only:
            if not str(row[0].value).isdigit():
                continue
        cur.execute('''INSERT INTO objects({})
                       VALUES({})'''.format(','.join(columns.values()),
                                            ','.join(["'" + str(row[column_index_from_string(i) - 1].value) + "'"
                                                      for i in columns.keys()])))
    con.commit()
    con.close()
    wb.close()


import os

os.remove('db/inventory_new.db')
print(convert_from_xlsx_to_sqlite('inventory_old.xlsx', 'стр.2',
                                  'db/inventory_new.db',
                                  ({'G': 'name',
                                    'H': 'serial_number'})))
