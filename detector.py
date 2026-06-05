import re
from collections import Counter
import requests
import config
from datetime import datetime
from jinja2 import Template
import smtplib
from email.mime.text import MIMEText

# Archivo de logs a analizar
LOG_FILE = "access.log"
UMBRAL_PETICIONES = 50

RUTAS_SOSPECHOSAS = [
    'wp-admin', 'wp-login', 'phpmyadmin', 'admin.php',
    '.env', '.git', 'config', 'backup', 'sql', 'dump',
    'shell', 'cmd', 'exec', '/admin/', '/administrator/',
    'setup', 'install', 'phpinfo', 'info.php', 'test.php'
]

def consultar_ip(ip):
    url = 'https://api.abuseipdb.com/api/v2/check'
    headers = {'Key': config.ABUSEIPDB_KEY, 'Accept': 'application/json'}
    params = {'ipAddress': ip, 'maxAgeInDays': 365}
    try:
        response = requests.get(url, headers=headers, params=params)
        return response.json()['data']['abuseConfidenceScore']
    except Exception:
        return 0

def enviar_correo(html_content):
    msg = MIMEText(html_content, 'html')
    msg['Subject'] = 'ThreatPulse - Alerta de Amenazas'
    msg['From'] = config.EMAIL_REMITENTE
    msg['To'] = config.EMAIL_DESTINATARIO
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(config.EMAIL_REMITENTE, config.EMAIL_PASSWORD)
        smtp.send_message(msg)
    print("Correo enviado correctamente")

# --- LECTURA DE LOGS ---
print("Leyendo archivo de logs...")
with open(LOG_FILE, 'r', encoding='utf-8', errors='ignore') as f:
    logs = f.readlines()
print(f"Total de líneas leídas: {len(logs)}")

ip_pattern = r'^(\d+\.\d+\.\d+\.\d+)'
ips = []
rutas_por_ip = {}

for line in logs:
    match = re.search(ip_pattern, line)
    if match:
        ip = match.group(1)
        ips.append(ip)
        ruta_match = re.search(r'"(?:GET|POST|HEAD|PUT|DELETE) ([^\s]+)', line)
        if ruta_match:
            rutas_por_ip.setdefault(ip, []).append(ruta_match.group(1))

print(f"IPs únicas encontradas: {len(set(ips))}")
print("\nAnalizando comportamiento sospechoso...")

ip_counts = Counter(ips)
ips_frecuentes = {ip: c for ip, c in ip_counts.items() if c > UMBRAL_PETICIONES}

ips_rutas_maliciosas = {}
for ip, rutas in rutas_por_ip.items():
    for ruta in rutas:
        for patron in RUTAS_SOSPECHOSAS:
            if patron in ruta.lower():
                ips_rutas_maliciosas.setdefault(ip, []).append(ruta)
                break

ips_sospechosas = set(list(ips_frecuentes.keys()) + list(ips_rutas_maliciosas.keys()))
print(f"IPs con más de {UMBRAL_PETICIONES} peticiones: {len(ips_frecuentes)}")
print(f"IPs que visitaron rutas sospechosas: {len(ips_rutas_maliciosas)}")
print(f"Total IPs sospechosas a investigar: {len(ips_sospechosas)}")

# --- CONSULTA ABUSEIPDB ---
print("\nConsultando AbuseIPDB...")
resultados = []
for i, ip in enumerate(ips_sospechosas, 1):
    resultados.append({
        'IP': ip,
        'Peticiones': ip_counts.get(ip, 0),
        'RutasSospechosas': ', '.join(ips_rutas_maliciosas.get(ip, [])[:3]),
        'AbuseScore': consultar_ip(ip)
    })
    if i % 10 == 0:
        print(f"  Procesadas {i}/{len(ips_sospechosas)} IPs...")
print("Consulta completada.")

# --- PRUEBA API ---
print("\n--- PRUEBA DE API ABUSEIPDB ---")
for ip_test in ["45.155.205.233", "185.220.101.42", "23.129.64.210"]:
    score = consultar_ip(ip_test)
    print(f"  {ip_test}: Abuse Score = {score}% {'✓' if score > 0 else '(sin datos recientes)'}")
print("--- FIN PRUEBA ---\n")

resultados_ordenados = sorted(resultados, key=lambda x: x['AbuseScore'], reverse=True)

# --- INFORME TXT ---
with open('informe_amenazas.txt', 'w') as f:
    f.write("=" * 60 + "\n")
    f.write("THREATPULSE - INFORME DE AMENAZAS AUTOMATIZADO\n")
    f.write(f"Generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    f.write(f"Archivo analizado: {LOG_FILE}\n")
    f.write(f"Total lineas procesadas: {len(logs)}\n")
    f.write("=" * 60 + "\n\n")
    f.write(f"{'IP':<20} {'Peticiones':<12} {'AbuseScore':<12} Rutas sospechosas\n")
    f.write("-" * 60 + "\n")
    for r in resultados_ordenados[:30]:
        f.write(f"{r['IP']:<20} {r['Peticiones']:<12} {r['AbuseScore']:<12} {r['RutasSospechosas']}\n")

print("Informe guardado como 'informe_amenazas.txt'")

# --- INFORME HTML ---
with open('template.html') as f:
    template = Template(f.read())

html = template.render(date=datetime.now().strftime('%Y-%m-%d %H:%M'), data=resultados_ordenados[:30])
with open('informe_amenazas.html', 'w') as f:
    f.write(html)
print("Informe HTML guardado como 'informe_amenazas.html'")

# --- TOP 5 ---
print("\nTop 5 IPs más peligrosas:")
print("-" * 60)
for r in resultados_ordenados[:5]:
    print(f"  {r['IP']} - Peticiones: {r['Peticiones']} - Abuse Score: {r['AbuseScore']}%")

# --- ENVÍO CORREO ---
enviar_correo(html)
print("\n¡Proyecto completado!")