# Exemplo de consumo de API externa para obter dados de localização usando requests.
import sys
import requests

# acessa a api e extrai dados de localização
def local(city: str) -> tuple[str, str, str]:
    url_base = "https://geocoding-api.open-meteo.com/v1/search"
    params = {
        'name': city,
        'count': 1
    }

    lat = lon = loc = None
    try:
        response = requests.get(url_base, params=params)
        if response.status_code == 200:
            data = response.json()
            if 'results' in data and data['results']:
                result = data['results'][0]
                lat = result['latitude']
                lon = result['longitude']
                loc = result['country']
                city = result['name']
            else:
                print("City not found.")
        else:
            print(f"Error: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

    return (lat, lon, loc, city)


# usa os dados de localização e recupera a temperatura
def temp(lat:str, lon:str):
    url_base = "https://api.open-meteo.com/v1/forecast"
    params = {
        'latitude': lat,
        'longitude': lon,
        'current': 'temperature_2m'
    }

    try:
        response = requests.get(url_base, params=params)
        if response.status_code == 200:
            data = response.json()
            res = data['current']['temperature_2m']
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

    return res

if __name__ == "__main__":
    if len(sys.argv) > 1:
        input_city = " ".join(sys.argv[1:])
        lat, lon, loc, city = local(input_city)
        if lat and lon and loc and city:
            temperatura = temp(lat, lon)
            print(f"Current temperature in {city}, {loc} is {temperatura}°C")
        else:
            print("Could not retrieve location data.")
    else:
        print("Usage: an argument is required.")

