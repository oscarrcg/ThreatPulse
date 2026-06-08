🌐 [English](#english) | [Español](#español)

---

<a name="english"></a>

# 🛡️ ThreatPulse - Automated Threat Detector

A log analysis tool that identifies malicious IPs through suspicious behavior detection and reputation lookup via AbuseIPDB.

## 🎯 What does it do?

Analyzes web server logs (Apache/Nginx) to:
- Detect IPs with abnormal request volume (>50)
- Identify scans of sensitive paths (wp-admin, .env, phpmyadmin, etc.)
- Query the AbuseIPDB API to obtain an Abuse Confidence Score (0-100)
- Generate a prioritized report by threat level

## 🛠️ Technologies

- **Python 3.13** - Core language
- **Requests** - REST API consumption
- **Regex** - Custom log parsing
- **Collections.Counter** - Statistical analysis
- **AbuseIPDB API** - External threat intelligence

## ✨ Key Features

| Feature | Description |
|---------|-------------|
| 🔍 Heuristic detection | Request threshold + known attack patterns |
| 🌐 External intelligence | AbuseIPDB integration for IP reputation |
| 📊 Prioritized reports | Sorted by Abuse Score (highest risk first) |
| 🧪 Built-in API test | Verifies API with known malicious IPs |
| 📁 Portable output | Generates `informe_amenazas.txt` ready for review. Also generates `informe_amenazas.html` with a color-coded table (green = low risk, red = high risk) for visual presentation. |

## 📈 Example Output

Running the detector on an `access.log` with 88,543 lines:

```
Reading log file...
Total lines read: 88543
Unique IPs found: 198

Analyzing suspicious behavior...
IPs with more than 50 requests: 1
IPs that visited suspicious paths: 6
Total suspicious IPs to investigate: 7

Querying AbuseIPDB...
Query complete.

--- ABUSEIPDB API TEST ---
  45.155.205.233: Abuse Score = 0% (no recent data)
  185.220.101.42: Abuse Score = 100% ✓ (API working)
  23.129.64.210: Abuse Score = 71% ✓ (API working)
--- END TEST ---

Top 5 most dangerous IPs:
------------------------------------------------------------
  84.239.25.147  - Requests:     1 - Abuse Score:  7%
  118.160.139.79 - Requests: 88138 - Abuse Score:  0%
  103.84.87.66   - Requests:    17 - Abuse Score:  0%
  119.45.171.165 - Requests:     2 - Abuse Score:  0%
  167.71.222.167 - Requests:     4 - Abuse Score:  0%

Project complete!
```

### 🔍 Interpreting Results

- **118.160.139.79** → 88,138 requests (99.5% of traffic) but Abuse Score 0%. Possible new attacker or unreported bot. Early detection here is key.
- **185.220.101.42** (100%) and **23.129.64.210** (71%) → Confirmed malicious IPs, validating that the API is working correctly.
- **7 suspicious IPs** identified out of 198 unique (3.5% anomalous traffic).

## 🚀 Installation & Usage

### 1. Clone the repository
```bash
git clone https://github.com/oscarrcg/ThreatPulse.git
cd ThreatPulse
```

### 2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate    # Linux/Mac
# venv\Scripts\activate     # Windows
```

### 3. Install dependencies
```bash
pip install requests jinja2
```

### 4. Configure your API key
Create a `config.py` file (do NOT push it to GitHub):
```python
# config.py
ABUSEIPDB_KEY = "your_real_api_key_here"
```

> ⚠️ **Important**: Get a free API key at [AbuseIPDB](https://www.abuseipdb.com/register)

### 5. Prepare your log
Place your `access.log` file in the same directory (standard Apache/Nginx format)

### 6. Run the detector
```bash
python detector.py
```

## 📊 Customization

You can adjust these parameters in `detector.py`:

```python
UMBRAL_PETICIONES = 50  # IP is suspicious if it exceeds this number of requests
maxAgeInDays = 365      # Days to look back in AbuseIPDB
```

## 🗺️ Upcoming Features

- [ ] Web dashboard with Flask and interactive charts
- [ ] Automatic blocking via Windows Firewall
- [ ] Email alerts for IPs with score > 75%
- [ ] Real-time log support (watchdog)
- [ ] VirusTotal API integration

## 📁 Project Structure

```
ThreatPulse/
├── detector.py              # Main script
├── test_api.py              # Standalone API test
├── config.py                # Configuration (NOT included in repo)
├── template.html            # Jinja2 template for HTML report
├── requirements.txt         # Dependencies
├── access.log               # Logs to analyze (you must add this)
├── informe_amenazas.txt     # Generated text report (auto-created)
├── informe_amenazas.html    # Generated visual report (auto-created)
├── .gitignore               # Excludes config.py from repository
└── README.md                # This file
```

## 🧪 Quick API Test

Run `test_api.py` to verify your key works:

```bash
python test_api.py
# You should see "Status code: 200" and JSON data
```

## 📄 License

MIT License - Free to use, modify, and distribute.

## 🤝 Contributing

Contributions are welcome. For major changes, please open an issue first to discuss them.

## 📬 Contact

Oscar Carrillo - [GitHub](https://github.com/oscarrcg)

---

⭐ Don't forget to leave a star if you find it useful!

---
---

<a name="español"></a>

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

## ✨ Características Clave

| Característica | Descripción |
|----------------|-------------|
| 🔍 Detección heurística | Umbral de peticiones + patrones de ataque conocidos |
| 🌐 Inteligencia externa | Integración con AbuseIPDB para reputación de IPs |
| 📊 Informes priorizados | Ordenamiento por Abuse Score (mayor riesgo primero) |
| 🧪 Prueba integrada | Verifica API con IPs maliciosas conocidas |
| 📁 Salida portable | Genera `informe_amenazas.txt` listo para revisión. También se genera `informe_amenazas.html` con tabla coloreada (verde = bajo riesgo, rojo = alto riesgo) para presentar resultados de forma visual. |

## 📈 Ejemplo de Salida

Ejecutando el detector en un `access.log` con 88,543 líneas:

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
  84.239.25.147  - Peticiones:     1 - Abuse Score:  7%
  118.160.139.79 - Peticiones: 88138 - Abuse Score:  0%
  103.84.87.66   - Peticiones:    17 - Abuse Score:  0%
  119.45.171.165 - Peticiones:     2 - Abuse Score:  0%
  167.71.222.167 - Peticiones:     4 - Abuse Score:  0%

¡Proyecto completado!
```

### 🔍 Interpretación de Resultados

- **118.160.139.79** → 88,138 peticiones (99.5% del tráfico) pero Abuse Score 0%. Posible nuevo atacante o bot no reportado. La detección temprana aquí es clave.
- **185.220.101.42** (100%) y **23.129.64.210** (71%) → IPs maliciosas confirmadas, validan que la API funciona correctamente.
- **7 IPs sospechosas** identificadas de 198 únicas (3.5% del tráfico anómalo).

## 🚀 Instalación y Uso

### 1. Clona el repositorio
```bash
git clone https://github.com/oscarrcg/ThreatPulse.git
cd ThreatPulse
```

### 2. Crea entorno virtual
```bash
python -m venv venv
source venv/bin/activate    # Linux/Mac
# venv\Scripts\activate     # Windows
```

### 3. Instala dependencias
```bash
pip install requests jinja2
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

## 🗺️ Próximas Mejoras

- [ ] Dashboard web con Flask y gráficos interactivos
- [ ] Bloqueo automático con firewall de Windows
- [ ] Alertas por email para IPs con score > 75%
- [ ] Soporte para logs en tiempo real (watchdog)
- [ ] Integración con VirusTotal API

## 📁 Estructura del Proyecto

```
ThreatPulse/
├── detector.py              # Script principal
├── test_api.py              # Prueba de API independiente
├── config.py                # Configuración (NO incluido en repo)
├── template.html            # Plantilla Jinja2 para informe HTML
├── requirements.txt         # Dependencias
├── access.log               # Logs a analizar (debes agregarlo)
├── informe_amenazas.txt     # Informe texto generado (autocreado)
├── informe_amenazas.html    # Informe visual generado (autocreado)
├── .gitignore               # Excluye config.py del repositorio
└── README.md                # Este archivo
```

## 🧪 Prueba Rápida de API

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