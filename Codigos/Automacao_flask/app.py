from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO, emit
import subprocess
import os
from datetime import datetime
import time
import uuid

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Diretório dos scripts
SCRIPT_DIR = "programas"

# Mapeamento de programas e seus parâmetros
PROGRAMS = {
    "Fazer backup das configurações": ("66_Backup_ativos.py", ["site_ip"]),
    "Comparar Configuração": ("66_Config_comparacao_html.py", ["site_ip"]),
    "Atualizar a configuração do STP": ("66_2530_atualizar_STP.py", ["site_ip"]),
    "Validar DHCP Snooping": ("66_2530_dhcp_sn.py", ["site_ip"]),
    "Validar STP": ("66_2530_stp.py", ["site_ip"]),
    "Consultar endereço MAC": ("66_2530_mac.py", ["site_ip", "end_mac"]),
    "Validar Contadores das Interfaces": ("66_2530_cont_int.py", ["site_ip"]),
    "Validar Dados Cadastrados no CMDB": ("66_2530_val_cmdb.py", ["site_ip"]),
    "Validar Enlaces entre os Ativos": ("66_2530_enlac.py", ["site_ip"]),
    "Validar Rotas": ("66_2530_rotas.py", ["site_ip"]),
    "Validar Vizinhos LLDP com o CMDB": ("66_2530_vizin.py", ["site_ip"]),
    "Validar Vlans das interfaces": ("66_2530_vlans.py", ["site_ip"]),
    "Verificar Telemetria dos Ativos": ("66_2530_telem.py", ["site_ip"]),
}

# Armazena processos em execução por usuário
running_processes = {}

@app.route("/")
def index():
    return render_template("index.html", programs=PROGRAMS)

@socketio.on("execute_script")
def execute_script(data):
    session_id = data["session_id"]
    program_name = data["program"]
    params = data["params"]

    if program_name not in PROGRAMS:
        emit("output", {"session_id": session_id, "data": "Programa inválido.\n"})
        return

    script, required_params = PROGRAMS[program_name]
    script_path = os.getcwd()
    script_path = os.path.abspath(os.path.join(script_path, os.pardir))
    script_path = script_path + "/" + script
    print(script_path)

    # Construir os argumentos do script
    args = [params[param] for param in required_params if param in params]

    try:
        # Se houver um processo rodando para o usuário, interrompa antes de iniciar um novo
        if session_id in running_processes:
            running_processes[session_id].terminate()
            del running_processes[session_id]

        # Para "Comparar Configuração", abrir uma nova aba
        if script == "66_Config_comparacao_html.py":
            process = subprocess.Popen(
                ["/usr/bin/python3", "-u", script_path] + args,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1
            )
            # Aguarda 5 segundos para execução do programa
            time.sleep(5)
            # Abre o arquivo salvo
            timestamp = datetime.now().strftime("%Y-%m-%d_%H")
            emit("open_new_tab", {"url": f"/static/Comparar_config_" + str(args[0]) + "_" + timestamp + ".html"})
            return

        # Executa o script
        process = subprocess.Popen(
            ["/usr/bin/python3", script_path] + args,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )

        running_processes[session_id] = process

        # Captura a saída em tempo real
        for line in iter(process.stdout.readline, ""):
            emit("output", {"session_id": session_id, "data": line})

        process.stdout.close()
        process.wait()

        del running_processes[session_id]

    except Exception as e:
        emit("output", {"session_id": session_id, "data": f"Erro: {str(e)}\n"})

@socketio.on("stop_script")
def stop_script(data):
    session_id = data["session_id"]
    if session_id in running_processes:
        running_processes[session_id].terminate()
        del running_processes[session_id]
        emit("output", {"session_id": session_id, "data": "Execução interrompida.\n"})

@app.route("/open_html/<path:filename>")
def open_html(filename):
    return redirect(url_for("static", filename=filename))

if __name__ == "__main__":
    socketio.run(app, debug=True, host="0.0.0.0", port=5000)
