import os
import datetime
import logging
import sys

# Importando bibliotecas para o multithreading
import concurrent.futures

# Importando templates TTP
from Switch.TTP_TEMPLATES.Aruba_2530 import *

# Importando modulo para manipulação de IPs
import ipaddress

# Importando modulos do Netmiko
from netmiko import Netmiko
from netmiko import NetMikoAuthenticationException, NetMikoTimeoutException, ReadTimeout

# Importando script customizado
from Switch import reutil
from CMDB import cmdb_rest


def conectar_sw(ip, poe):
    retorno = ''
    # Conecta ao IP do ativo e consulta os dados informados
    device_dict = {
        'host': ip,
        'username': 'admin',
        'password': '==senha==',
        'device_type': 'hp_procurve',
    }
    # Verifica se o dispositivo esta online
    response = os.system("ping -c 1 " + ip + "> /dev/null")
    if response != 0:
        retorno += ip + " - OFFLINE"
        logging.warning(f"FALHA,OFFLINE,{ip}")
        erro_zabbix = "zabbix_sender -z ==ENDERECO_IP_ZABBIX== -s Projeto_Switch_Netbox -k Trap_Erros_Telemetria -o \"" + ip + " - LOGIN - OFFLINE\""
        os.system(erro_zabbix)
        return retorno
    # Conecta ao equipamento
    try:
        net_connect = Netmiko(**device_dict)
    except NetMikoTimeoutException:
        retorno += ip + " - ERRO AO CONECTAR - TIMEOUT"
        logging.warning(f"FALHA,ERRO AO CONECTAR - TIMEOUT,{ip}")
        erro_zabbix = "zabbix_sender -z ==ENDERECO_IP_ZABBIX== -s Projeto_Switch_Netbox -k Trap_Erros_Telemetria -o \"" + ip + " - LOGIN  - ERRO AO CONECTAR - TIMEOUT\""
        os.system(erro_zabbix)
        return retorno
    except NetMikoAuthenticationException:
        retorno += ip + " - ERRO AO CONECTAR - AUTENTICACAO"
        logging.warning(f"FALHA,ERRO AO CONECTAR - AUTENTICACAO,{ip}")
        erro_zabbix = "zabbix_sender -z ==ENDERECO_IP_ZABBIX== -s Projeto_Switch_Netbox -k Trap_Erros_Telemetria -o \"" + ip + " - LOGIN  - ERRO AO CONECTAR - AUTENTICACAO\""
        os.system(erro_zabbix)
        return retorno
    except Exception:
        retorno += ip + " - ERRO AO CONECTAR - DIVERSOS"
        logging.warning(f"FALHA,ERRO AO CONECTAR - DIVERSOS,{ip}")
        erro_zabbix = "zabbix_sender -z ==ENDERECO_IP_ZABBIX== -s Projeto_Switch_Netbox -k Trap_Erros_Telemetria -o \"" + ip + " - LOGIN  - ERRO AO CONECTAR - DIVERSOS\""
        os.system(erro_zabbix)
        return retorno
    # Coleta o prompt do ativo
    prompt = net_connect.find_prompt()
    # Verificar o status da CPU do ativo
    retorno += ttp_show_cpu(net_connect, ip)
    # Verificar o status da memória do ativo
    retorno += ttp_show_memoria(net_connect, ip)
    # Verificar o status das fans do ativo
    retorno += ttp_show_fans(net_connect, ip)
    # Verifica o status do PoE caso a variável seja verdadeira
    if poe == True:
        retorno += ttp_show_power_over_ethernet(net_connect, ip)
    return retorno


def valida_ativo(dev):
    if dev['device_role']['id'] == 4 or dev['device_role']['id'] == 5 or dev['device_role']['id'] == 6 or dev['device_role']['id'] == 7:
        # Caso o ativo não possua endereço Ipv4 cadastrado no CMDB, ignorar
        if dev['primary_ip4']['address'] == None:
            return
        # Verifica se o ativo é PoE
        if dev['device_type']['id'] == 26 or dev['device_type']['id'] == 96:
            ativo_poe = True
        else:
            ativo_poe = False
        # Identidca os ativos Aruba 2530 pelo device_type
        if dev['device_type']['id'] == 25 or dev['device_type']['id'] == 26 or dev['device_type']['id'] == 27 or dev['device_type']['id'] == 96:
            # Conecta ao equipamento
            retorno_valida = dev['primary_ip4']['address'][:-3]
            retorno_valida += '\n' + dev['name'] + '\n'
            retorno_valida += conectar_sw(dev['primary_ip4']['address'][:-3], ativo_poe)
            retorno_valida += '\n' + '-' * 40
            print(retorno_valida)
    return


def lista_ativos(devic):
        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
            futures = [executor.submit(valida_ativo, devi) for devi in devic]


def main(x):
    # Usuário deve informar o IP ou site ID do CMDB
    print('PROGRAMA PARA VERIFICAR A TELEMETRIA NOS ATIVOS ARUBA 2530')
    # Variável de controle
    var_controle = 0
    # Verifica se o digitado é um site no CMDB
    if x == 'GERAL':
        print('VERIFICANDO EM TODOS OS ATIVOS ARUBA 2530 com IPv4 do CMDB')
        var_controle = 100
    if len(x) == 4 and x.isdigit():
        print('Formato do CMDB VALIDADO')
        var_controle = 1
    # Verifica se o digitado é um IP
    try:
        if ipaddress.ip_address(x) != True:
            print('IP VALIDADO')
            ip = x
            var_controle = 10
            entrada_poe = False
    except Exception:
        ip = 0
    if var_controle == 0:
        print("Erro - CMDB/IP COM FORMATO INVÁLIDO, inserir novamente \n")
        print("SAINDO DO PROGRAMA")
        exit()

    # Configurações de log
    log_dir = os.getcwd()
    log_dir = os.path.abspath(os.path.join(log_dir, os.pardir))
    log_dir = log_dir + '/Switch/LOG'
    hora = datetime.datetime.now()
    logfile = log_dir + '/' + 'Aruba_2530_verif_telemetria_' + str(hora.strftime("%Y-%m-%d") + '.csv')
    # Caso não exista, cria o diretório de log
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    # Arquivo de log de execução
    if not os.path.exists(logfile):
        with open(logfile, mode='w', newline='') as file:
            file.write("DATA,HORA,STATUS,MENSAGEM,IP\n")
            file.close()
    # Configuração do log
    logging.basicConfig(filename=logfile,
                        filemode='a',
                        datefmt='%Y/%m/%d,%I:%M:%S',
                        format='%(asctime)s,%(message)s',
                        level=logging.WARN)

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
            print(f"Iniciando a verificação da telemetria nos ativos Aruba 2530 do site: {site['name']}, ID: {site['id']}")
            print('=' * 60)
            # Lista os ativos cadastrados
            devices = cmdb_rest.list_device_todos_role_id_por_site(str(site['id']))
            # Cicla pelos ativos via multithread
            lista_ativos(devices)
    if var_controle == 10:
        print(f"Iniciando a verificação da telemetria no ativo: {ip}")
        conectar_sw(ip, entrada_poe)
    if var_controle == 1:
        # Lista todos os sites cadastrados no CMDB
        sites = cmdb_rest.list_all_sites()
        for site in sites:
            # Descanrtando os sites STI-DC e STI - ESTOQUE
            if site['id'] == 206 or site['id'] == 108:
                break
            if site['id'] == int(x):
                print(f"Iniciando a verificação da telemetria nos ativos Aruba 2530 do site: {site['name']}, ID: {site['id']}")
                print('-' * 40)
                # Lista os ativos cadastrados
                devices = cmdb_rest.list_device_todos_role_id_por_site(str(site['id']))
                # Cicla pelos ativos via multithread
                lista_ativos(devices)
                break
        else:
            print(f"ERRO: O SITE INDICADO NÃO EXISTE NO CMDB: {x}")

    hora_final = datetime.datetime.now()
    delta = hora_final - hora
    print(f"O programa demorou {delta} segundos para finalizar")


if __name__ == "__main__":
    main(sys.argv[1])  # Passando os argumentos do Python
