import subprocess
import time
import os

# Lista dos scripts Python a serem executados
programas = [
    "66_2530_cont_int.py",
    "66_2530_dhcp_sn.py",
    "66_2530_enlac.py",
    "66_2530_rotas.py",
    "66_2530_stp.py",
    "66_2530_telem.py",
    "66_2530_val_cmdb.py",
    "66_2530_vizin.py",
    "66_2530_vlans.py"
]

# Caminho absoluto opcional, se os scripts não estiverem no mesmo diretório
caminho_programas = os.getcwd()
caminho_programas = caminho_programas + '/'
# Argumento fixo
argumento = "GERAL"

# Executar cada script em sequência com 60 segundos de intervalo
for programa in programas:
    print(f"{caminho_programas}{programa} {argumento}")
    try:
        print(f"Executando {programa} com argumento '{argumento}'...")
        subprocess.run(["python3", f"{caminho_programas}{programa}", argumento], check=True)
        print(f"{programa} finalizado. Aguardando 60 segundos...\n")
        time.sleep(60)
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar {programa}: {e}")
