import requests
import configparser
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def weather_dashboard():
    return render_template('home.html')


@app.route('/results', methods=['POST'])
def render_results():
    name = request.form['name']

    api_key = get_api_key()
    data = get_weather_weather(name, api_key)
    temp = "{0:.2f}".format(data["main"]["temp"])
    feels_like = "{0:.2f}".format(data["main"]["feels_like"])
    weather = data["weather"][0]["main"]
    location = data["name"]
    icon = data['weather'][0]['icon']

    dataforecast = get_weather_forecast(name, api_key)
    forecast = dataforecast['list']

    return render_template('results.html',
                           location=location, temp=temp, feels_like=feels_like, icon=icon, weather=weather, forecast=forecast, api_key=api_key)
def get_api_key():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config['openweathermap']['api']


def get_weather_weather(name, api_key):
    api_url = "http://api.openweathermap.org/" \
              "data/2.5/weather?q={}&units=metric&appid={}".format(name, api_key)
    r = requests.get(api_url)
    return r.json()

def get_weather_forecast(name, api_key):
    api_url = "http://api.openweathermap.org/" \
              "data/2.5/forecast?q={}&units=metric&appid={}".format(name, api_key)
    r = requests.get(api_url)
    return r.json()


if __name__ == '__main__':
    app.run()

