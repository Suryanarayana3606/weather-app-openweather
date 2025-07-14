from flask import Flask, render_template, request
import requests
from datetime import datetime

app = Flask(__name__)
API_KEY = 'Your_API_KEY'

@app.route('/', methods=['GET', 'POST'])
def index():
    current_weather = None
    next_hours = []

    if request.method == 'POST':
        city = request.form['city'].strip()

        # --- Current Weather ---
        weather_url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric'
        weather_response = requests.get(weather_url)

        if weather_response.status_code == 200:
            data = weather_response.json()
            current_weather = {
                'city': data['name'],
                'temperature': data['main']['temp'],
                'description': data['weather'][0]['description'],
                'icon': data['weather'][0]['icon']
            }

            # --- Next 12 Hours Forecast ---
            forecast_url = f'https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric'
            forecast_response = requests.get(forecast_url)

            if forecast_response.status_code == 200:
                forecast_data = forecast_response.json()['list'][:4]  # first 4 entries (3hr interval)

                for entry in forecast_data:
                    dt_txt = entry['dt_txt']
                    time_str = datetime.strptime(dt_txt, '%Y-%m-%d %H:%M:%S').strftime('%I:%M %p')
                    next_hours.append({
                        'time': time_str,
                        'temp': entry['main']['temp'],
                        'desc': entry['weather'][0]['description'],
                        'icon': entry['weather'][0]['icon']
                    })

        else:
            current_weather = {'error': 'City not found!'}

    return render_template('index.html', weather=current_weather, next_hours=next_hours)

if __name__ == "__main__":
    app.run(debug=True)
