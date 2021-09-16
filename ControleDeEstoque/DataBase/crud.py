import pyodbc


class DataBase:
    def __init__(self, name):
        self.cnxn = pyodbc.connect(f"Driver=SQLite3 ODBC Driver;Database={name}.db")
        self.cursor = self.cnxn.cursor()
        print(f'Connected to the base {name}')
    
    def CreateTB(self, name):
        try:
            self.cursor.execute(f'''CREATE TABLE IF NOT EXISTS {name}
                                (id INTEGER PRIMARY KEY AUTOINCREMENT, code varchar(13), name varchar(30), amount int, price real, description varchar(100))''')
            self.cursor.commit()
            print(f'Table {name} created')
        except Exception as err:
            print("ERROR: Make sure there is no space between strings, ", err)

    def CreateTBClientes(self):
        try:
            self.cursor.execute(f'''CREATE TABLE IF NOT EXISTS clientes
                                (id INTEGER PRIMARY KEY AUTOINCREMENT, nome varchar(30), cpf varchar(15), rg varchar(15), celular varchar(20), email varchar(40))''')
            self.cursor.commit()
            print(f'Table clientes created')
        except Exception as err:
            print("ERROR: Make sure there is no space between strings, ", err) 
    
    def InsertValues(self, table, code, name, amount, price, description):
        try:
            self.cursor.execute(f'''INSERT INTO {table}(code, name, amount, price, description)
                                VALUES("{code}","{name}",{amount}, {price}, "{description}")''')
            self.cursor.commit()
            print('Values entered successfully')
        except Exception as err:
            print('ERROR: check if the values were filled in correctly ',err)

    def InsertCliente(self, table, nome, cpf, rg, celular, email):
        try:
            self.cursor.execute(f'''INSERT INTO {table}(nome, cpf, rg, celular, email)
                                VALUES("{nome}","{cpf}","{rg}", "{celular}", "{email}")''')
            self.cursor.commit()
            print('Values entered successfully')
        except Exception as err:
            print('ERROR: check if the values were filled in correctly ',err)

    def ViewData(self, table):
        try:
            self.cursor.execute(f'''SELECT * FROM {table};''')
            data_read = self.cursor.fetchall()
            return data_read
        except Exception as err:
            print('ERROR: check if the fields were filled in correctly ',err)

    def UpdateValues(self, table, code, name, amount, price, description, id):
        try:
            self.cursor.execute(f'''UPDATE {table} SET code="{code}",name="{name}", amount={amount}, price={price}, description="{description}" WHERE id={id}''')
            self.cursor.commit()
            print('Data updated successfully')     
        except Exception as err:
            print('ERROR: check if the fields were filled in correctly ',err)

    def DeleteValues(self, table, id):
        try:
            self.cursor.execute(f'''DELETE FROM {table} WHERE id={id};''')
            self.cursor.commit()
            print('Data successfully deleted')
        except Exception as err:
            print('ERROR: check if the fields were filled in correctly ',err)

    def SearchValues(self, table, column, search):
        self.cursor.execute(f'''SELECT * FROM {table} WHERE "{column}" LIKE "%{search}%" ''')
        data_read = self.cursor.fetchall()
        return data_read

    def TamanhoTabela(self, table):
        self.cursor.execute(f'''SELECT * FROM {table}''')
        data_read = self.cursor.fetchall()
        return len(data_read)
 
