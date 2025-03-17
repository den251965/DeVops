import json
import time
# from array import *
import collections

from http.server import SimpleHTTPRequestHandler, HTTPServer
import psycopg2

port = 8585
table = 'сadri'

Person = collections.namedtuple("Person", ["name", "family", "doljnost"])
defaultcadri = Person("Иванов", "Иван", "Директор"),("Петров", "Иван", "Зам.Директора"),("Сидоров", "Иван", "Зам.Зам.Директор")

#Проверка наличия таблицы и при необходимости создание ее с добавление 3 записей
def isCreated_DB():
    cur = conn.cursor()
    # Создание таблицы Фамилия Имя должность
    cur.execute('SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = %s) AS table_exists;', (table,))
    existtable = bool(cur.fetchone()[0])
    cur.close()
    print(existtable)
    if existtable == False :
        print(f"table \t{table} not exists, creat....")
        cur = conn.cursor()
        cur.execute(f'CREATE TABLE IF NOT EXISTS \t{table} (id SERIAL PRIMARY KEY, name VARCHAR(100), family VARCHAR(100), doljnost VARCHAR(100));')
        cur.close()
        #Вставка дефолтных значений
        Insert_DB(defaultcadri)
        # отображение того, что вставили
        rows = AllEntries()
        print(f"table created \t{table} success, added 3 entries: ")
        print(rows)
    else :
        print(f"table \t{table} exists")

# Извлечение всех записей из таблицы servers
def AllEntries() :
    cur = conn.cursor()    
    cur.execute(f"SELECT id, name, family, doljnost FROM \t{table};")
    rows = cur.fetchall()
    cur.close()
    return rows

# Вставка блока записей
def Insert_DB(datainput):
    print(f"Insert from table \t{table}")
    cur = conn.cursor()
    for name, family, doljnost in datainput :
       cur.execute(f"INSERT INTO \t{table} (name, family, doljnost) VALUES (%s, %s, %s);", (name, family, doljnost))        
    conn.commit()
    cur.close()

# Обновление блока записей
def Update_DB(id, name, family, doljnost ): 
    print(f"Update from table \t{table}")   
    cur = conn.cursor()
    cur.execute(f"UPDATE \t{table} SET name = %s, family = %s, doljnost = %s WHERE  id = \t{id};", (name, family, doljnost))
    conn.commit()
    cur.close()

# Удаление блока записей
def Delete_DB(id): 
    cur = conn.cursor()
    print(f"Delete from table \t{table}")
    cur.execute( f"DELETE FROM \t{table} WHERE id = \t{id};")
    conn.commit()
    cur.close()

# Сервер
class MyHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"Hello otdel kadrov, this is a GET response!")

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        
        
        response = f"Received POST data: {post_data.decode('utf-8')}"
        self.wfile.write(response.encode('utf-8'))

if __name__ == '__main__':
    # Небольшая задержка
    # time.sleep(40)
    # Работа с БД
    conn = psycopg2.connect('postgresql://postgres:cadri@localhost:5432/postgres')
    isCreated_DB()

    # cadri = Person("Перл", "Иван", "Директор"),
    # Insert_DB(cadri)

    # Update_DB(2, "ggh", "tydtr", "dtrhtr")
    # Delete_DB(3)


    # Запуск сервера
    server_address = ('', port)
    httpd = HTTPServer(server_address, MyHandler)
    print(f"Starting server on port \t{port}...")
    httpd.serve_forever()


   