# Multi-Location Weather Collection - Documentação

## 📍 Visão Geral

O sistema foi expandido para coletar dados meteorológicos de **15 cidades** distribuídas pelo Estado de São Paulo, ao invés de apenas uma localização fixa.

## 🗺️ Cidades Cobertas

### Região Metropolitana de São Paulo
- São Paulo (-23.5505, -46.6333)
- Guarulhos (-23.4538, -46.5333)

### Região Metropolitana de Campinas
- Campinas (-22.9099, -47.0626)
- Jundiaí (-23.1864, -46.8842)

### Litoral
- Santos (-23.9608, -46.3336)

### Vale do Paraíba
- São José dos Campos (-23.1790, -45.8869)

### Interior - Região Central
- Ribeirão Preto (-21.1704, -47.8103)
- Araraquara (-21.7947, -48.1758)
- Piracicaba (-22.7253, -47.6491)

### Interior - Região Oeste
- Sorocaba (-23.5015, -47.4526)
- Bauru (-22.3147, -49.0608)
- Marília (-22.2139, -49.9458)
- Presidente Prudente (-22.1256, -51.3888)

### Interior - Região Norte
- São José do Rio Preto (-20.8197, -49.3794)
- Franca (-20.5386, -47.4008)

## ⚙️ Configuração

### Modo Multi-Localização (Padrão)

No arquivo `.env`, configure:

```bash
ENABLE_MULTI_LOCATION=true
COLLECTION_INTERVAL_MINUTES=60
```

Isso fará o sistema coletar dados de todas as 15 cidades a cada 60 minutos.

**Tempo estimado de coleta**: ~30 segundos (15 cidades × 2 segundos de delay)

### Modo Single-Localização (Legado)

Para usar apenas uma localização específica:

```bash
ENABLE_MULTI_LOCATION=false
LATITUDE=-23.64683
LONGITUDE=-46.45510
COLLECTION_INTERVAL_MINUTES=60
```

## 🚀 Como Usar

### 1. Atualizar variáveis de ambiente

```bash
# Copie o .env.example se ainda não tiver .env
cp .env.example .env

# Edite o .env e defina ENABLE_MULTI_LOCATION=true
```

### 2. Reiniciar o serviço

```bash
# Parar containers existentes
docker-compose down

# Reconstruir e iniciar
docker-compose up --build -d python-producer

# Ver logs
docker-compose logs -f python-producer
```

### 3. Verificar logs

Você verá logs como:

```
🔵 Iniciando o scheduler (Producer Mode)...
🚀 Multi-Location Mode: 15 cidades de São Paulo
⏰ Intervalo: 60 minutos

🌎 Coletando dados de 15 cidades de São Paulo...
  📍 Coletando dados de São Paulo...
  ✅ São Paulo: Dados publicados
  📍 Coletando dados de Guarulhos...
  ✅ Guarulhos: Dados publicados
  ...
📊 Resumo: 15 sucessos, 0 falhas
```

## 📊 Estrutura dos Dados

Cada coleta agora inclui:

```json
{
  "timestamp": "2025-11-27T22:30:00Z",
  "location": {
    "latitude": -23.5505,
    "longitude": -46.6333,
    "city": "São Paulo",
    "state": "São Paulo",
    "country": "Brazil"
  },
  "data": {
    "temperature": 24.5,
    "humidity": 65,
    "wind_speed": 12.3,
    "weather_code": 0,
    "weather_condition": "Clear sky",
    "precipitation_probability": 10
  },
  "source": "open-meteo",
  "version": "1.0"
}
```

## 🔍 Consultas no Frontend

### Opção 1: Buscar dados próximos à localização do usuário

```typescript
// Frontend obtém geolocalização do usuário
navigator.geolocation.getCurrentPosition(async (position) => {
  const { latitude, longitude } = position.coords;
  
  // Busca dados próximos no backend
  const response = await fetch(
    `/api/weather/by-location?latitude=${latitude}&longitude=${longitude}&radius=50`
  );
  
  const nearbyWeather = await response.json();
});
```

### Opção 2: Buscar dados de uma cidade específica

```typescript
// Buscar dados de Campinas
const response = await fetch('/api/weather/filter?city=Campinas');
const campinasWeather = await response.json();
```

## 📈 Impacto

### Vantagens
- ✅ Cobertura de todo o estado de SP
- ✅ Usuários veem dados mais próximos de sua localização
- ✅ Dados mais relevantes regionalmente
- ✅ Melhor análise de tendências climáticas

### Considerações
- ⚠️ Volume de dados: 15x maior (15 cidades)
- ⚠️ Tempo de coleta: ~30 segundos a cada ciclo
- ⚠️ Armazenamento: cresce proporcionalmente

## 🛠️ Manutenção

### Adicionar novas cidades

Edite `python_producer/sp_locations.py`:

```python
SP_LOCATIONS = [
    # ... cidades existentes ...
    {"city": "Nova Cidade", "latitude": -XX.XXXX, "longitude": -XX.XXXX},
]
```

### Ajustar delay entre requisições

Edite `python_producer/scheduler.py`, linha do `time.sleep(2)`:

```python
# Aumentar para 5 segundos
time.sleep(5)
```

## 🧪 Testes Manuais

### Verificar coleta

```bash
# Ver logs em tempo real
docker-compose logs -f python-producer

# Verificar RabbitMQ
# Acesse: http://localhost:15672
# Login: admin / admin (ou conforme seu .env)
```

### Verificar MongoDB

```bash
# Conectar ao container MongoDB
docker exec -it mongo mongosh

# Ver dados recentes
use climate-sync
db.weathers.find().sort({createdAt: -1}).limit(5).pretty()

# Contar dados por cidade
db.weathers.aggregate([
  { $group: { _id: "$location.city", count: { $sum: 1 } } },
  { $sort: { count: -1 } }
])
```

## 📝 Arquivos Modificados

- ✅ `python_producer/sp_locations.py` (NOVO)
- ✅ `python_producer/config.py`
- ✅ `python_producer/weather_client.py`
- ✅ `python_producer/scheduler.py`
- ✅ `.env.example`
- ✅ `docker-compose.yml`

## 🔄 Rollback

Para voltar ao modo antigo:

```bash
# No .env
ENABLE_MULTI_LOCATION=false

# Reiniciar
docker-compose restart python-producer
```
