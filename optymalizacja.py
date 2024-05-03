import requests
from datetime import datetime, timedelta


class WeatherForecast:
    def __init__(self):
        self.data = {}

    def __setitem__(self, date, result):
        self.data[date] = result

    def __getitem__(self, date):
        return self.data.get(date)

    def __iter__(self):
        return iter(self.data)

    def items(self):
        return self.data.items()

    def check_rainfall(self, date):
        latitude = "54.3520"
        longitude = "18.6466"
        api_url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=rain&daily=rain_sum&timezone=Europe%2FWarsaw&start_date={date}&end_date={date}"

        try:
            response = requests.get(api_url)
            print("Status code:", response.status_code)

            if response.status_code == 200:
                data = response.json()
                print("Response data:", data)

                if 'hourly' in data and 'rain' in data['hourly']:
                    hourly_rain = data['hourly']['rain']

                    # Sprawdź, czy występują opady deszczu w danych godzinowych
                    if any(rainfall > 0.0 for rainfall in hourly_rain):
                        result = "Będzie padać"
                    else:
                        result = "Nie będzie padać"
                else:
                    print(
                        "Nie znaleziono danych godzinowych o opadach deszczu.")
                    result = "Nie wiem"
            else:
                print("Wystąpił problem z zapytaniem do serwera. Status:",
                      response.status_code)
                result = "Nie wiem"

        except requests.exceptions.RequestException as e:
            print("Nie udało się pobrać danych z API:", e)
            result = "Nie wiem"

        self[date] = result
        return result


def main():
    weather_forecast = WeatherForecast()

    date_input = input(
        "Podaj datę w formacie YYYY-mm-dd (jeśli puste, użyję następnego dnia): ")
    if not date_input:
        date = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
    else:
        date = date_input

    result = weather_forecast[date]
    if result:
        print("Wynik z pliku:", result)
    else:
        result = weather_forecast.check_rainfall(date)
        print("Wynik zapytania:", result)

    # Zapisz wynik do pliku
    weather_forecast[date] = result
    print("Zapisano wynik do pliku.")


if __name__ == "__main__":
    main()
