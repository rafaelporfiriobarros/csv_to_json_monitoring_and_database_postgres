import time
import pandas as pd
import json
import os
import chardet
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

dados_ficticios = "dados_ficticios.csv"

class CSVtoJSONHandler(FileSystemEventHandler):
    def __init__(self):
        self.last_processed_time = 0  # Track the last processed time to avoid duplicate processing

    def on_modified(self, event):
        if event.is_directory:
            return

        # Verifica se o arquivo modificado é o "dados_ficticios.csv"
        if os.path.basename(event.src_path) == dados_ficticios:
            current_time = time.time()
            file_modified_time = os.path.getmtime(event.src_path)
            
            # Verifica se o arquivo foi modificado e se passou tempo suficiente desde a última verificação
            if file_modified_time > self.last_processed_time + 2:
                self.last_processed_time = file_modified_time
                time.sleep(1)  # Permite que o arquivo seja totalmente gravado
                self.convert_csv_to_json()

    def convert_csv_to_json(self):
        try:
            # Detecta a codificação do arquivo para evitar problemas
            with open("dados_ficticios.csv", "rb") as f:
                result = chardet.detect(f.read())
                encoding_detected = result["encoding"] if result["encoding"] else "utf-8"

            # Lê o arquivo CSV com a codificação detectada
            df = pd.read_csv("dados_ficticios.csv", encoding=encoding_detected, sep=";")

            # Remover colunas "Unnamed"
            df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

            # Converte o DataFrame para JSON
            json_data = df.to_json(orient="records", force_ascii=False, indent=4)

            # Escreve o arquivo JSON
            with open("dados_ficticios.json", "w", encoding="utf-8", errors='ignore') as json_file:
                json_file.write(json_data)

            print("Arquivo JSON atualizado!")
        except pd.errors.EmptyDataError:
            print("Erro: O arquivo CSV está vazio.")
        except pd.errors.ParserError:
            print("Erro: O arquivo CSV está mal formatado.")
        except FileNotFoundError:
            print("Erro: O arquivo CSV não foi encontrado.")
        except PermissionError:
            print("Erro: Permissão negada para acessar o arquivo CSV.")
        except Exception as e:
            print(f"Erro ao converter CSV para JSON: {e}")


if __name__ == "__main__":
    path = "."  # Monitorar o diretório atual
    event_handler = CSVtoJSONHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)

    print("Monitorando alterações no arquivo 'dados_ficticios.csv'...")
    observer.start()

    try:
        while True:
            time.sleep(5)  # Manter o script em execução
    except KeyboardInterrupt:
        observer.stop()
        print("Monitoramento interrompido pelo usuário.")
    observer.join()
