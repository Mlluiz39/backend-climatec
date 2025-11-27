import schedule
import time
from weather_client import WeatherClient
from queue_publisher import QueuePublisher
from config import Config
from sp_locations import SP_LOCATIONS, get_total_locations

class WeatherScheduler:
    def __init__(self):
        self.weather_client = WeatherClient()
        self.queue_publisher = QueuePublisher()
        self.config = Config()
    
    def collect_and_publish_single(self, latitude: float, longitude: float, city_name: str = None):
        """
        Coleta e publica dados para uma única localização
        
        Args:
            latitude: Latitude da localização
            longitude: Longitude da localização
            city_name: Nome da cidade (opcional)
        """
        location_label = city_name or f"{latitude},{longitude}"
        print(f"  📍 Coletando dados de {location_label}...")
        
        weather_data = self.weather_client.fetch_weather_data(latitude, longitude, city_name)
        if weather_data:
            success = self.queue_publisher.publish(weather_data)
            if success:
                print(f"  ✅ {location_label}: Dados publicados")
            else:
                print(f"  ⚠️ {location_label}: Falha ao publicar")
        else:
            print(f"  ⚠️ {location_label}: Falha ao coletar dados")
        
        return weather_data is not None
    
    def collect_and_publish_multi(self):
        """
        Coleta dados de todas as cidades configuradas em SP_LOCATIONS
        """
        print(f"\n🌎 Coletando dados de {get_total_locations()} cidades de São Paulo...")
        
        successful = 0
        failed = 0
        
        for location in SP_LOCATIONS:
            city = location["city"]
            lat = location["latitude"]
            lon = location["longitude"]
            
            if self.collect_and_publish_single(lat, lon, city):
                successful += 1
            else:
                failed += 1
            
            # Delay de 2 segundos entre cada requisição para evitar rate limiting
            time.sleep(2)
        
        print(f"\n📊 Resumo: {successful} sucessos, {failed} falhas")
    
    def collect_and_publish(self):
        """
        Método principal que decide entre single ou multi-location
        """
        if self.config.ENABLE_MULTI_LOCATION:
            self.collect_and_publish_multi()
        else:
            # Modo single-location (compatibilidade com versão antiga)
            print(f"\n🌤️  Coletando dados (modo single-location)...")
            self.collect_and_publish_single(
                float(self.config.SINGLE_LATITUDE),
                float(self.config.SINGLE_LONGITUDE)
            )
    
    def run(self):
        print("🔵 Iniciando o scheduler (Producer Mode)...")
        
        if self.config.ENABLE_MULTI_LOCATION:
            print(f"🚀 Multi-Location Mode: {get_total_locations()} cidades de São Paulo")
            print(f"⏰ Intervalo: {self.config.COLLECTION_INTERVAL_MINUTES} minutos")
        else:
            print(f"🚀 Single-Location Mode: {self.config.SINGLE_LATITUDE},{self.config.SINGLE_LONGITUDE}")
            print(f"⏰ Intervalo: {self.config.COLLECTION_INTERVAL_MINUTES} minutos")
        
        # Coleta inicial
        self.collect_and_publish()
        
        # Agendamento
        schedule.every(self.config.COLLECTION_INTERVAL_MINUTES).minutes.do(self.collect_and_publish)
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(1)
        except KeyboardInterrupt:
            print("⏹️ Shutting down...")
            self.queue_publisher.close()

if __name__ == "__main__":
    scheduler = WeatherScheduler()
    scheduler.run()

