import requests
import matplotlib.pyplot as plt
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("WEATHER_API_KEY")

def get_weather(city):
    # Получение текущей погоды
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric&lang=ru"
    response = requests.get(url).json()
    
    if response.get("cod") != 200:
        return None
    
    return {
        "temp": response["main"]["temp"],
        "desc": response["weather"][0]["description"],
        "city": response["name"]
    }

def get_forecast_graph(city):
    # Получение прогноза на 5 дней для графика
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric&lang=ru"
    response = requests.get(url).json()
    
    if response.get("cod") != "200":
        return None

    # Обработка данных через Pandas
    data = []
    for item in response["list"][:8]:  # Берем ближайшие 24 часа (8 интервалов по 3 часа)
        data.append({
            "time": item["dt_txt"][11:16],
            "temp": item["main"]["temp"]
        })
    
    df = pd.DataFrame(data)
    
    # Построение графика
    plt.figure(figsize=(10, 5))
    plt.plot(df["time"], df["temp"], marker='o', color='b')
    plt.title(f"Прогноз температуры в {city}")
    plt.xlabel("Время")
    plt.ylabel("Градусы Celsius")
    plt.grid(True)
    
    graph_path = "weather_plot.png"
    plt.savefig(graph_path)
    plt.close()
    return graph_path
