import psycopg2
import json
import os
import time

# Nome do arquivo JSON
JSON_FILE = "dados_ficticios.json"

# Configurações do banco de dados PostgreSQL
DB_CONFIG = {
    'dbname': 'postgres',
    'user': 'postgres',
    'password': '123',
    'host': 'localhost',
    'port': '5432'
}

class Database:
    def __init__(self, config):
        self.config = config

    def connection(self):
        return psycopg2.connect(**self.config)

    def create_table(self):
        conn = self.connection()
        cursor = conn.cursor()
        cursor.execute(""" 
        CREATE TABLE IF NOT EXISTS clients (
            id SERIAL PRIMARY KEY,
            nome TEXT NOT NULL,
            email TEXT NOT NULL,
            idade INTEGER NOT NULL,
            endereco TEXT NOT NULL
        )
        """)
        conn.commit()
        conn.close()

    def insert_user(self, data):
        conn = self.connection()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO clients (nome, email, idade, endereco) VALUES (%s, %s, %s, %s)", 
                           (data["nome"], data["email"], data["idade"], data["endereco"]))
            conn.commit()
            print(f"User {data['nome']} created successfully!")
        except psycopg2.IntegrityError as e:
            print(f"Error inserting user {data['nome']}: {e}")
        finally:
            conn.close()

    def read_clients(self):
        conn = self.connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM clients")
        clients = cursor.fetchall()
        conn.close()

        clients_list = [{"id": row[0], "nome": row[1], "email": row[2], "idade": row[3], "endereco": row[4]} for row in clients]
        return clients_list


class FileManager:
    def __init__(self, file_path):
        self.file_path = file_path
        self.last_mod_time = 0

    def get_modification_time(self):
        return os.path.getmtime(self.file_path)

    def read_json(self):
        with open(self.file_path, "r", encoding="utf-8") as file:
            return json.load(file)

    def file_changed(self):
        current_mod_time = self.get_modification_time()
        if current_mod_time != self.last_mod_time:
            self.last_mod_time = current_mod_time
            return True
        return False


class DataUpdater:
    def __init__(self, db, file_manager):
        self.db = db
        self.file_manager = file_manager

    def insert_clients_from_json(self):
        clients = self.file_manager.read_json()
        for user in clients:
            self.db.insert_user(user)

    def update_database_if_file_changed(self):
        while True:
            if self.file_manager.file_changed():
                print(f"File has changed. Updating the database...")
                self.db.create_table()  # Garante que a tabela exista
                self.insert_clients_from_json()  # Insere os usuários do arquivo JSON
            time.sleep(10)  # Verifica a cada 10 segundos


# Inicializa as classes
if __name__ == "__main__":
    db = Database(DB_CONFIG)
    file_manager = FileManager(JSON_FILE)
    data_updater = DataUpdater(db, file_manager)

    # Inicia o processo de atualização do banco de dados quando houver alterações no arquivo JSON
    data_updater.update_database_if_file_changed()
