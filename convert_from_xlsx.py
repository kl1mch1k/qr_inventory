def convert_from_xlsx_to_sqlite(xlsx_name, sheet_name, db_name, columns, take_rows_with_id_only=True):
    from openpyxl import load_workbook
    from openpyxl.utils import column_index_from_string
    import sqlite3
    import os
    # Loading a workbook and required sheet
    try:
        wb = load_workbook(xlsx_name, read_only=True)
        sheet = wb[sheet_name]
        if db_name in os.listdir():
            raise FileExistsError

        # Creating a database and cursor
        con = sqlite3.connect(db_name)  # Creating a database and cursor
        cur = con.cursor()

        # Normalizing column letters to int list indexes
        for i in range(len(columns)):
            columns[i]['column_index'] = column_index_from_string(columns[i]['column_index'])

        # Creating main table
        cur.execute('CREATE TABLE objects ('
                    'id   INTEGER PRIMARY KEY AUTOINCREMENT,'
                    '{});'.format(",".join([str(column["column_name"]) + " STRING" for column in columns])))

        # Adding data
        for row in sheet.rows:
            if take_rows_with_id_only:
                if not str(row[0].value).isdigit():
                    continue
            cur.execute('''INSERT INTO objects({})
                           VALUES({})'''.format(','.join([column['column_name'] for column in columns]),
                                                ','.join(["'" + str(row[i['column_index'] - 1].value) + "'"
                                                          for i in columns])))
        con.commit()
        con.close()
        wb.close()

    except Exception as e:
        return e


# import os
# os.remove('inventory_new.db')
print(convert_from_xlsx_to_sqlite('inventory_old.xlsx', 'стр.2',
                                  'inventory_new.db',
                                  ({'column_index': 'G', 'column_name': 'name'},
                                   {'column_index': 'H', 'column_name': 'number'})))
