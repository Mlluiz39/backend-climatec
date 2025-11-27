"""
Coordenadas das principais cidades do Estado de São Paulo
Distribuição geográfica para cobrir todas as regiões
"""

SP_LOCATIONS = [
    # Região Metropolitana de São Paulo
    {"city": "São Paulo", "latitude": -23.5505, "longitude": -46.6333},
    {"city": "Guarulhos", "latitude": -23.4538, "longitude": -46.5333},
    
    # Região Metropolitana de Campinas
    {"city": "Campinas", "latitude": -22.9099, "longitude": -47.0626},
    {"city": "Jundiaí", "latitude": -23.1864, "longitude": -46.8842},
    
    # Litoral
    {"city": "Santos", "latitude": -23.9608, "longitude": -46.3336},
    
    # Vale do Paraíba
    {"city": "São José dos Campos", "latitude": -23.1790, "longitude": -45.8869},
    
    # Interior - Região Central
    {"city": "Ribeirão Preto", "latitude": -21.1704, "longitude": -47.8103},
    {"city": "Araraquara", "latitude": -21.7947, "longitude": -48.1758},
    {"city": "Piracicaba", "latitude": -22.7253, "longitude": -47.6491},
    
    # Interior - Região Oeste
    {"city": "Sorocaba", "latitude": -23.5015, "longitude": -47.4526},
    {"city": "Bauru", "latitude": -22.3147, "longitude": -49.0608},
    {"city": "Marília", "latitude": -22.2139, "longitude": -49.9458},
    {"city": "Presidente Prudente", "latitude": -22.1256, "longitude": -51.3888},
    
    # Interior - Região Norte
    {"city": "São José do Rio Preto", "latitude": -20.8197, "longitude": -49.3794},
    {"city": "Franca", "latitude": -20.5386, "longitude": -47.4008},
]


def get_all_locations():
    """Retorna todas as localizações configuradas"""
    return SP_LOCATIONS


def get_location_by_city(city_name: str):
    """Busca uma localização específica pelo nome da cidade"""
    for location in SP_LOCATIONS:
        if location["city"].lower() == city_name.lower():
            return location
    return None


def get_total_locations():
    """Retorna o número total de localizações"""
    return len(SP_LOCATIONS)
