import logging
import os
import git
import datetime

# Importando bibliotecas para o multithreading
import concurrent.futures

# Importando modulos do Netmiko
from netmiko import Netmiko
from netmiko import NetMikoAuthenticationException, NetMikoTimeoutException, ReadTimeout

# Importando script customizado
from Switch import reutil
from CMDB import cmdb_rest


def update_git(mensagem):
    # Atualizar Git com os arquivos coletados
    logging.warning("Atualizando repositório Git")
    repo = git.Repo(repo_path)
    repo.git.add('--all')
    repo.index.commit(mensagem)
    repo.remotes.origin.push()
    return()


def backup_ativo(site, dev):
    ativo = {}
    ativo['site_slug'] = site['slug']
    ativo['site_id'] = site['id']
    if dev['device_role']['id'] == 4 or dev['device_role']['id'] == 5 or dev['device_role']['id'] == 6 or dev['device_role']['id'] == 7:
        ativo['dev_name'] = dev['name']
        ativo['dev_id'] = dev['id']
        ativo['dev_type'] = dev['device_type']['display']
        # Confirma a existência da Plataforma e atribui, se for o caso
        if dev['platform'] == None:
            logging.error("Plataforma não cadastrada no ativo: %s, ID: %s. NECESSÁRIO CORREÇÃO", ativo['dev_name'], ativo['dev_id'])
            return
        else:
            ativo['dev_platform'] = dev['platform']['id']
        # Confirma a existência do endereço IPv4 e atribui, se for o caso
        if dev['primary_ip4'] == None:
            logging.error("Endereço IPv4 não cadastrado no ativo: %s, ID: %s. NECESSÁRIO CORREÇÃO", ativo['dev_name'], ativo['dev_id'])
            return
        else:
            ativo['dev_ipv4'] = dev['primary_ip4']['address'][:-3]
#            print(ativo['dev_ipv4'])
        # Conecta via SSH ao tivos e coleta os arquivos de configuração
        # Identifica e o ativo e popula o tipo de ativo
        if ativo['dev_platform'] == 1:
            tipo_ativo = 'hp_procurve'
            command_run = 'show running-config structured'
            command_start = 'show config structured'
        elif 3 <= ativo['dev_platform'] <= 8:
            tipo_ativo = 'hp_comware'
            command_run = 'display current-configuration'
            command_start = 'display saved-configuration'
        else:
            logging.error("Plataforma não conhecida no ativo: %s, ID: %s, IPv4: %s. NECESSÁRIO CORREÇÃO", ativo['dev_name'], ativo['dev_id'], ativo['dev_ipv4'])
            return
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
            logging.error("Ativo OFFLINE: %s, ID: %s, IPv4: %s.", ativo['dev_name'], ativo['dev_id'], ativo['dev_ipv4'])
            return
        # Tenta conectar ao equipamento
        try:
            net_connect = Netmiko(**device_dict)
        except NetMikoTimeoutException:
            logging.error("FALHA ao conectar - TIMEOUT: %s, ID: %s, IPv4: %s.", ativo['dev_name'], ativo['dev_id'], ativo['dev_ipv4'])
            return
        except NetMikoAuthenticationException:
            logging.error("FALHA ao conectar - AUTENTICAÇÃO: %s, ID: %s, IPv4: %s.", ativo['dev_name'], ativo['dev_id'], ativo['dev_ipv4'])
            return
        except Exception:
            logging.error("FALHA ao conectar - DIVERSOS: %s, ID: %s, Ipv4: %s.", ativo['dev_name'], ativo['dev_id'], ativo['dev_ipv4'])
            return
        # Coleta o prompt do ativo e compara com o nome cadastrado no CMDB
        prompt = net_connect.find_prompt()
        if tipo_ativo == 'hp_comware':
            if prompt[1:-1] != ativo['dev_name']:
                logging.error("EQUIPAMENTO COM O NOME DIVERGENTE, FAVOR VERIFICAR: %s, ID: %s, IPv4: %s. NECESSÁRIO CORREÇÃO", ativo['dev_name'], ativo['dev_id'], ativo['dev_ipv4'])
                return
        else:
            if prompt[:-1] != ativo['dev_name']:
                logging.error("EQUIPAMENTO COM O NOME DIVERGENTE, FAVOR VERIFICAR: %s, ID: %s, IPv4: %s. NECESSÁRIO CORREÇÃO", ativo['dev_name'], ativo['dev_id'], ativo['dev_ipv4'])
                return
        print(f"LOGADO NO ATIVO: {ativo['dev_name']}")
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
            logging.error("DEVICE TYPE NÃO CADASTRADO (ETAPA SCREEN LENGHT): %s, ID: %s, IPv4: %s. NECESSÁRIO CORREÇÃO", ativo['dev_name'], ativo['dev_id'], ativo['dev_ipv4'])
            return
        print(f"COLETA CONFIGS {ativo['dev_name']}")
        # Coleta a running config
        try:
            save_run = net_connect.send_command(command_run)
        except OSError:
            logging.error("FALHA AO COLETAR A RUNNING CONFIG - OS: %s, ID: %s, IPv4: %s. NECESSÁRIO CORREÇÃO", ativo['dev_name'], ativo['dev_id'], ativo['dev_ipv4'])
        except ReadTimeout:
            logging.error("FALHA AO COLETAR A RUNNING CONFIG - TIMEOUT: %s, ID: %s, IPv4: %s. NECESSÁRIO CORREÇÃO", ativo['dev_name'], ativo['dev_id'], ativo['dev_ipv4'])
        # Coleta a startup config
        try:
            save_start = net_connect.send_command(command_start)
        except OSError:
            logging.error("FALHA AO COLETAR A STARTUP CONFIG - OS: %s, ID: %s, IPv4: %s. NECESSÁRIO CORREÇÃO", ativo['dev_name'], ativo['dev_id'], ativo['dev_ipv4'])
        except ReadTimeout:
            logging.error("FALHA AO COLETAR A STARTUP CONFIG - TIMEOUT: %s, ID: %s, IPv4: %s. NECESSÁRIO CORREÇÃO", ativo['dev_name'], ativo['dev_id'], ativo['dev_ipv4'])
        # Salva a running config
        dir = repo_path + '/' + str(ativo['site_id']) + '_' + ativo['site_slug']
        if not os.path.exists(dir):
            os.makedirs(dir)
        # Salva a running config
        with open(dir + '/' + ativo['dev_name'] + '-' + ativo['dev_ipv4'] + '-RUNNING_CONFIG.txt', 'w') as f:
            f.write(save_run)
            logging.warning("Salvando running config do ativo: %s, ID: %s, IPv4: %s.", ativo['dev_name'], str(ativo['dev_id']), ativo['dev_ipv4'])
        # Salva a startup config
        with open(dir + '/' + ativo['dev_name'] + '-' + ativo['dev_ipv4'] + '-STARTUP_CONFIG.txt', 'w') as f:
            f.write(save_start)
            logging.warning("Salvando startup config do ativo: %s, ID: %s, IPv4: %s.", ativo['dev_name'], str(ativo['dev_id']), ativo['dev_ipv4'])
        return
    return


def coletar_dados_ativos(devices, site):
    # Lista todos os ativos com IPv4 primário configurados de um determinado site
    logging.warning("Iniciando backup de ativos do site: %s, ID: %s", site['slug'], site['id'])
    print(f"Iniciando backup de ativos do site: {site['slug']}, ID: {site['id']}")
    # Lista, coleta e salva arquivos com informações relevantes de cada dispositivo
    # Obtém o slug do site do loop
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        futures = [executor.submit(backup_ativo, site, dev) for dev in devices]
    logging.warning("Finalizando backup de ativos do site: %s, ID: %s", site['slug'], site['id'])


# Adicionar a chave SSH para liberar acesso ao servidor Git
os.system('eval "$(ssh-agent -s)" && ssh-add ~/.ssh/==CHAVE_SSH==')
# Coleta a hora da coleta
hora = datetime.datetime.now()
hora_inicio = datetime.datetime.now()
print(hora_inicio)
# Diretório configurado para o Git (arquivos serão salvos aqui)
repo_path = os.getcwd()
repo_path = os.path.abspath(os.path.join(repo_path, os.pardir))
repo_path = repo_path + '/Backup_ativos'
# Atualizando repositótio Git local
g = git.cmd.Git(repo_path)
g.pull()

# Configurações de log
log_dir = repo_path + '/LOG'
logfile = log_dir + '/' + 'Backup_ativos_' + str(hora.strftime("%Y-%m-%d") + '.txt')
# Caso não exista, cria o diretório de log
if not os.path.exists(log_dir):
    os.makedirs(log_dir)
# Configuração do log
logging.basicConfig(filename=logfile,
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    level=logging.WARN)

logging.warning("============ Iniciando backup ============")

# Lista todos os sites cadastrados no CMDB
sites = cmdb_rest.list_all_sites()
for site in sites:
    # Função para coletar os dados dos switches a partir de ativos cadastrados no CMDB
    coletar_dados_ativos(cmdb_rest.list_device_todos_role_id_por_site(str(site['id'])), site)


# Coleta a hora de término da coleta para registro no Git
hora = datetime.datetime.now()
delta = hora - hora_inicio
print(f"O script demorou {delta} segundos para finalizar")
# Mensagem a ser gravada no commit do Git
comm_mensgem = 'Commit de todos os sites. Data: ' + str(hora.strftime("%d-%m-%Y %H:%M"))
# Atualiza repositório remoto
update = update_git(comm_mensgem)
