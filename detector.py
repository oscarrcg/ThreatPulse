import re
from collections import Counter
import requests
import config
from datetime import datetime

# Archivo de logs a analizar
LOG_FILE = "access.log"

# Umbral: una IP es sospechosa si aparece más de 50 veces
UMBRAL_PETICIONES = 50

# Rutas que suelen indicar escaneo o ataque
RUTAS_SOSPECHOSAS = [
    'wp-admin', 'wp-login', 'phpmyadmin', 'admin.php',
    '.env', '.git', 'config', 'backup', 'sql', 'dump',
    'shell', 'cmd', 'exec', '/admin/', '/administrator/',
    'setup', 'install', 'phpinfo', 'info.php', 'test.php'
]

print("Leyendo archivo de logs...")
with open(LOG_FILE, 'r', encoding='utf-8', errors='ignore') as f:
    logs = f.readlines()

print(f"Total de líneas leídas: {len(logs)}")

# Patrón para extraer IP al inicio de cada línea (formato Apache)
ip_pattern = r'^(\d+\.\d+\.\d+\.\d+)'

ips = []
rutas_por_ip = {}  # Guardaremos las rutas que visita cada IP

for line in logs:
    match = re.search(ip_pattern, line)
    if match:
        ip = match.group(1)
        ips.append(ip)
        
        # Extraer la ruta solicitada (lo que va entre comillas después de GET/POST)
        ruta_match = re.search(r'"(?:GET|POST|HEAD|PUT|DELETE) ([^\s]+)', line)
        if ruta_match:
            ruta = ruta_match.group(1)
            if ip not in rutas_por_ip:
                rutas_por_ip[ip] = []
            rutas_por_ip[ip].append(ruta)

print(f"IPs únicas encontradas: {len(set(ips))}")

print("\nAnalizando comportamiento sospechoso...")

# Contar frecuencia de cada IP
ip_counts = Counter(ips)

# Filtrar IPs con muchas peticiones
ips_frecuentes = {ip: count for ip, count in ip_counts.items() if count > UMBRAL_PETICIONES}

# Detectar IPs que visitaron rutas sospechosas
ips_rutas_maliciosas = {}
for ip, rutas in rutas_por_ip.items():
    for ruta in rutas:
        for patron in RUTAS_SOSPECHOSAS:
            if patron in ruta.lower():
                if ip not in ips_rutas_maliciosas:
                    ips_rutas_maliciosas[ip] = []
                ips_rutas_maliciosas[ip].append(ruta)
                break

# Combinar ambas listas
ips_sospechosas = set(list(ips_frecuentes.keys()) + list(ips_rutas_maliciosas.keys()))

print(f"IPs con más de {UMBRAL_PETICIONES} peticiones: {len(ips_frecuentes)}")
print(f"IPs que visitaron rutas sospechosas: {len(ips_rutas_maliciosas)}")
print(f"Total IPs sospechosas a investigar: {len(ips_sospechosas)}")

print("\nConsultando AbuseIPDB...")

def consultar_ip(ip):
    """Consulta el Abuse Score de una IP. Devuelve un número 0-100."""
    url = 'https://api.abuseipdb.com/api/v2/check'  # ✅ Usar .com
    headers = {
        'Key': config.ABUSEIPDB_KEY,
        'Accept': 'application/json'
    }
    params = {
        'ipAddress': ip,
        'maxAgeInDays': 365
    }
    try:
        response = requests.get(url, headers=headers, params=params)
        data = response.json()
        return data['data']['abuseConfidenceScore']
    except Exception:
        return 0

resultados = []
contador = 0
total = len(ips_sospechosas)

for ip in ips_sospechosas:
    contador += 1
    peticiones = ip_counts.get(ip, 0)
    rutas_maliciosas = ips_rutas_maliciosas.get(ip, [])
    score = consultar_ip(ip)
    
    resultados.append({
        'IP': ip,
        'Peticiones': peticiones,
        'RutasSospechosas': ', '.join(rutas_maliciosas[:3]),  # Máximo 3 rutas
        'AbuseScore': score
    })
    
    if contador % 10 == 0:
        print(f"  Procesadas {contador}/{total} IPs...")

print("Consulta completada.")

print("\nGenerando informe...")

# PRUEBA: Verificar que AbuseIPDB funciona con una IP maliciosa conocida
print("\n--- PRUEBA DE API ABUSEIPDB ---")
ips_prueba = ["45.155.205.233", "185.220.101.42", "23.129.64.210"]
for ip_prueba in ips_prueba:
    score_prueba = consultar_ip(ip_prueba)
    if score_prueba > 0:
        print(f"  {ip_prueba}: Abuse Score = {score_prueba}% ✓ (API funciona)")
    else:
        print(f"  {ip_prueba}: Abuse Score = {score_prueba}% (sin datos recientes)")
print("--- FIN PRUEBA ---\n")

# Ordenar por AbuseScore descendente
resultados_ordenados = sorted(resultados, key=lambda x: x['AbuseScore'], reverse=True)

# Crear informe de texto simple
with open('informe_amenazas.txt', 'w') as f:
    f.write("=" * 60 + "\n")
    f.write("THREATPULSE - INFORME DE AMENAZAS AUTOMATIZADO\n")
    f.write(f"Generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    f.write(f"Archivo analizado: {LOG_FILE}\n")
    f.write(f"Total lineas procesadas: {len(logs)}\n")
    f.write("=" * 60 + "\n\n")
    
    f.write(f"{'IP':<20} {'Peticiones':<12} {'AbuseScore':<12} Rutas sospechosas\n")
    f.write("-" * 60 + "\n")
    
    for r in resultados_ordenados[:30]:  # Top 30 más peligrosas
        f.write(f"{r['IP']:<20} {r['Peticiones']:<12} {r['AbuseScore']:<12} {r['RutasSospechosas']}\n")

print("Informe guardado como 'informe_amenazas.txt'")
print("\nTop 5 IPs más peligrosas:")
print("-" * 60)
for r in resultados_ordenados[:5]:
    print(f"  {r['IP']} - Peticiones: {r['Peticiones']} - Abuse Score: {r['AbuseScore']}%")
print("\n¡Proyecto completado!")