# projeto_clima.py
import requests
import pandas as pd
import sqlite3
from datetime import datetime

API_KEY = "78f7a5cd38c00a922d0ed9527bbeec35"  # coloque sua chave aqui
CITY = "Sao Paulo"

def coletar_dados():
    url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric&lang=pt_br"
    r = requests.get(url).json()
    dados = {
        "cidade": CITY,
        "temperatura": r["main"]["temp"],
        "umidade": r["main"]["humidity"],
        "descricao": r["weather"][0]["description"].title(),
        "data_coleta": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    return pd.DataFrame([dados])

def salvar_dados(df):
    conn = sqlite3.connect("clima.db")
    df.to_sql("clima", conn, if_exists="append", index=False)
    conn.close()

def mostrar_dados():
    conn = sqlite3.connect("clima.db")
    df = pd.read_sql("SELECT * FROM clima ORDER BY data_coleta DESC", conn)
    conn.close()
    print(df.head())

if __name__ == "__main__":
    df = coletar_dados()
    salvar_dados(df)
    mostrar_dados()
    print("✅ Dados coletados e salvos com sucesso!")
