# ThreatPulse - Detector Automatizado de Amenazas

## ¿Qué hace?
Analiza logs de Apache/Nginx, detecta comportamiento sospechoso y consulta AbuseIPDB para obtener reputación de IPs.

## Tecnologías
- Python 3.13
- Requests (API integration)
- Regex para parsing de logs
- Análisis estadístico con Counter

## Características clave
- ✅ Detección por volumen (>50 peticiones)
- ✅ Detección por patrones de ataque (wp-admin, .env, phpmyadmin)
- ✅ Integración con AbuseIPDB API
- ✅ Generación de informes priorizados

## Ejemplo de salida
[Pon aquí la salida de tu detector.py]

## Próximas mejoras
- [ ] Bloqueo automático con firewall de Windows
- [ ] Dashboard web con Flask
- [ ] Alertas por email para scores > 75%