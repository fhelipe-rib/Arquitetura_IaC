import os
import git
import datetime
import logging
import sys

# Importando bibliotecas para o multithreading
import concurrent.futures

# Importando modulo para manipulação de IPs
import ipaddress

# Importando modulos do Netmiko
from netmiko import Netmiko
from netmiko import NetMikoAuthenticationException, NetMikoTimeoutException, ReadTimeout

# Importando script customizado
from Switch import reutil
from CMDB import cmdb_rest

# Importando modulos para adição da chave SSH
import subprocess
import os


def update_git(mensagem):
    # Atualizar Git com os arquivos coletados
    log_exe.warning("Atualizando repositório Git")
    repo = git.Repo(repo_path)
    repo.git.add(all=True)
    repo.index.commit(mensagem)
    origin = repo.remote(name="origin")
    origin.push()
    return()


def conectar_sw(dev, site):
    retorno = ''
    ativo = {}
    ativo['site_slug'] = site['slug']
    ativo['site_id'] = site['id']
    if dev['device_role']['id'] == 4 or dev['device_role']['id'] == 5 or dev['device_role']['id'] == 6 or dev['device_role']['id'] == 7:
        ativo['dev_name'] = dev['name']
        ativo['dev_id'] = dev['id']
        ativo['dev_type'] = dev['device_type']['display']
        # Confirma a existência da Plataforma e atribui, se for o caso
        if dev['platform'] == None:
            log_exe.error("Plataforma não cadastrada no ativo: %s, ID: %s. NECESSÁRIO CORREÇÃO", ativo['dev_name'], ativo['dev_id'])
            retorno += str(ativo['dev_id']) + " - Plataforma não cadastrada"
            return retorno
        else:
            ativo['dev_platform'] = dev['platform']['id']
        # Confirma a existência do endereço IPv4 e atribui, se for o caso
        if dev['primary_ip4'] == None:
            log_exe.error("Endereço IPv4 não cadastrado no ativo: %s, ID: %s. NECESSÁRIO CORREÇÃO", ativo['dev_name'], ativo['dev_id'])
            retorno += str(ativo['dev_id']) + " - Endereço IPv4 não cadastrado"
            return retorno
        else:
            ativo['dev_ipv4'] = dev['primary_ip4']['address'][:-3]
        # Conecta via SSH ao tivos e coleta os arquivos de configuração
        # Identifica e o ativo e popula o tipo de ativo
        # Para ativos ArubaOS
        if ativo['dev_platform'] == 1:
            tipo_ativo = 'hp_procurve'
            command_run = 'show running-config structured'
            command_start = 'show config structured'
        # Para ativos Comware
        elif 3 <= ativo['dev_platform'] <= 8:
            tipo_ativo = 'hp_comware'
            command_run = 'display current-configuration'
            command_start = 'display saved-configuration'
        else:
            log_exe.error("Plataforma não conhecida no ativo: %s, ID: %s, IPv4: %s. NECESSÁRIO CORREÇÃO", ativo['dev_name'], ativo['dev_id'], ativo['dev_ipv4'])
            retorno += str(ativo['dev_ipv4']) + " - Plataforma não cadastrada"
            return retorno
        # Identifica o ativo e popula a senha
        if '5500' in ativo['dev_type'] or '5510' in ativo['dev_type'] or '5520' in ativo['dev_type'] or '5820' in ativo['dev_type'] or '4800' in ativo['dev_type']:
            senha = '==senha=='
        else:
            senha = '==senha=='
        # Variável para conexão via biblioteca Netmiko
        device_dict = {
            'host': ativo['dev_ipv4'],
            'username': 'admin',
            'password': senha,
            'device_type': tipo_ativo,
            'global_delay_factor': 2,
        }
        # Verifica se o dispositivo esta online
        response = os.system("ping -c 1 " + device_dict["host"] + "> /dev/null")
        if response != 0:
            retorno += ativo['dev_ipv4'] + " - OFFLINE"
            log_exe.error("Ativo OFFLINE: %s, ID: %s, IPv4: %s.", ativo['dev_name'], ativo['dev_id'], ativo['dev_ipv4'])
            erro_zabbix = "zabbix_sender -z ==ENDERECO_IP_ZABBIX== -s Projeto_Switch_Netbox -k Trap_Erros_Backup -o \"" + ativo['dev_ipv4'] + " - LOGIN - OFFLINE\""
            os.system(erro_zabbix)
            return retorno
        # Tenta conectar ao equipamento
        try:
            net_connect = Netmiko(**device_dict)
        except NetMikoTimeoutException:
            retorno += ativo['dev_ipv4'] + " - LOGIN - ERRO AO CONECTAR - TIMEOUT,"
            log_exe.error("FALHA ao conectar - TIMEOUT: %s, ID: %s, IPv4: %s.", ativo['dev_name'], ativo['dev_id'], ativo['dev_ipv4'])
            erro_zabbix = "zabbix_sender -z ==ENDERECO_IP_ZABBIX== -s Projeto_Switch_Netbox -k Trap_Erros_Backup -o \"" + ativo['dev_ipv4'] + " - LOGIN - ERRO AO CONECTAR - TIMEOUT\""
            os.system(erro_zabbix)
            return retorno
        except NetMikoAuthenticationException:
            retorno += ativo['dev_ipv4'] + " - LOGIN - ERRO AO CONECTAR - AUTENTICAÇÃO."
            log_exe.error("FALHA ao conectar - AUTENTICAÇÃO: %s, ID: %s, IPv4: %s.", ativo['dev_name'], ativo['dev_id'], ativo['dev_ipv4'])
            erro_zabbix = "zabbix_sender -z ==ENDERECO_IP_ZABBIX== -s Projeto_Switch_Netbox -k Trap_Erros_Backup -o \"" + ativo['dev_ipv4'] + " - LOGIN - ERRO AO CONECTAR - AUTENTICAÇÃO\""
            os.system(erro_zabbix)
            return retorno
        except Exception:
            retorno += ativo['dev_ipv4'] + " - LOGIN - ERRO AO CONECTAR - DIVERSOS."
            log_exe.error("FALHA ao conectar - DIVERSOS: %s, ID: %s, Ipv4: %s.", ativo['dev_name'], ativo['dev_id'], ativo['dev_ipv4'])
            erro_zabbix = "zabbix_sender -z ==ENDERECO_IP_ZABBIX== -s Projeto_Switch_Netbox -k Trap_Erros_Backup -o \"" + ativo['dev_ipv4'] + " - LOGIN - ERRO AO CONECTAR - DIVERSOS\""
            os.system(erro_zabbix)
            return retorno
        # Coleta o prompt do ativo e compara com o nome cadastrado no CMDB
        prompt = net_connect.find_prompt()
        if tipo_ativo == 'hp_comware':
            if prompt[1:-1] != ativo['dev_name']:
                retorno += ativo['dev_ipv4'] + " - CMDB - EQUIPAMENTO COM O NOME DIVERGENTE."
                log_exe.error("EQUIPAMENTO COM O NOME DIVERGENTE, FAVOR VERIFICAR: %s, ID: %s, IPv4: %s. NECESSÁRIO CORREÇÃO", ativo['dev_name'], ativo['dev_id'], ativo['dev_ipv4'])
                erro_zabbix = "zabbix_sender -z ==ENDERECO_IP_ZABBIX== -s Projeto_Switch_Netbox -k Trap_Erros_Backup -o \"" + ativo['dev_ipv4'] + " - CMDB - EQUIPAMENTO COM O NOME DIVERGENTE\""
                os.system(erro_zabbix)
                return retorno
        else:
            if prompt[:-1] != ativo['dev_name']:
                retorno += ativo['dev_ipv4'] + " - CMDB - EQUIPAMENTO COM O NOME DIVERGENTE."
                log_exe.error("EQUIPAMENTO COM O NOME DIVERGENTE, FAVOR VERIFICAR: %s, ID: %s, IPv4: %s. NECESSÁRIO CORREÇÃO", ativo['dev_name'], ativo['dev_id'], ativo['dev_ipv4'])
                erro_zabbix = "zabbix_sender -z ==ENDERECO_IP_ZABBIX== -s Projeto_Switch_Netbox -k Trap_Erros_Backup -o \"" + ativo['dev_ipv4'] + " - CMDB - EQUIPAMENTO COM O NOME DIVERGENTE\""
                os.system(erro_zabbix)
                return retorno
        # habilitar advanced CLI ou screen-length 0 em modelos especificos
        if "1910" in ativo['dev_type']:
            reutil.login_1910(net_connect)
            net_connect.send_command("screen-length disable")
        elif "2928" in ativo['dev_type']:
            reutil.login_1910(net_connect)
            net_connect.send_command("screen-length disable")
        elif "2952" in ativo['dev_type']:
            reutil.login_1910(net_connect)
            net_connect.send_command("screen-length disable")
        elif "1920" in ativo['dev_type']:
            reutil.login_1920(net_connect)
            net_connect.send_command("screen-length disable")
        elif "1950" in ativo['dev_type']:
            reutil.login_1950(net_connect)
            net_connect.send_command("screen-length disable")
        elif "4210" in ativo['dev_type']:
            reutil.screen_leng_4210_4500(net_connect)
        elif "4500" in ativo['dev_type']:
            reutil.screen_leng_4210_4500(net_connect)
        elif "5120" in ativo['dev_type']:
            net_connect.send_command("screen-length disable")
            net_connect.send_command_timing("undo terminal monitor")
        elif "5130" in ativo['dev_type']:
            net_connect.send_command("screen-length disable")
            net_connect.send_command_timing("undo terminal monitor")
        elif "5140" in ativo['dev_type']:
            net_connect.send_command("screen-length disable")
            net_connect.send_command_timing("undo terminal monitor")
        elif "4800" in ativo['dev_type']:
            net_connect.send_command("screen-length disable")
            net_connect.send_command_timing("undo terminal monitor")
        elif "5500" in ativo['dev_type']:
            net_connect.send_command("screen-length disable")
            net_connect.send_command_timing("undo terminal monitor")
        elif "5510" in ativo['dev_type']:
            net_connect.send_command("screen-length disable")
            net_connect.send_command_timing("undo terminal monitor")
        elif "5520" in ativo['dev_type']:
            net_connect.send_command("screen-length disable")
            net_connect.send_command_timing("undo terminal monitor")
        elif "5820" in ativo['dev_type']:
            net_connect.send_command("screen-length disable")
            net_connect.send_command_timing("undo terminal monitor")
        elif "2530" in ativo['dev_type']:
            net_connect.send_command("screen-length 1000")
        elif "2540" in ativo['dev_type']:
            net_connect.send_command("screen-length 1000")
        elif "2930" in ativo['dev_type']:
            net_connect.send_command("screen-length 1000")
        else:
            retorno += ativo['dev_ipv4'] + " - CMDB - DEVICE TYPE NÃO CADASTRADO (ETAPA SCREEN LENGHT)."
            log_exe.error("DEVICE TYPE NÃO CADASTRADO (ETAPA SCREEN LENGHT): %s, ID: %s, IPv4: %s. NECESSÁRIO CORREÇÃO", ativo['dev_name'], ativo['dev_id'], ativo['dev_ipv4'])
            erro_zabbix = "zabbix_sender -z ==ENDERECO_IP_ZABBIX== -s Projeto_Switch_Netbox -k Trap_Erros_Backup -o \"" + ativo['dev_ipv4'] + " - CMDB - DEVICE TYPE NÃO CADASTRADO (ETAPA SCREEN LENGHT)\""
            os.system(erro_zabbix)
            return retorno
        # Coleta a running config
        try:
            save_run = net_connect.send_command(command_run)
        except OSError:
            retorno += ativo['dev_ipv4'] + " - FALHA AO COLETAR A RUNNING CONFIG - OS."
            log_exe.error("FALHA AO COLETAR A RUNNING CONFIG - OS: %s, ID: %s, IPv4: %s. NECESSÁRIO CORREÇÃO", ativo['dev_name'], ativo['dev_id'], ativo['dev_ipv4'])
            erro_zabbix = "zabbix_sender -z ==ENDERECO_IP_ZABBIX== -s Projeto_Switch_Netbox -k Trap_Erros_Backup -o \"" + ativo['dev_ipv4'] + " - FALHA AO COLETAR A RUNNING CONFIG - OS\""
            os.system(erro_zabbix)
        except ReadTimeout:
            retorno += ativo['dev_ipv4'] + " - FALHA AO COLETAR A RUNNING CONFIG - TIMEOUT."
            log_exe.error("FALHA AO COLETAR A RUNNING CONFIG - TIMEOUT: %s, ID: %s, IPv4: %s. NECESSÁRIO CORREÇÃO", ativo['dev_name'], ativo['dev_id'], ativo['dev_ipv4'])
            erro_zabbix = "zabbix_sender -z ==ENDERECO_IP_ZABBIX== -s Projeto_Switch_Netbox -k Trap_Erros_Backup -o \"" + ativo['dev_ipv4'] + " - FALHA AO COLETAR A RUNNING CONFIG - TIMEOUT\""
            os.system(erro_zabbix)
        # Coleta a startup config
        try:
            save_start = net_connect.send_command(command_start)
        except OSError:
            retorno += ativo['dev_ipv4'] + " - FALHA AO COLETAR A STARTUP CONFIG - OS."
            log_exe.error("FALHA AO COLETAR A STARTUP CONFIG - OS: %s, ID: %s, IPv4: %s. NECESSÁRIO CORREÇÃO", ativo['dev_name'], ativo['dev_id'], ativo['dev_ipv4'])
            erro_zabbix = "zabbix_sender -z ==ENDERECO_IP_ZABBIX== -s Projeto_Switch_Netbox -k Trap_Erros_Backup -o \"" + ativo['dev_ipv4'] + " - FALHA AO COLETAR A STARTUP CONFIG - OS\""
            os.system(erro_zabbix)
        except ReadTimeout:
            retorno += ativo['dev_ipv4'] + " - FALHA AO COLETAR A STARTUP CONFIG - TIMEOUT."
            log_exe.error("FALHA AO COLETAR A STARTUP CONFIG - TIMEOUT: %s, ID: %s, IPv4: %s. NECESSÁRIO CORREÇÃO", ativo['dev_name'], ativo['dev_id'], ativo['dev_ipv4'])
            erro_zabbix = "zabbix_sender -z ==ENDERECO_IP_ZABBIX== -s Projeto_Switch_Netbox -k Trap_Erros_Backup -o \"" + ativo['dev_ipv4'] + " - FALHA AO COLETAR A STARTUP CONFIG - TIMEOUT\""
            os.system(erro_zabbix)
        # Salva a running config
        dir = repo_path + '/' + str(ativo['site_id']) + '_' + ativo['site_slug']
        if not os.path.exists(dir):
            os.makedirs(dir)
        # Salva a running config
        with open(dir + '/' + ativo['dev_name'] + '-' + ativo['dev_ipv4'] + '-RUNNING_CONFIG.txt', 'w') as f:
            f.write(save_run)
            retorno += str(ativo['dev_ipv4']) + " - Running config SALVA.\n"
            log_exe.warning("Salvando running config do ativo: %s, ID: %s, IPv4: %s.", ativo['dev_name'], str(ativo['dev_id']), ativo['dev_ipv4'])
        # Salva a startup config
        with open(dir + '/' + ativo['dev_name'] + '-' + ativo['dev_ipv4'] + '-STARTUP_CONFIG.txt', 'w') as f:
            f.write(save_start)
            retorno += str(ativo['dev_ipv4']) + " - Startup config SALVA."
            log_exe.warning("Salvando startup config do ativo: %s, ID: %s, IPv4: %s.", ativo['dev_name'], str(ativo['dev_id']), ativo['dev_ipv4'])
        return retorno
    return retorno


def valida_ativo(dev, sitee):
    # Conecta ao equipamento
    retorno_valida = dev['primary_ip4']['address'][:-3]
    retorno_valida += '\n' + dev['name'] + '\n'
    retorno_valida += conectar_sw(dev, sitee)
    retorno_valida += '\n' + '-' * 40
    print(retorno_valida)
    return


def lista_ativos(devic, sit):
        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
            futures = [executor.submit(valida_ativo, devi, sit) for devi in devic]
        log_exe.warning("Finalizando backup de ativos do site: %s, ID: %s", sit['slug'], sit['id'])


def setup_logger(logger_name, log_file, level=logging.WARNING):
    # Configura o formato dos arquivos de logs
    l = logging.getLogger(logger_name)
    formatter = logging.Formatter('%(asctime)s,%(message)s','%Y/%m/%d,%I:%M:%S')
    fileHandler = logging.FileHandler(log_file, mode='a')
    fileHandler.setFormatter(formatter)
    l.setLevel(level)
    l.addHandler(fileHandler)
    return


def main(x):
    # Usuário deve informar o IP ou site ID do CMDB
    print('PROGRAMA PARA REALIZAR BACKUP DAS CONFIGURAÇÕES EM TODOS OS EQUIPAMENTOS')

    # Variável de controle
    var_controle = 0
    # Verifica se o digitado é um site no CMDB
    if x == 'GERAL':
        print('VERIFICANDO EM TODOS OS ATIVOS com IPv4 do CMDB')
        var_controle = 100
    if len(x) == 4 and x.isdigit():
        print('Formato do CMDB VALIDADO')
        var_controle = 1
    # Verifica se o digitado é um IP
    # Temporariamente, essa operação não é permitida por IP
    try:
        if ipaddress.ip_address(x) != True:
            print('NÃO É PERMITIDO REALIZAR O BACKUP POR IP')
    except Exception:
        ip = 0
    if var_controle == 0:
        print("Erro - CMDB/IP COM FORMATO INVÁLIDO, inserir novamente \n")
        print("SAINDO DO PROGRAMA")
        exit()

    # Caso positivo, chama a função e conecta ao ativo
    print('-' * 40)
    # Verificando em todos os ativos Aruba 2530 com IP do CMDB
    if x == 'GERAL':
    # Lista todos os sites cadastrados no CMDB
        sites = cmdb_rest.list_all_sites()
        for site in sites:
            # Descanrtando os sites STI-DC e STI - ESTOQUE
            if site['id'] == 206 or site['id'] == 108:
                break
            print(f"Iniciando o backup de todos os ativos do site: {site['name']}, ID: {site['id']}")
            log_exe.warning("Iniciando backup de ativos do site: %s, ID: %s", site['slug'], site['id'])
            print('=' * 60)
            # Lista os ativos cadastrados
            devices = cmdb_rest.list_device_todos_role_id_por_site(str(site['id']))
            # Cicla pelos ativos via multithread
            print(devices)
            lista_ativos(devices, site)
    if var_controle == 10:
        print(f"Iniciando o backup do ativo: {ip}")
        conectar_sw(ip)
    if var_controle == 1:
        # Lista todos os sites cadastrados no CMDB
        sites = cmdb_rest.list_all_sites()
        for site in sites:
            # Descanrtando os sites STI-DC e STI - ESTOQUE
            if site['id'] == 206 or site['id'] == 108:
                break
            if site['id'] == int(x):
                print(f"Iniciando o backup de todos os ativos do site: {site['name']}, ID: {site['id']}")
                log_exe.warning("Iniciando backup de ativos do site: %s, ID: %s", site['slug'], site['id'])
                print('-' * 40)
                # Lista os ativos cadastrados
                devices = cmdb_rest.list_device_todos_role_id_por_site(str(site['id']))
                # Cicla pelos ativos via multithread
                lista_ativos(devices, site)
                break
        else:
            print(f"ERRO: O SITE INDICADO NÃO EXISTE NO CMDB: {x}")

    # Coleta a hora de término da coleta para registro no Git
    hora_git = datetime.datetime.now()
    # Mensagem a ser gravada no commit do Git
    comm_mensgem = 'Commit via Interface Web. Data: ' + str(hora_git.strftime("%d-%m-%Y %H:%M"))
    # Atualiza repositório remoto
    update = update_git(comm_mensgem)
    hora_final = datetime.datetime.now()
    delta = hora_final - hora
    print(f"O programa demorou {delta} segundos para finalizar")



# Inicia o ssh-agent e captura as variáveis de ambiente
process = subprocess.run("ssh-agent -s", capture_output=True, text=True, shell=True)
output = process.stdout

# Extrai variáveis de ambiente do ssh-agent
for line in output.splitlines():
    if "=" in line:
        key, value = line.split(";")[0].split("=")
        # Define no ambiente do processo Python
        os.environ[key] = value

# Adiciona a chave privada ao ssh-agent
subprocess.run(["ssh-add", os.path.expanduser("~/.ssh/==CHAVE_SSH==")])

#os.system('ssh-add /home/admin/.ssh/rsa_sti')
# Coleta a hora da coleta
hora = datetime.datetime.now()
hora_inicio = datetime.datetime.now()
print(hora_inicio)
# Diretório configurado para o Git (arquivos serão salvos aqui)
repo_path = os.getcwd()
repo_path = os.path.abspath(os.path.join(repo_path, os.pardir))
repo_path = os.path.abspath(os.path.join(repo_path, os.pardir))
repo_path = repo_path + '/Backup_ativos'

# # Atualizando repositótio Git local
g = git.cmd.Git(repo_path)
g.pull()

# Configurações de log
log_dir = os.getcwd()
log_dir = os.path.abspath(os.path.join(log_dir, os.pardir))
log_dir = os.path.abspath(os.path.join(log_dir, os.pardir))
log_dir = log_dir + '/Backup_ativos/LOG'
#print(log_dir)
logfile_exec = log_dir + '/Backup_ativos_' + str(hora.strftime("%Y-%m-%d") + '.txt')
#print(logfile_exec)

# Caso não exista, cria o diretórios, arquivos de log e salva os cabeçalhos
# Diretório do arquivo de log de execução
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# Configuração do log
setup_logger('log_exec', logfile_exec)
log_exe = logging.getLogger('log_exec')
log_exe.warning("============ Iniciando backup ============")

# # # Atualizando repositótio Git local
log_exe.warning(f"SUCESSO,Repositório Git SINCRONIZADO com o servidor,")


if __name__ == "__main__":
    # Passando os argumentos do Python
    main(sys.argv[1])
