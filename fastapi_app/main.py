import psutil
from dotenv import load_dotenv
from fastapi import FastAPI, Form, Request
from loguru import logger
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Gauge, generate_latest
from starlette.responses import Response

# Charger les variables d'environnement depuis .env
load_dotenv()

# Initialisation de l'application FastAPI
app = FastAPI(title="FastAPI Monitoring App")

# ---------------------------------------------------
# Metrics Prometheus
# ---------------------------------------------------
REQUEST_COUNT = Counter(
    "app_requests_total", "Total requests received", ["method", "endpoint"]
)
CPU_USAGE = Gauge("system_cpu_usage_percent", "System CPU usage in %")
MEMORY_USAGE = Gauge("system_memory_usage_percent", "System memory usage in %")
DISK_USAGE = Gauge("system_disk_usage_percent", "System disk usage in %")

# ---------------------------------------------------
# Logging
# ---------------------------------------------------
logger.add("/logs/fastapi.log", rotation="500 MB")

# ---------------------------------------------------
# Middleware pour compter toutes les requêtes
# ---------------------------------------------------
@app.middleware("http")
async def count_requests(request: Request, call_next):
    REQUEST_COUNT.labels(method=request.method, endpoint=request.url.path).inc()
    response = await call_next(request)
    return response

# ---------------------------------------------------
# Endpoints
# ---------------------------------------------------
@app.get("/")
async def root():
    """
    Endpoint racine pour tester que l'application est UP.
    """
    return {"status": "up"}

@app.get("/health")
async def health_check():
    """
    Endpoint pour vérifier l'état de santé du système.
    Retourne CPU, RAM, et disque.
    Utile pour Uptime Kuma et Docker Healthcheck.
    """
    cpu = psutil.cpu_percent()
    memory = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent

    # Mettre à jour les gauges Prometheus
    CPU_USAGE.set(cpu)
    MEMORY_USAGE.set(memory)
    DISK_USAGE.set(disk)

    health_status = {
        "status": "healthy",
        "cpu_usage": f"{cpu}%",
        "memory_usage": f"{memory}%",
        "disk_usage": f"{disk}%"
    }
    return health_status

@app.post("/predict")
async def predict(data: str = Form(...)):
    """
    Endpoint de prédiction fictif.
    Enregistre la donnée reçue et retourne une prédiction simulée.
    """
    logger.info(f"Donnée reçue : {data}")
    # Ici tu pourrais appeler ton modèle ML
    prediction_value = 450
    return {"prediction": "Valeur prédite", "value": prediction_value}

@app.get("/metrics")
async def metrics():
    """
    Endpoint Prometheus pour exposer toutes les métriques.
    CPU, RAM, disque et compteur de requêtes.
    """
    # Mise à jour des métriques système
    CPU_USAGE.set(psutil.cpu_percent())
    MEMORY_USAGE.set(psutil.virtual_memory().percent)
    DISK_USAGE.set(psutil.disk_usage('/').percent)

    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)