import os

class Config:
    # Open-Meteo API
    WEATHER_API_URL = "https://api.open-meteo.com/v1/forecast"
    
    # Multi-location support
    # Set ENABLE_MULTI_LOCATION=true to collect from multiple cities in SP state
    # Set ENABLE_MULTI_LOCATION=false to use single location (LATITUDE/LONGITUDE below)
    ENABLE_MULTI_LOCATION = os.getenv("ENABLE_MULTI_LOCATION", "true").lower() == "true"
    
    # Single location configuration (used when ENABLE_MULTI_LOCATION=false)
    SINGLE_LATITUDE = os.getenv("LATITUDE", "-23.65221")
    SINGLE_LONGITUDE = os.getenv("LONGITUDE", "-46.45428")
    
    # RabbitMQ
    RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "rabbitmq")
    RABBITMQ_PORT = int(os.getenv("RABBITMQ_PORT", "5672"))
    RABBITMQ_USER = os.getenv("RABBITMQ_USER", "admin")
    RABBITMQ_PASS = os.getenv("RABBITMQ_PASS", "admin")
    RABBITMQ_QUEUE = os.getenv("RABBITMQ_QUEUE", "weather.data")
    RABBITMQ_VHOST = os.getenv("RABBITMQ_VHOST", "/")
    
    # Schedule
    COLLECTION_INTERVAL_MINUTES = int(os.getenv("COLLECTION_INTERVAL_MINUTES", "60"))
    
    # Logs
    LOG_PATH = "/logs/producer.log"
