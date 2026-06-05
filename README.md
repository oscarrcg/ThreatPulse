# 🛡️ ThreatPulse - Detector Automatizado de Amenazas

Herramienta de análisis de logs que identifica IPs maliciosas mediante detección de comportamientos sospechosos y consulta su reputación en AbuseIPDB.

## 🎯 ¿Qué hace?

Analiza logs de servidores web (Apache/Nginx) para:
- Detectar IPs con volumen anormal de peticiones (>50)
- Identificar escaneos de rutas sensibles (wp-admin, .env, phpmyadmin, etc.)
- Consultar AbuseIPDB API para obtener Abuse Confidence Score (0-100)
- Generar informe priorizado por nivel de amenaza

## 🛠️ Tecnologías

- **Python 3.13** - Lenguaje principal
- **Requests** - Consumo de API REST
- **Regex** - Parsing de logs personalizado
- **Collections.Counter** - Análisis estadístico
- **AbuseIPDB API** - Inteligencia de amenazas externa

## ✨ Características clave

| Característica | Descripción |
|----------------|-------------|
| 🔍 Detección heurística | Umbral de peticiones + patrones de ataque conocidos |
| 🌐 Inteligencia externa | Integración con AbuseIPDB para reputación de IPs |
| 📊 Informes priorizados | Ordenamiento por Abuse Score (mayor riesgo primero) |
| 🧪 Prueba integrada | Verifica API con IPs maliciosas conocidas |
| 📁 Salida portable | Genera informe_amenazas.txt listo para revisión |

## 📈 Ejemplo de salida

Ejecutando el detector en un access.log con 88,543 líneas:

```
Leyendo archivo de logs...
Total de líneas leídas: 88543
IPs únicas encontradas: 198

Analizando comportamiento sospechoso...
IPs con más de 50 peticiones: 1
IPs que visitaron rutas sospechosas: 6
Total IPs sospechosas a investigar: 7

Consultando AbuseIPDB...
Consulta completada.

--- PRUEBA DE API ABUSEIPDB ---
  45.155.205.233: Abuse Score = 0% (sin datos recientes)
  185.220.101.42: Abuse Score = 100% ✓ (API funciona)
  23.129.64.210: Abuse Score = 71% ✓ (API funciona)
--- FIN PRUEBA ---

Top 5 IPs más peligrosas:
------------------------------------------------------------
  84.239.25.147 - Peticiones: 1 - Abuse Score: 7%
  118.160.139.79 - Peticiones: 88138 - Abuse Score: 0%
  103.84.87.66 - Peticiones: 17 - Abuse Score: 0%
  119.45.171.165 - Peticiones: 2 - Abuse Score: 0%
  167.71.222.167 - Peticiones: 4 - Abuse Score: 0%

¡Proyecto completado!
```

### 🔍 Interpretación de resultados

- **118.160.139.79** → 88,138 peticiones (99.5% del tráfico) pero Abuse Score 0%. Posible nuevo atacante o bot no reportado. La detección temprana aquí es clave.
- **185.220.101.42** (100%) y **23.129.64.210** (71%) → IPs maliciosas confirmadas, validan que la API funciona correctamente.
- **7 IPs sospechosas** identificadas de 198 únicas (3.5% del tráfico anómalo).

## 🚀 Instalación y uso

### 1. Clona el repositorio
```bash
git clone https://github.com/oscarrcg/ThreatPulse.git
cd ThreatPulse
```

### 2. Crea entorno virtual
```bash
python -m venv venv
venv\Scripts\activate  # En Windows
# source venv/bin/activate  # En Linux/Mac
```

### 3. Instala dependencias
```bash
pip install requests
```

### 4. Configura tu API key
Crea un archivo `config.py` (NO lo subas a GitHub):
```python
# config.py
ABUSEIPDB_KEY = "tu_api_key_real_aqui"
```

> ⚠️ **Importante**: Obtén una API key gratis en [AbuseIPDB](https://www.abuseipdb.com/register)

### 5. Prepara tu log
Coloca tu archivo `access.log` en el mismo directorio (formato Apache/Nginx estándar)

### 6. Ejecuta el detector
```bash
python detector.py
```

## 📊 Personalización

Puedes ajustar estos parámetros en `detector.py`:

```python
UMBRAL_PETICIONES = 50  # IP sospechosa si supera este número
maxAgeInDays = 365       # Días hacia atrás en AbuseIPDB
```

## 🗺️ Próximas mejoras

- [ ] Dashboard web con Flask y gráficos interactivos
- [ ] Bloqueo automático con firewall de Windows
- [ ] Alertas por email para IPs con score > 75%
- [ ] Soporte para logs en tiempo real (watchdog)
- [ ] Integración con VirusTotal API

## 📁 Estructura del proyecto

```
ThreatPulse/
├── detector.py          # Script principal
├── test_api.py          # Prueba de API independiente
├── config.py            # Configuración (NO incluido en repo)
├── requirements.txt     # Dependencias
├── access.log           # Logs a analizar (debes agregarlo)
├── informe_amenazas.txt # Informe generado (autocreado)
└── README.md            # Este archivo
```

## 🧪 Prueba rápida de API

Ejecuta `test_api.py` para verificar que tu clave funciona:

```bash
python test_api.py
# Deberías ver "Status code: 200" y datos JSON
```

## 📄 Licencia

MIT License - Libre de usar, modificar y distribuir.

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Para cambios mayores, abre un issue primero para discutirlo.

## 📬 Contacto

Oscar Carrillo - [GitHub](https://github.com/oscarrcg)

---

⭐ ¡No olvides darle una estrella si te es útil!