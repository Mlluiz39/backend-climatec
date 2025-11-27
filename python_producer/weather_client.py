import requests
from datetime import datetime
from typing import Dict, Optional
from config import Config


class WeatherClient:
    def __init__(self):
        self.api_url = Config.WEATHER_API_URL

    def fetch_weather_data(self, latitude: float, longitude: float, city_name: str = None) -> Optional[Dict]:
        """
        Busca dados climáticos da API Open-Meteo para coordenadas específicas
        
        Args:
            latitude: Latitude da localização
            longitude: Longitude da localização
            city_name: Nome da cidade (opcional, usado para override no normalize)
        """
        try:
            params = {
                "latitude": latitude,
                "longitude": longitude,
                "current": "temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code",
                "hourly": "precipitation_probability",
                "timezone": "America/Sao_Paulo"
            }
            
            response = requests.get(self.api_url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            return self._normalize_data(data, latitude, longitude, city_name)
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Error fetching weather data for {city_name or f'{latitude},{longitude}'}: {e}")
            return None

    def _normalize_data(self, raw_data: Dict, latitude: float, longitude: float, city_name: str = None) -> Dict:
        """
        Normaliza dados da API para formato padrão, incluindo lookup de cidade/estado/país
        
        Args:
            raw_data: Dados brutos da API
            latitude: Latitude da localização
            longitude: Longitude da localização
            city_name: Nome da cidade (opcional, sobrescreve o lookup)
        """
        current = raw_data.get("current", {})
        hourly = raw_data.get("hourly", {})
        
        # Probabilidade de precipitação da próxima hora
        precipitation_prob = 0
        if hourly.get("precipitation_probability"):
            precipitation_prob = hourly["precipitation_probability"][0]
        
        # Geocoding reverso para obter cidade, estado e país
        # Se city_name foi fornecido, usa ele. Caso contrário, faz lookup
        if city_name:
            location_info = {
                "city": city_name,
                "state": "São Paulo",
                "country": "Brazil"
            }
        else:
            location_info = self._get_location_info(latitude, longitude)
        
        normalized = {
            "timestamp": datetime.utcnow().isoformat(),
            "location": {
                "latitude": float(latitude),
                "longitude": float(longitude),
                "city": location_info.get("city", "Unknown"),
                "state": location_info.get("state", "Unknown"),
                "country": location_info.get("country", "Unknown")
            },
            "data": {
                "temperature": current.get("temperature_2m"),
                "humidity": current.get("relative_humidity_2m"),
                "wind_speed": current.get("wind_speed_10m"),
                "weather_code": current.get("weather_code"),
                "weather_condition": self._get_weather_condition(current.get("weather_code", 0)),
                "precipitation_probability": precipitation_prob
            },
            "source": "open-meteo",
            "version": "1.0"
        }
        
        return normalized

    def _get_location_info(self, latitude: float, longitude: float) -> Dict[str, str]:
        """
        Retorna cidade, estado e país via geocoding reverso usando Nominatim API
        
        Args:
            latitude: Latitude da localização
            longitude: Longitude da localização
        """
        try:
            url = "https://nominatim.openstreetmap.org/reverse"
            params = {
                "lat": latitude,
                "lon": longitude,
                "format": "json",
                "accept-language": "pt"
            }
            headers = {
                "User-Agent": "weather-app/1.0"
            }
            
            response = requests.get(url, params=params, headers=headers, timeout=5)
            response.raise_for_status()
            
            data = response.json()
            address = data.get("address", {})
            
            return {
                "city": address.get("city") or address.get("town") or address.get("village") or address.get("municipality"),
                "state": address.get("state"),
                "country": address.get("country")
            }
        except Exception as e:
            print(f"❌ Error fetching location info for {latitude},{longitude}: {e}")
            return {}

    def _get_weather_condition(self, code: int) -> str:
        """
        Converte código WMO para descrição textual
        https://open-meteo.com/en/docs
        """
        conditions = {
            0: "Clear sky",
            1: "Mainly clear",
            2: "Partly cloudy",
            3: "Overcast",
            45: "Foggy",
            48: "Depositing rime fog",
            51: "Light drizzle",
            53: "Moderate drizzle",
            55: "Dense drizzle",
            61: "Slight rain",
            63: "Moderate rain",
            65: "Heavy rain",
            71: "Slight snow",
            73: "Moderate snow",
            75: "Heavy snow",
            77: "Snow grains",
            80: "Slight rain showers",
            81: "Moderate rain showers",
            82: "Violent rain showers",
            85: "Slight snow showers",
            86: "Heavy snow showers",
            95: "Thunderstorm",
            96: "Thunderstorm with slight hail",
            99: "Thunderstorm with heavy hail"
        }
        return conditions.get(code, "Unknown")