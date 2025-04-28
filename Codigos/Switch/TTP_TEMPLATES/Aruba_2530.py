from ttp import ttp
import re
import logging
import os

# importa arquivo de atualização de configurações
from . import config_ar2530

# CPU
# show cpu 300
ttp_cpu_10sec = "{{cpu_10_sec}}/100 busy, for past 10 sec"
ttp_cpu_60sec = "{{cpu_60_sec}}/100 busy, for past 60 sec"
ttp_cpu_300sec = "{{cpu_300_sec}}/100 busy, for past 300 sec"
def ttp_show_cpu(net_connect, dev):
    # variável de retorno
    texto = ''
    cont_erros = 0
    # Templates TTP
    # Aplicando o template a resposta do ativo
    parser = ttp(data=net_connect.send_command("show cpu 300"), template=ttp_cpu_300sec)
    parser.parse()
    res = parser.result()
    # Gera um alarme caso o uso de CPU seja maior que 70%
    try:
        if int(res[0][0]['cpu_300_sec']) > 70:
            texto += "ALTO uso de CPU (300sec). IP: " + dev + ", valor: " + res[0][0]['cpu_300_sec'] + "%.\n"
            logging.warning(f"FALHA,ALTO uso de CPU (300sec). Valor: {res[0][0]['cpu_300_sec']}%,{dev}")
            erro_zabbix = "zabbix_sender -z ==ENDERECO_IP_ZABBIX== -s Projeto_Switch_Netbox -k Trap_Erros_Telemetria -o \"" + dev + " - ALTO uso de CPU (300sec). Valor: " + str(res[0][0]['cpu_300_sec']) + "\""
            os.system(erro_zabbix)
            cont_erros += 1
    except Exception:
        texto += "ERRO ao coletar comando CPU (300sec). IP: " + dev + "%.\n"
        logging.warning(f"FALHA,ERRO ao coletar comando CPU (300sec),{dev}")
        erro_zabbix = "zabbix_sender -z ==ENDERECO_IP_ZABBIX== -s Projeto_Switch_Netbox -k Trap_Erros_Telemetria -o \"" + dev + " - ERRO ao coletar comando CPU (300sec)\""
        os.system(erro_zabbix)
        cont_erros += 1
    parser = ttp(data=net_connect.send_command("show cpu 60"), template=ttp_cpu_60sec)
    parser.parse()
    res = parser.result()
    # Gera um alarme caso o uso de CPU seja maior que 70%
    try:
        if int(res[0][0]['cpu_60_sec']) > 70:
            texto += "ALTO uso de CPU (60sec). IP: " + dev + ", valor: " + res[0][0]['cpu_60_sec'] + "%.\n"
            logging.warning(f"FALHA,ALTO uso de CPU (60sec). Valor: {res[0][0]['cpu_60_sec']}%,{dev}")
            erro_zabbix = "zabbix_sender -z ==ENDERECO_IP_ZABBIX== -s Projeto_Switch_Netbox -k Trap_Erros_Telemetria -o \"" + dev + " - ALTO uso de CPU (60sec). Valor: " + str(res[0][0]['cpu_60_sec']) + "\""
            os.system(erro_zabbix)
            cont_erros += 1
    except Exception:
        texto += "ERRO ao coletar comando CPU (60sec). IP: " + dev + "%.\n"
        logging.warning(f"FALHA,ERRO ao coletar comando CPU (60sec),{dev}")
        erro_zabbix = "zabbix_sender -z ==ENDERECO_IP_ZABBIX== -s Projeto_Switch_Netbox -k Trap_Erros_Telemetria -o \"" + dev + " - ERRO ao coletar comando CPU (60sec)\""
        os.system(erro_zabbix)
        cont_erros += 1
    parser = ttp(data=net_connect.send_command("show cpu 10"), template=ttp_cpu_10sec)
    parser.parse()
    res = parser.result()
    # Gera um alarme caso o uso de CPU seja maior que 70%
    try:
        if int(res[0][0]['cpu_10_sec']) > 70:
            texto += "ALTO uso de CPU (10sec). IP: " + dev + ", valor: " + res[0][0]['cpu_10_sec'] + "%.\n"
            logging.warning(f"FALHA,ALTO uso de CPU (10sec). Valor: {res[0][0]['cpu_10_sec']}%,{dev}")
            erro_zabbix = "zabbix_sender -z ==ENDERECO_IP_ZABBIX== -s Projeto_Switch_Netbox -k Trap_Erros_Telemetria -o \"" + dev + " - ALTO uso de CPU (10sec). Valor: " + str(res[0][0]['cpu_10_sec']) + "\""
            os.system(erro_zabbix)
            cont_erros += 1
    except Exception:
        texto += "ERRO ao coletar comando CPU (10sec). IP: " + dev['primary_ip4']['address'][:-3] + "%.\n"
        logging.warning(f"FALHA,ERRO ao coletar comando CPU (10sec),{dev}")
        erro_zabbix = "zabbix_sender -z ==ENDERECO_IP_ZABBIX== -s Projeto_Switch_Netbox -k Trap_Erros_Telemetria -o \"" + dev + " - ERRO ao coletar comando CPU (10sec)\""
        os.system(erro_zabbix)
        cont_erros += 1
    # Imprime mensagem de sucesso caso não tenha encontrado nenhum erro
    if cont_erros == 0:
        logging.warning(f"SUCESSO,Uso de CPU dentro do normal,{dev}")
    return texto


# MEMORIA
# show system information
ttp_system_info = """
  System Name        : {{sysname}}
  System Contact     : {{system_contact}}
  System Location    : {{system_location}}

  MAC Age Time (sec) : {{mac_age}}

  Time Zone          : {{timezone}}
  Daylight Time Rule : {{timezone_daylight}}

  Software revision  : {{firmware}}        Base MAC Addr      : {{mac_add}}
  ROM Version        : {{versao_rom}}             Serial Number      : {{serial}}

  Up Time            : {{uptime | ORPHRASE}}              Memory   - Total   : {{memoria_total}}
  CPU Util (%)       : 18                              Free    : {{memoria_livre}}

  IP Mgmt  - Pkts Rx : {{ip_mgmt_packets_recebidos}}              Packet   - Total   : {{packet_buffers_total}}
             Pkts Tx : {{ip_mgmt_packets_transmitidos}}              Buffers    Free    : {{packet_buffers_livre}}
                                                       Lowest  : {{packet_buffers_minimo}}
                                                       Missed  : {{packet_buffers_perdido}}
"""
def ttp_show_memoria(net_connect, dev):
    # variável de retorno
    texto = ''
    cont_erros = 0
    cont_erros_fw = 0
    # Templates TTP
    # Acima da função
    # Aplicando o template a resposta do ativo
    parser = ttp(data=net_connect.send_command("show system information"), template=ttp_system_info)
    parser.parse()
    res = parser.result()
    # Gera um alarme caso o uso de memória seja maior que 70%
    uso_mem = (int(res[0][0]['memoria_livre'].replace(",", "")) / int(res[0][0]['memoria_total'].replace(",", "")))*100
    try:
        if  uso_mem > 70:
            texto += "ALTO uso de memória. IP: " + dev + ", valor: " + uso_mem + "%.\n"
            logging.warning(f"FALHA,ALTO uso de memória. Valor: {uso_mem}%,{dev}")
            erro_zabbix = "zabbix_sender -z ==ENDERECO_IP_ZABBIX== -s Projeto_Switch_Netbox -k Trap_Erros_Telemetria -o \"" + dev + " - ALTO uso de memória. Valor: " + str(uso_mem) + "\""
            os.system(erro_zabbix)
            cont_erros += 1
    except Exception:
        texto += "ERRO ao coletar comando memória. IP: " + dev + ".\n"
        logging.warning(f"FALHA,ERRO ao coletar comando memória,{dev}")
        erro_zabbix = "zabbix_sender -z ==ENDERECO_IP_ZABBIX== -s Projeto_Switch_Netbox -k Trap_Erros_Telemetria -o \"" + dev + "  - ERRO ao coletar comando memória\""
        os.system(erro_zabbix)
        cont_erros += 1
    try:
        if res[0][0]['firmware'][:-5] != 'YA.16.11' or res[0][0]['firmware'][:-5] != 'WC.16.11':
            texto += "FIRMWARE desatualizado. IP: " + dev + ", Firmware: " + res[0][0]['firmware'] + ".\n"
            logging.warning(f"FALHA,FIRMWARE desatualizado. Firmware: {res[0][0]['firmware']},{dev}")
            erro_zabbix = "zabbix_sender -z ==ENDERECO_IP_ZABBIX== -s Projeto_Switch_Netbox -k Trap_Erros_Telemetria -o \"" + dev + " - FIRMWARE desatualizado. Firmware: " + res[0][0]['firmware'] + "\""
            os.system(erro_zabbix)
            cont_erros_fw += 1
    except Exception:
            texto += "FALHA ao coletar modelo firmware. IP: " + dev + ".\n"
            logging.warning(f"FALHA ao coletar modelo firmware,{dev}")
            erro_zabbix = "zabbix_sender -z ==ENDERECO_IP_ZABBIX== -s Projeto_Switch_Netbox -k Trap_Erros_Telemetria -o \"" + dev + " - FALHA ao coletar o firmware\""
            os.system(erro_zabbix)
            cont_erros_fw += 1
    # Imprime mensagem de sucesso caso não tenha encontrado nenhum erro
    if cont_erros == 0:
        logging.warning(f"SUCESSO,Uso de memória dentro do normal,{dev}")
    if cont_erros_fw == 0:
        logging.warning(f"SUCESSO,Firmware atualizado,{dev}")
    return texto


# FANS
# show system fans
ttp_falha_fans = """
{{fans_falha}} / {{fans_total}} Fans in Failure State
{{fans_falha_historico}} / {{fans_total}} Fans have been in Failure State
"""
def ttp_show_fans(net_connect, dev):
    # variável de retorno
    texto = ''
    cont_erros = 0
    # Templates TTP
    # Acima da função
    # Aplicando o template a resposta do ativo
    parser = ttp(data=net_connect.send_command("show system fans"), template=ttp_falha_fans, log_level='CRITICAL')
    parser.parse()
    res = parser.result()
    # Gera um alarme em caso de falha nas fans
    try:
        if int(res[0][0]['fans_falha']) > 0:
            texto += "FAN com defeito. IP: " + dev + ", valor: " + (res[0][0]['fans_falha']/res[0][0]['fans_total']) + ".\n"
            logging.warning(f"FALHA,FAN com defeito. Valor: {res[0][0]['fans_falha']}/{res[0][0]['fans_total']},{dev}")
            erro_zabbix = "zabbix_sender -z ==ENDERECO_IP_ZABBIX== -s Projeto_Switch_Netbox -k Trap_Erros_Telemetria -o \"" + dev + " - FALHA FAN com defeito. Valor: " + str(res[0][0]['fans_falha']) + "/" + str(res[0][0]['fans_total']) + "\""
            os.system(erro_zabbix)
            cont_erros += 1
    except Exception:
            texto += "FALHA ao coletar dados FANS. IP: " + dev + ".\n"
            logging.warning(f"FALHA,ERRO ao coletar dados FANS,{dev}")
            erro_zabbix = "zabbix_sender -z ==ENDERECO_IP_ZABBIX== -s Projeto_Switch_Netbox -k Trap_Erros_Telemetria -o \"" + dev + " - ERRO ao coletar dados FANS\""
            os.system(erro_zabbix)
            cont_erros += 1
    try:
        if int(res[0][0]['fans_falha']) > 0:
            texto += "FAN com histórico de defeito. IP: " + dev + ", valor: " + (res[0][0]['fans_falha_historico']/res[0][0]['fans_total']) + ".\n"
            logging.warning(f"FALHA,FAN com histórico de defeito. Valor: {res[0][0]['fans_falha_historico']}/{res[0][0]['fans_total']},{dev}")
            erro_zabbix = "zabbix_sender -z ==ENDERECO_IP_ZABBIX== -s Projeto_Switch_Netbox -k Trap_Erros_Telemetria -o \"" + dev + " - FALHA FAN com histórico de defeito. Valor: " + str(res[0][0]['fans_falha_historico']) + "/" + str(res[0][0]['fans_total']) + "\""
            os.system(erro_zabbix)
            cont_erros += 1
    except Exception:
            texto += "FALHA,ERRO ao coletar histórico FANS. IP: " + dev + ".\n"
            logging.warning(f"FALHA,ERRO ao coletar histórico FANS,{dev}")
            erro_zabbix = "zabbix_sender -z ==ENDERECO_IP_ZABBIX== -s Projeto_Switch_Netbox -k Trap_Erros_Telemetria -o \"" + dev + " - ERRO ao coletar histórico das FANS\""
            os.system(erro_zabbix)
            cont_erros += 1
    # Imprime mensagem de sucesso caso não tenha encontrado nenhum erro
    if cont_erros == 0:
        logging.warning(f"SUCESSO,Fans operando dentro do normal,{dev}")
    return texto


# PoE
# show power-over-ethernet
ttp_poe = """
  Operational Status     : {{poe_estado}}
  Total Available Power  :  {{poe_potencia_total}} W
  Total Power Drawn      :   {{poe_potencia_utilizada}} W +/- 6W
  Total Power Reserved   :   {{poe_potencia_reservada}} W
  Total Remaining Power  :  {{poe_potencia_disponivel}} W
  """
def ttp_show_power_over_ethernet(net_connect, dev):
    # variável de retorno
    texto = ''
    cont_erros = 0
    # Templates TTP
    # Acima da função
    # Aplicando o template a resposta do ativo
    parser = ttp(data=net_connect.send_command("show power-over-ethernet"), template=ttp_poe)
    parser.parse()
    res = parser.result()
    # Gera um alarme caso a potência utilizada seja maior que 70%
    try:
        uso_poe = (int(res[0][0]['poe_potencia_utilizada']) / int(res[0][0]['poe_potencia_total']))*100
    except Exception:
            texto += "DADOS SOBRE O PoE NÃO conseguiram ser coletados. IP: " + dev + ".\n"
            logging.warning(f"FALHA,DADOS SOBRE O PoE NÃO conseguiram ser coletados,{dev}")
            erro_zabbix = "zabbix_sender -z ==ENDERECO_IP_ZABBIX== -s Projeto_Switch_Netbox -k Trap_Erros_Telemetria -o \"" + dev + " - ERRO ao coletar dados do PoE\""
            os.system(erro_zabbix)
            cont_erros += 1
            return texto
    try:
        if  uso_poe > 80:
            texto += "ALTO uso de PoE. IP: " + dev + ", valor: " + uso_poe + "%.\n"
            logging.warning(f"FALHA,ALTO uso de PoE. Valor: {uso_poe}%,{dev}")
            erro_zabbix = "zabbix_sender -z ==ENDERECO_IP_ZABBIX== -s Projeto_Switch_Netbox -k Trap_Erros_Telemetria -o \"" + dev + " - ALTO uso de PoE. Valor: " + str(uso_poe) + "\""
            os.system(erro_zabbix)
            cont_erros += 1
    except Exception:
            texto += "ERRO ao coletar dados PoE. IP: " + dev + ".\n"
            logging.warning(f"FALHA,ERRO ao coletar dados PoE,{dev}")
            erro_zabbix = "zabbix_sender -z ==ENDERECO_IP_ZABBIX== -s Projeto_Switch_Netbox -k Trap_Erros_Telemetria -o \"" + dev + " - ERRO ao coletar dados PoE\""
            os.system(erro_zabbix)
            cont_erros += 1
    try:
        if res[0][0]['poe_estado'] != 'On':
            texto += "ERRO no PoE. IP: " + dev + ", estado operacional: " + res[0][0]['poe_estado'] + "%.\n"
            logging.warning(f"FALHA,ERRO no PoE. Estado operacional: {res[0][0]['poe_estado']}%,{dev}")
            erro_zabbix = "zabbix_sender -z ==ENDERECO_IP_ZABBIX== -s Projeto_Switch_Netbox -k Trap_Erros_Telemetria -o \"" + dev + " - ERRO no PoE. Estado operacional: " + str(res[0][0]['poe_estado']) + "\""
            os.system(erro_zabbix)
            cont_erros += 1
    except Exception:
            texto += "ERRO ao coletar estado PoE. IP: " + dev + ".\n"
            logging.warning("FALHA,ERRO ao coletar estado PoE,{dev}")
            erro_zabbix = "zabbix_sender -z ==ENDERECO_IP_ZABBIX== -s Projeto_Switch_Netbox -k Trap_Erros_Telemetria -o \"" + dev + " - ERRO ao coletar coletar do PoE\""
            os.system(erro_zabbix)
            cont_erros += 1
    # Imprime mensagem de sucesso caso não tenha encontrado nenhum erro
    if cont_erros == 0:
        logging.warning(f"SUCESSO,Uso do PoE dentro do normal,{dev}")
    return texto


# STP
# show spanning-tree
# show running-config interface
ttp_stp = """
  STP Enabled   : {{stp_enale}}
  Force Version : {{stp_versao}}
  IST Mapped VLANs : {{stp_vlans_mapeadas}}
  Switch MAC Address : {{stp_mac_add}}
  Switch Priority    : {{stp_prioridade}}
  Max Age  : {{stp_max_age}}
  Max Hops : {{stp_max_hops}}
  Forward Delay : {{stp_forward_delay}}

  Topology Change Count  : {{stp_quant_mudancas_topologia}}
  Time Since Last Change : {{stp_ultima_mudanca_topologia | ORPHRASE}}

  CST Root MAC Address : {{stp_root_mac_add}}
  CST Root Priority    : {{stp_root_prioridade}}
  CST Root Port        : {{stp_root_port | ORPHRASE}}
"""
def ttp_show_spanning_tree(net_connect, dev, log_ex, log_dat):
    # variável de retorno
    texto = ''
    cont_erros = 0
    cont_erro_update = 0
    # Templates TTP
    # Acima da função
    # Aplicando o template a resposta do ativo
    parser = ttp(data=net_connect.send_command("show spanning-tree"), template=ttp_stp, log_level='CRITICAL')
    parser.parse()
    res = parser.result()
    # Gera um alarme em caso de falha na configuração
    try:
        a = res[0][0]['stp_enale']
    except Exception:
        texto += "DADOS SOBRE O STP NÃO conseguiram ser coletados: " + dev + ".\n"
        log_ex.warning(f"FALHA,DADOS SOBRE O STP NÃO conseguiram ser coletados,{dev}")
        log_dat.warning(f"FALHA,DADOS SOBRE O STP NÃO conseguiram ser coletados,,{dev}")
        erro_zabbix = "zabbix_sender -z ==ENDERECO_IP_ZABBIX== -s Projeto_Switch_Netbox -k Trap_Erros_Spanning_Tree -o \"" + dev + " - ERRO ao coletar dados do STP\""
        os.system(erro_zabbix)
        cont_erros += 1
        return texto
    if res[0][0]['stp_enale'] == 'Yes':
        try:
            if res[0][0]['stp_versao'] != 'RSTP-operation':
                texto += "STP com versão incorreta. IP: " + dev + ".\n"
                log_ex.warning(f"FALHA,STP com versão incorreta,{dev}")
                log_dat.warning(f"FALHA,STP com versão incorreta,,{dev}")
                erro_zabbix = "zabbix_sender -z ==ENDERECO_IP_ZABBIX== -s Projeto_Switch_Netbox -k Trap_Erros_Spanning_Tree -o \"" + dev + " - STP com versão incorreta\""
                os.system(erro_zabbix)
                cont_erros += 1
                cont_erro_update += 1
        except Exception:
            texto += "ERRO ao coletar versão do STP. IP: " + dev + ".\n"
            log_ex.warning(f"FALHA,ERRO ao coletar versão do STP,{dev}")
            log_dat.warning(f"FALHA,ERRO ao coletar versão do STP,,{dev}")
            erro_zabbix = "zabbix_sender -z ==ENDERECO_IP_ZABBIX== -s Projeto_Switch_Netbox -k Trap_Erros_Spanning_Tree -o \"" + dev + " - ERRO ao coletar versão do STP\""
            os.system(erro_zabbix)
            cont_erros += 1
        try:
            if res[0][0]['stp_vlans_mapeadas'] != '1-4094':
                texto += "STP sem todas vlans mapeadas. IP: " + dev + ".\n"
                log_ex.warning(f"FALHA,STP sem todas vlans mapeadas,{dev}")
                log_dat.warning(f"FALHA,STP sem todas vlans mapeadas,,{dev}")
                erro_zabbix = "zabbix_sender -z ==ENDERECO_IP_ZABBIX== -s Projeto_Switch_Netbox -k Trap_Erros_Spanning_Tree -o \"" + dev + " - STP sem todas vlans mapeadas\""
                os.system(erro_zabbix)
                cont_erros += 1
                cont_erro_update += 1
        except Exception:
            texto += "ERRO ao coletar vlans mapeadas STP. IP: " + dev + ".\n"
            log_ex.warning(f"FALHA,ERRO ao coletar vlans mapeadas STP,{dev}")
            log_dat.warning(f"FALHA,ERRO ao coletar vlans mapeadas STP,,{dev}")
            erro_zabbix = "zabbix_sender -z ==ENDERECO_IP_ZABBIX== -s Projeto_Switch_Netbox -k Trap_Erros_Spanning_Tree -o \"" + dev + " - ERRO ao coletar vlans mapeadas\""
            os.system(erro_zabbix)
            cont_erros += 1
        try:
            if res[0][0]['stp_prioridade'] != '32768':
                texto += "STP com a prioridade incorreta. IP: " + dev + ".\n"
                log_ex.warning(f"FALHA,STP com a prioridade incorreta,{dev}")
                log_dat.warning(f"FALHA,STP com a prioridade incorreta,,{dev}")
                erro_zabbix = "zabbix_sender -z ==ENDERECO_IP_ZABBIX== -s Projeto_Switch_Netbox -k Trap_Erros_Spanning_Tree -o \"" + dev + " - STP com a prioridade incorreta\""
                os.system(erro_zabbix)
                cont_erros += 1
                cont_erro_update += 1
        except Exception:
            texto += "ERRO ao coletar prioridade STP. IP: " + dev + ".\n"
            log_ex.warning(f"FALHA,ERRO ao coletar prioridade STP,{dev}")
            log_dat.warning(f"FALHA,ERRO ao coletar prioridade STP,,{dev}")
            erro_zabbix = "zabbix_sender -z ==ENDERECO_IP_ZABBIX== -s Projeto_Switch_Netbox -k Trap_Erros_Spanning_Tree -o \"" + dev + " - ERRO ao coletar prioridade STP\""
            os.system(erro_zabbix)
            cont_erros += 1
        try:
            if res[0][0]['stp_root_prioridade'] != '4096':
                texto += "STP com a prioridade do ROOT incorreta. IP: " + dev + ".\n"
                log_ex.warning(f"FALHA,STP com a prioridade do ROOT incorreta,{dev}")
                log_dat.warning(f"FALHA,STP com a prioridade do ROOT incorreta,,{dev}")
                erro_zabbix = "zabbix_sender -z ==ENDERECO_IP_ZABBIX== -s Projeto_Switch_Netbox -k Trap_Erros_Spanning_Tree -o \"" + dev + " - STP com a prioridade do ROOT incorreta\""
                os.system(erro_zabbix)
                cont_erros += 1
        except Exception:
            texto += "ERRO ao coletar prioridade do root do STP. IP: " + dev + ".\n"
            log_ex.warning(f"FALHA,ERRO ao coletar prioridade do root do STP,{dev}")
            log_dat.warning(f"FALHA,ERRO ao coletar prioridade do root do STP,,{dev}")
            erro_zabbix = "zabbix_sender -z ==ENDERECO_IP_ZABBIX== -s Projeto_Switch_Netbox -k Trap_Erros_Spanning_Tree -o \"" + dev + " - ERRO ao coletar prioridade do root do STP\""
            os.system(erro_zabbix)
            cont_erros += 1
    else:
        texto += "STP desabilitado. IP: " + dev + ".\n"
        log_ex.warning(f"FALHA,STP desabilitado,{dev}")
        log_dat.warning(f"FALHA,STP desabilitado,,{dev}")
        erro_zabbix = "zabbix_sender -z ==ENDERECO_IP_ZABBIX== -s Projeto_Switch_Netbox -k Trap_Erros_Spanning_Tree -o \"" + dev + " - STP desabilitado\""
        os.system(erro_zabbix)
        cont_erros += 1
        cont_erro_update += 1
    # Encontrando a porta de UPLINK e validando com a porta do ROOT do STP
    interfaces = net_connect.send_command("show running-config interface")
    # Encontrando a porta de UPLINK
    # Dividir a configuração por blocos de interface
    interfaces = interfaces.strip().split("interface ")    
    # Armazenar interfaces de uplink
    uplinks = []
    # Processar cada bloco
    for bloco in interfaces:
        if bloco.strip():  # Ignorar linhas vazias
            linhas = bloco.strip().split("\n")
            nome_interface = linhas[0].strip()  # Nome da interface
            # Verificar UPLINK na string'
            if any("UPLINK" in linha.upper() for linha in linhas):
                uplinks.append(nome_interface)
    # Verifica se mais de uma porta está identificada como UPLINK
    if len(uplinks) > 1:
        texto += "STP MAIS DE UMA PORTA IDENTIFICADA COMO UPLINK. IP: " + dev + ", Portas: " + uplinks + ".\n"
        log_ex.warning(f"FALHA,STP MAIS DE UMA PORTA IDENTIFICADA COMO UPLINK. Portas: {str(uplinks)},{dev}")
        log_dat.warning(f"FALHA,STP MAIS DE UMA PORTA IDENTIFICADA COMO UPLINK,{str(uplinks)},{dev}")
        erro_zabbix = "zabbix_sender -z ==ENDERECO_IP_ZABBIX== -s Projeto_Switch_Netbox -k Trap_Erros_Spanning_Tree -o \"" + dev + " - MAIS DE UMA PORTA IDENTIFICADA COMO UPLINK\""
        os.system(erro_zabbix)
        cont_erros += 1
        return texto
    # Verifica se nenhuma porta está identificada como UPLINK
    if len(uplinks) ==0:
        texto += "STP NENHUMA PORTA IDENTIFICADA COMO UPLINK. IP: " + dev + ".\n"
        log_ex.warning(f"FALHA,STP NENHUMA PORTA IDENTIFICADA COMO UPLINK,{dev}")
        log_dat.warning(f"FALHA,STP NENHUMA PORTA IDENTIFICADA COMO UPLINK,,{dev}")
        erro_zabbix = "zabbix_sender -z ==ENDERECO_IP_ZABBIX== -s Projeto_Switch_Netbox -k Trap_Erros_Spanning_Tree -o \"" + dev + " - NENHUMA PORTA IDENTIFICADA COMO UPLINK\""
        os.system(erro_zabbix)
        cont_erros += 1
        return texto
    # Valida uplink com root
    if str(uplinks[0]) != str(res[0][0]['stp_root_port']):
        texto += "STP INTERFACE DO ROOT DIFERENTE DO UPLINK. IP: " + dev + ", ROOT do STP: " + res[0][0]['stp_root_port'] + ", UPLINK: " + uplinks[0] + ".\n"
        log_ex.warning(f"FALHA,STP INTERFACE DO ROOT DIFERENTE DO UPLINK. ROOT do STP: {res[0][0]['stp_root_port']}. UPLINK: {uplinks[0]},{dev}")
        log_dat.warning(f"FALHA,STP INTERFACE DO ROOT DIFERENTE DO UPLINK,ROOT do STP: {res[0][0]['stp_root_port']}. UPLINK: {uplinks[0]},{dev}")
        erro_zabbix = "zabbix_sender -z ==ENDERECO_IP_ZABBIX== -s Projeto_Switch_Netbox -k Trap_Erros_Spanning_Tree -o \"" + dev + " - STP INTERFACE DO ROOT DIFERENTE DO UPLINK\""
        os.system(erro_zabbix)
        cont_erros += 1
    # Atualiza a configuração caso tenha encontrado erros de configuração
    if cont_erro_update > 0:
        config_ar2530.update_stp(net_connect, dev, log_ex, log_dat)
    # Imprime mensagem de sucesso caso não tenha encontrado nenhum erro
    if cont_erros == 0:
        log_ex.warning(f"SUCESSO,STP configurado corretamente,{dev}")
        log_dat.warning(f"SUCESSO,STP configurado corretamente,,{dev}")
    return texto


# DHCP-SNOOPING v4
# show dhcp-snooping
# show dhcp-snooping stats
# show dhcp-snooping binding
ttp_dhcp_sn_v4 = """
  DHCP Snooping              : {{dhcp_sn_v4_status}}
  Enabled VLANs              : {{dhcp_sn_v4_vlans}}
  Verify MAC address         : {{dhcp_sn_v4_verify_mac}}
  Option 82 untrusted policy : {{dhcp_sn_v4_op_82}}
  Option 82 insertion        : {{dhcp_sn_v4_op_82_insert}}
  Store lease database       : {{dhcp_sn_v4_store_lease | ORPHRASE}}
"""
ttp_dhcp_sn_v4_stats = """
 server       forward  from trusted port              {{dhcp_sn_v4_packets_received_trusted_port}}
 client       forward  to trusted port                {{dhcp_sn_v4_packets_sent_to_trusted_port}}
 server       drop     received on untrusted port     {{dhcp_sn_v4_packets_reveived_untrusted_port}}
 server       drop     unauthorized server            {{dhcp_sn_v4_packets_drop_unaut_server}}
 client       drop     destination on untrusted port  {{dhcp_sn_v4_destination_untrusted_port}}
 client       drop     untrusted option 82 field      {{dhcp_sn_v4_untrustes_op_82}}
 client       drop     bad DHCP release request       {{dhcp_sn_v4_bad_dhcp_release}}
 client       drop     failed verify MAC check        {{dhcp_sn_v4_failed_mac_check}}
 client       drop     failed on max-binding limit    {{dhcp_sn_v4_max_bind}}
 """
def dhcp_v4_snoop(net_connect, dev, log_ex, log_dat):
    # Variável de retorno
    texto = ''
    cont_erros = 0
    cont_reset = 0
    cont_erro_update = 0
    # Templates TTP
    # Acima da função
    # Verificand oo tamanho da tabela de bindings
    bind = net_connect.send_command("show dhcp-snooping binding")
    # Dividir o texto em linhas
    linhas = bind.strip().split("\n")
    # Ignorar a linha do cabeçalho e a linha de separadores
    entradas_bind = linhas[2:]  # A partir da terceira linha são os dados
    # Verificando se a quantidade de entradas é menor que 6550 (80% de 8192)
    if len(entradas_bind) > 6550:
        texto += "DHCP-SNOOPING V4 BINDINGS acima de 80% do limite (8192). IP: " + dev + ", Quantidade de entradas: " + str(len(entradas_bind)) + ".\n"
        log_ex.warning(f"FALHA,DHCP-SNOOPING V4 - BINDINGS acima de 80% do limite (8192). Quantidade de entradas: {str(len(entradas_bind))},{dev}")
        log_dat.warning(f"FALHA,DHCP-SNOOPING V4,BINDINGS acima de 80% do limite (8192),{str(len(entradas_bind))},{dev}")
        erro_zabbix = "zabbix_sender -z ==ENDERECO_IP_ZABBIX== -s Projeto_Switch_Netbox -k Trap_Erros_DHCP_snooping -o \"" + dev + " - BINDINGS acima de 80% do limite (8192): " + str(len(entradas_bind)) + "\""
        os.system(erro_zabbix)
        cont_erros += 1
    # Aplicando o template a resposta do ativo
    parser = ttp(data=net_connect.send_command("show dhcp-snooping"), template=ttp_dhcp_sn_v4, log_level='CRITICAL')
    parser.parse()
    res = parser.result()
    if res != [[{}]]:
        if res[0][0]['dhcp_sn_v4_status'] == 'Yes':
            try:
                if res[0][0]['dhcp_sn_v4_vlans'] != '1-4000':
                    texto += "DHCP-SNOOPING V4 não está configurado em todas as vlans. IP: " + dev + ".\n"
                    log_ex.warning(f"FALHA,DHCP-SNOOPING V4 - Não está configurado em todas as vlans,{dev}")
                    log_dat.warning(f"FALHA,DHCP-SNOOPING V4,Não está configurado em todas as vlans,,{dev}")
                    erro_zabbix = "zabbix_sender -z ==ENDERECO_IP_ZABBIX== -s Projeto_Switch_Netbox -k Trap_Erros_DHCP_snooping -o \"" + dev + " - Não está configurado em todas as vlans\""
                    os.system(erro_zabbix)
                    cont_erro_update += 1
                    cont_erros += 1
            except Exception:
                texto += "ERRO ao coletar vlans habilitadas no DHCP-SNOOPING V4. IP: " + dev + ".\n"
                log_ex.warning(f"FALHA,DHCP-SNOOPING V4 - ERRO ao coletar vlans habilitadas,{dev}")
                log_dat.warning(f"FALHA,DHCP-SNOOPING V4,ERRO ao coletar vlans habilitadas,,{dev}")
                erro_zabbix = "zabbix_sender -z ==ENDERECO_IP_ZABBIX== -s Projeto_Switch_Netbox -k Trap_Erros_DHCP_snooping -o \"" + dev + " - ERRO ao coletar vlans habilitadas\""
                os.system(erro_zabbix)
            try:
                if res[0][0]['dhcp_sn_v4_verify_mac'] != 'Yes':
                    texto += "DHCP-SNOOPING V4 não está verificando o endereço MAC. IP: " + dev + "\n."
                    log_ex.warning(f"FALHA,DHCP-SNOOPING V4 - Não está verificando o endereço MAC,{dev}")
                    log_dat.warning(f"FALHA,DHCP-SNOOPING V4,Não está verificando o endereço MAC,,{dev}")
                    erro_zabbix = "zabbix_sender -z ==ENDERECO_IP_ZABBIX== -s Projeto_Switch_Netbox -k Trap_Erros_DHCP_snooping -o \"" + dev + " - Não está verificando o endereço MAC\""
                    os.system(erro_zabbix)
                    cont_erro_update += 1
                    cont_erros += 1
            except Exception:
                texto += "ERRO ao coletar validação de MAC no DHCP-snooping V4. IP: " + dev + ".\n"
                log_ex.warning(f"FALHA,DHCP-SNOOPING V4 - ERRO ao coletar validação de MAC,{dev}")
                log_dat.warning(f"FALHA,DHCP-SNOOPING V4,ERRO ao coletar validação de MAC,,{dev}")
                erro_zabbix = "zabbix_sender -z ==ENDERECO_IP_ZABBIX== -s Projeto_Switch_Netbox -k Trap_Erros_DHCP_snooping -o \"" + dev + " - ERRO ao coletar validação de MAC\""
                os.system(erro_zabbix)
            try:
                if res[0][0]['dhcp_sn_v4_op_82'] != 'keep' or res[0][0]['dhcp_sn_v4_op_82_insert'] != 'No':
                    texto += "DHCP-SNOOPING V4 está com a configuração incorreta da OPTION 82. IP: " + dev + ".\n"
                    log_ex.warning(f"FALHA,DHCP-SNOOPING V4 - Configuração incorreta da OPTION 82,{dev}")
                    log_dat.warning(f"FALHA,DHCP-SNOOPING V4,Configuração incorreta,OPTION 82,{dev}")
                    erro_zabbix = "zabbix_sender -z ==ENDERECO_IP_ZABBIX== -s Projeto_Switch_Netbox -k Trap_Erros_DHCP_snooping -o \"" + dev + " - Configuração incorreta da OPTION 82\""
                    os.system(erro_zabbix)
                    cont_erro_update += 1
                    cont_erros += 1
            except Exception:
                texto += "ERRO ao coletar OPTION 82 no DHCP-snooping V4. IP: " + dev + ".\n"
                log_ex.warning(f"FALHA,DHCP-SNOOPING V4 - ERRO ao coletar OPTION 82,{dev}")
                log_dat.warning(f"FALHA,DHCP-SNOOPING V4,ERRO ao coletar OPTION 82,,{dev}")
                erro_zabbix = "zabbix_sender -z ==ENDERECO_IP_ZABBIX== -s Projeto_Switch_Netbox -k Trap_Erros_DHCP_snooping -o \"" + dev + " - ERRO ao coletar a OPTION 82\""
                os.system(erro_zabbix)
            # Comando secundário para avaliação do dhcp-snnoping v4
            parser = ttp(data=net_connect.send_command("show dhcp-snooping stats"), template=ttp_dhcp_sn_v4_stats, log_level='CRITICAL')
            parser.parse()
            res = parser.result()
            try:
                if res[0][0]['dhcp_sn_v4_packets_received_trusted_port'] == '0' and res[0][0]['dhcp_sn_v4_packets_sent_to_trusted_port'] != '0':
                    texto += "DHCP-SNOOPING V4 - Sem receber mensagens do servidor DHCP. IP: " + dev + ", valor: " + res[0][0]['dhcp_sn_v4_packets_received_trusted_port'] + ".\n"
                    log_ex.warning(f"FALHA,DHCP-SNOOPING V4 - Sem receber mensagens do servidor DHCP. Valor: {res[0][0]['dhcp_sn_v4_packets_received_trusted_port']},{dev}")
                    log_dat.warning(f"FALHA,DHCP-SNOOPING V4,Sem receber mensagens do servidor DHCP,{res[0][0]['dhcp_sn_v4_packets_received_trusted_port']},{dev}")
                    erro_zabbix = "zabbix_sender -z ==ENDERECO_IP_ZABBIX== -s Projeto_Switch_Netbox -k Trap_Erros_DHCP_snooping -o \"" + dev + " - Sem receber mensagens do servidor DHCP\""
                    os.system(erro_zabbix)
                    cont_erros += 1
            except Exception:
                texto += "ERRO ao coletar pacotes recebidos da porta trust DHCP-snooping V4. IP: " + dev + ".\n"
                log_ex.warning(f"FALHA,DHCP-SNOOPING V4 - ERRO ao coletar pacotes recebidos da porta trust,{dev}")
                log_dat.warning(f"FALHA,DHCP-SNOOPING V4,ERRO ao coletar pacotes recebidos da porta trust,,{dev}")
                erro_zabbix = "zabbix_sender -z ==ENDERECO_IP_ZABBIX== -s Projeto_Switch_Netbox -k Trap_Erros_DHCP_snooping -o \"" + dev + " - ERRO ao coletar pacotes recebidos da porta trust\""
                os.system(erro_zabbix)
            try:
                if res[0][0]['dhcp_sn_v4_packets_reveived_untrusted_port'] != '0' or res[0][0]['dhcp_sn_v4_packets_drop_unaut_server'] != '0':
                    texto += "DHCP-SNOOPING V4 - Detectado dhcp incorreto na rede. IP: "+ dev + ", valor: " + res[0][0]['dhcp_sn_v4_packets_reveived_untrusted_port'] + ".\n"
                    log_ex.warning(f"FALHA,DHCP-SNOOPING V4 - Detectado dhcp incorreto na rede. Valor: {res[0][0]['dhcp_sn_v4_packets_reveived_untrusted_port']},{dev}")
                    log_dat.warning(f"FALHA,DHCP-SNOOPING V4,Detectado dhcp incorreto na rede,{res[0][0]['dhcp_sn_v4_packets_reveived_untrusted_port']},{dev}")
                    erro_zabbix = "zabbix_sender -z ==ENDERECO_IP_ZABBIX== -s Projeto_Switch_Netbox -k Trap_Erros_DHCP_snooping -o \"" + dev + " - Detectado dhcp incorreto na rede. Pacotes recebidos: " + str(res[0][0]['dhcp_sn_v4_packets_reveived_untrusted_port']) + "\""
                    os.system(erro_zabbix)
                    cont_erro_update += 1
                    cont_erros += 1
            except Exception:
                texto += "ERRO ao coletar pacotes recebidos de porta untrusted DHCP-snooping V4. IP: " + dev + ".\n"
                log_ex.warning(f"FALHA,DHCP-SNOOPING V4 - ERRO ao coletar pacotes recebidos de porta untrusted,{dev}")
                log_dat.warning(f"FALHA,DHCP-SNOOPING V4,ERRO ao coletar pacotes recebidos de porta untrusted,,{dev}")
                erro_zabbix = "zabbix_sender -z ==ENDERECO_IP_ZABBIX== -s Projeto_Switch_Netbox -k Trap_Erros_DHCP_snooping -o \"" + dev + " - ERRO ao coletar pacotes recebidos de porta untrusted\""
                os.system(erro_zabbix)
            try:
                if res[0][0]['dhcp_sn_v4_failed_mac_check'] != '0':
                    texto += "DHCP-SNOOPING V4 - Falha no MAC check. IP: " + dev + ", valor: " + res[0][0]['dhcp_sn_v4_failed_mac_check'] + ".\n"
                    log_ex.warning(f"FALHA,DHCP-SNOOPING V4 - Falha no MAC check. Valor: {res[0][0]['dhcp_sn_v4_failed_mac_check']},{dev}")
                    log_dat.warning(f"FALHA,DHCP-SNOOPING V4,Falha no MAC check,{res[0][0]['dhcp_sn_v4_failed_mac_check']},{dev}")
                    erro_zabbix = "zabbix_sender -z ==ENDERECO_IP_ZABBIX== -s Projeto_Switch_Netbox -k Trap_Erros_DHCP_snooping -o \"" + dev + " - Falha no MAC check: " + str(res[0][0]['dhcp_sn_v4_failed_mac_check']) + "\""
                    os.system(erro_zabbix)
                    cont_erros += 1
            except Exception:
                texto += "ERRO ao coletar MAC check no DHCP-snooping V4. IP: " + dev + ".\n"
                log_ex.warning(f"FALHA,DHCP-SNOOPING V4 - ERRO ao coletar MAC check ,{dev}")
                log_dat.warning(f"FALHA,DHCP-SNOOPING V4,ERRO ao coletar MAC check,,{dev}")
                erro_zabbix = "zabbix_sender -z ==ENDERECO_IP_ZABBIX== -s Projeto_Switch_Netbox -k Trap_Erros_DHCP_snooping -o \"" + dev + " - ERRO ao coletar MAC check\""
                os.system(erro_zabbix)
            try:
                if res[0][0]['dhcp_sn_v4_max_bind'] != '0':
                    texto += "DHCP-SNOOPING V4 - Quantidade máxima de bindings. IP: " + dev + ", valor: " + res[0][0]['dhcp_sn_v4_max_bind'] + ".\n"
                    log_ex.warning(f"FALHA,DHCP-SNOOPING V4 - Quantidade máxima de bindings. Valor: {res[0][0]['dhcp_sn_v4_max_bind']},{dev}")
                    log_dat.warning(f"FALHA,DHCP-SNOOPING V4,Quantidade máxima de bindings,{res[0][0]['dhcp_sn_v4_max_bind']},{dev}")
                    erro_zabbix = "zabbix_sender -z ==ENDERECO_IP_ZABBIX== -s Projeto_Switch_Netbox -k Trap_Erros_DHCP_snooping -o \"" + dev + " - Quantidade máxima de bindings: " + str(res[0][0]['dhcp_sn_v4_max_bind']) + "\""
                    os.system(erro_zabbix)
                    cont_erros += 1
            except Exception:
                texto += "ERRO ao coletar quantidade máxima de bindings DHCP-snooping V4. IP: " + dev + ".\n"
                log_ex.warning(f"FALHA,DHCP-SNOOPING V4 - ERRO ao coletar quantidade máxima de bindings,{dev}")
                log_dat.warning(f"FALHA,DHCP-SNOOPING V4,ERRO ao coletar quantidade máxima de bindings,,{dev}")
                erro_zabbix = "zabbix_sender -z ==ENDERECO_IP_ZABBIX== -s Projeto_Switch_Netbox -k Trap_Erros_DHCP_snooping -o \"" + dev + " - ERRO ao coletar quantidade máxima de bindings\""
                os.system(erro_zabbix)
        else:
            texto += "DHCP-SNOOPING V4 desabilitado. IP: " + dev + ".\n"
            log_ex.warning(f"FALHA,DHCP-SNOOPING V4 - Desabilitado,{dev}")
            log_dat.warning(f"FALHA,DHCP-SNOOPING V4,Desabilitado,,{dev}")
            erro_zabbix = "zabbix_sender -z ==ENDERECO_IP_ZABBIX== -s Projeto_Switch_Netbox -k Trap_Erros_DHCP_snooping -o \"" + dev + " - DESABILITADO\""
            os.system(erro_zabbix)
            cont_erro_update += 1
            cont_erros += 1
    else:
        texto += "DHCP-SNOOPING V4 desabilitado. IP: " + dev + ".\n"
        log_ex.warning(f"FALHA,DHCP-SNOOPING V4 - Desabilitado,{dev}")
        log_dat.warning(f"FALHA,DHCP-SNOOPING V4,Desabilitado,,{dev}")
        erro_zabbix = "zabbix_sender -z ==ENDERECO_IP_ZABBIX== -s Projeto_Switch_Netbox -k Trap_Erros_DHCP_snooping -o \"" + dev + " - DESABILITADO\""
        os.system(erro_zabbix)
        cont_erro_update += 1
        cont_erros += 1
    # Reseta contadores
    try:
        net_connect.send_command("clear dhcp-snooping statistics")
    except Exception:
        texto += "ERRO ao resetar contadores do DHCP-SNOOPING V4. IP: " + dev + ".\n"
        log_ex.warning(f"FALHA,DHCP-SNOOPING V4 - ERRO ao resetar contadores,{dev}.")
        log_dat.warning(f"FALHA,DHCP-SNOOPING V4,ERRO ao resetar contadores,,{dev}.")
        erro_zabbix = "zabbix_sender -z ==ENDERECO_IP_ZABBIX== -s Projeto_Switch_Netbox -k Trap_Erros_DHCP_snooping -o \"" + dev + " - ERRO ao resetar contadores\""
        os.system(erro_zabbix)
        cont_reset += 1
    # Atualiza a configuração caso tenha encontrado erros de configuração
    if cont_erro_update > 0:
        config_ar2530.update_dhcp_snoop_v4(net_connect, dev, log_ex, log_dat)
    # Mensagem caso não encontre nenhum erro
    if cont_erros == 0:
        log_ex.warning(f"SUCESSO,DHCP-SNOOPING V4 - Configurado corretamente,{dev}")
        log_dat.warning(f"SUCESSO,DHCP-SNOOPING V4,Configuração correta,,{dev}")
    if cont_reset == 0:
        log_ex.warning(f"SUCESSO,DHCP-SNOOPING V4 - Contadores resetados,{dev}")
        log_dat.warning(f"SUCESSO,DHCP-SNOOPING V4,Contadores resetados,,{dev}")    
    # ENCONTRAR PORTA UPLINK E VALIDAR PORTA TRUST
    return texto


# DHCP-SNOOPING v6
# show dhcpv6-snooping
# show dhcpv6-snooping stats
# show dhcp-snooping binding
ttp_dhcp_sn_v6 = """
  DHCPv6 Snooping              : {{dhcp_sn_v6_status}}
  Enabled Vlans                : {{dhcp_sn_v6_vlans}}
  Store lease database         : {{dhcp_sn_v4_store_lease | ORPHRASE}}
"""
ttp_dhcp_sn_v6_stats = """
 server       forward  from trusted port              {{dhcp_sn_v6_packets_received_trusted_port}}
 client       forward  to trusted port                {{dhcp_sn_v6_packets_sent_to_trusted_port}}
 server       drop     received on untrusted port     {{dhcp_sn_v6_packets_reveived_untrusted_port}}
 server       drop     unauthorized server            {{dhcp_sn_v6_packets_drop_unaut_server}}
 client       drop     destination on validating port {{dhcp_sn_v6_destination_validanting_port}}
 client       drop     relay reply on validating port {{dhcp_sn_v6_reply_validating_port}}
 client       drop     bad DHCP release request       {{dhcp_sn_v6_bad_dhcp_release}}
 client       drop     max-binding limit reached    {{dhcp_sn_v6_max_bind}}
 """
def dhcp_v6_snoop(net_connect, dev,log_ex, log_dat):
    # Variável de retorno
    texto = ''
    cont_erros = 0
    cont_reset = 0
    cont_erro_update = 0
    # Templates TTP
    # Acima da função
    # Verificand oo tamanho da tabela de bindings
    bind = net_connect.send_command("show dhcpv6-snooping binding")
    # Dividir o texto em linhas
    linhas = bind.strip().split("\n")
    # Ignorar a linha do cabeçalho e a linha de separadores
    entradas_bind = linhas[2:]
    # Verificando se a quantidade de entradas é menor que 6550 (80% de 8192)
    if len(entradas_bind) > 6550:
        texto += "DHCP-SNOOPING V6 BINDINGS acima de 80% do limite (8192). IP: " + dev + ", Quantidade de entradas: " + str(len(entradas_bind)) + ".\n"
        log_ex.warning(f"FALHA,DHCP-SNOOPING V6 - BINDINGS acima de 80% do limite (8192). Quantidade de entradas: {str(len(entradas_bind))},{dev}")
        log_dat.warning(f"FALHA,DHCP-SNOOPING V6,BINDINGS acima de 80% do limite (8192),{str(len(entradas_bind))},{dev}")
        erro_zabbix = "zabbix_sender -z ==ENDERECO_IP_ZABBIX== -s Projeto_Switch_Netbox -k Trap_Erros_DHCPv6_snooping -o \"" + dev + " - BINDINGS acima de 80% do limite (8192): " + str(len(entradas_bind)) + "\""
        os.system(erro_zabbix)
        cont_erros += 1
    # Aplicando o template a resposta do ativo
    parser = ttp(data=net_connect.send_command("show dhcpv6-snooping"), template=ttp_dhcp_sn_v6, log_level='CRITICAL')
    parser.parse()
    res = parser.result()
    if res != [[{}]]:
        if res[0][0]['dhcp_sn_v6_status'] == 'Yes':
            try:
                if res[0][0]['dhcp_sn_v6_vlans'] != '1-4000':
                    texto += "DHCP-SNOOPING V6 não está configurado para em as vlans. IP: " + dev + ".\n"
                    log_ex.warning(f"FALHA,DHCP-SNOOPING V6 - Não está configurado em todas as vlans,{dev}")
                    log_dat.warning(f"FALHA,DHCP-SNOOPING V6,Não está configurado em todas as vlans,,{dev}")
                    erro_zabbix = "zabbix_sender -z ==ENDERECO_IP_ZABBIX== -s Projeto_Switch_Netbox -k Trap_Erros_DHCPv6_snooping -o \"" + dev + " - Não está configurado em todas as vlans\""
                    os.system(erro_zabbix)
                    cont_erro_update += 1
                    cont_erros += 1
            except Exception:
                texto += "ERRO ao coletar vlans mapeadas DHCPv6-snooping. IP: " + dev + ".\n"
                log_ex.warning(f"FALHA,DHCP-SNOOPING V6 - ERRO ao coletar vlans mapeadas,{dev}")
                log_dat.warning(f"FALHA,DHCP-SNOOPING V6,ERRO ao coletar vlans mapeadas,,{dev}")
                erro_zabbix = "zabbix_sender -z ==ENDERECO_IP_ZABBIX== -s Projeto_Switch_Netbox -k Trap_Erros_DHCPv6_snooping -o \"" + dev + " - ERRO ao coletar vlans mapeadas\""
                os.system(erro_zabbix)
            # Comando secundário para avaliação do dhcp-snnoping v6
            parser = ttp(data=net_connect.send_command("show dhcpv6-snooping stats"), template=ttp_dhcp_sn_v6_stats, log_level='CRITICAL')
            parser.parse()
            res = parser.result()
            try:
                if res[0][0]['dhcp_sn_v6_packets_received_trusted_port'] == '0' and res[0][0]['dhcp_sn_v6_packets_sent_to_trusted_port'] != '0':
                    texto += "DHCP-SNOOPING V6 - Sem receber mensagens do servidor DHCP. IP: " + dev + ", valor: " + res[0][0]['dhcp_sn_v6_packets_received_trusted_port'] + ".\n"
                    log_ex.warning(f"FALHA,DHCP-SNOOPING V6 - Sem receber mensagens do servidor DHCP. Valor: {res[0][0]['dhcp_sn_v6_packets_received_trusted_port']},{dev}")
                    log_dat.warning(f"FALHA,DHCP-SNOOPING V6,Sem receber mensagens do servidor DHCP,{res[0][0]['dhcp_sn_v6_packets_received_trusted_port']},{dev}")
                    erro_zabbix = "zabbix_sender -z ==ENDERECO_IP_ZABBIX== -s Projeto_Switch_Netbox -k Trap_Erros_DHCPv6_snooping -o \"" + dev + " - Sem receber mensagens do servidor DHCP\""
                    os.system(erro_zabbix)
                    cont_erros += 1
            except Exception:
                texto += "ERRO ao coletar pacotes recebidos da porta trust DHCPv6-snooping. IP: " + dev + ".\n"
                log_ex.warning(f"FALHA,DHCP-SNOOPING V6 - ERRO ao coletar pacotes recebidos da porta trust,{dev}")
                log_dat.warning(f"FALHA,DHCP-SNOOPING V6,ERRO ao coletar pacotes recebidos da porta trust,,{dev}")
                erro_zabbix = "zabbix_sender -z ==ENDERECO_IP_ZABBIX== -s Projeto_Switch_Netbox -k Trap_Erros_DHCPv6_snooping -o \"" + dev + " - ERRO ao coletar pacotes recebidos da porta trust\""
                os.system(erro_zabbix)
            try:
                if res[0][0]['dhcp_sn_v6_packets_reveived_untrusted_port'] != '0' or res[0][0]['dhcp_sn_v6_packets_drop_unaut_server'] != '0':
                    texto += "DHCP-SNOOPING V6 - Detectado dhcp incorreto na rede. IP: " + dev + ", valor: " + res[0][0]['dhcp_sn_v6_packets_reveived_untrusted_port'] + ".\n"
                    log_ex.warning(f"FALHA,DHCP-SNOOPING V6 - Detectado dhcp incorreto na rede. Valor: {res[0][0]['dhcp_sn_v6_packets_reveived_untrusted_port']},{dev}")
                    log_dat.warning(f"FALHA,DHCP-SNOOPING V6,Detectado dhcp incorreto na rede,{res[0][0]['dhcp_sn_v6_packets_reveived_untrusted_port']},{dev}")
                    erro_zabbix = "zabbix_sender -z ==ENDERECO_IP_ZABBIX== -s Projeto_Switch_Netbox -k Trap_Erros_DHCPv6_snooping -o \"" + dev + " - Detectado dhcp incorreto na rede. Pacotes recebidos: " + str(res[0][0]['dhcp_sn_v6_packets_reveived_untrusted_port']) + "\""
                    os.system(erro_zabbix)
                    cont_erro_update += 1
                    cont_erros += 1
            except Exception:
                texto += "ERRO ao coletar pacotes recebidos de porta untrusted DHCPv6-snooping. IP: " + dev + ".\n"
                log_ex.warning(f"FALHA,DHCP-SNOOPING V6 - ERRO ao coletar pacotes recebidos de porta untrusted,{dev}")
                log_dat.warning(f"FALHA,DHCP-SNOOPING V6,ERRO ao coletar pacotes recebidos de porta untrusted,,{dev}")
                erro_zabbix = "zabbix_sender -z ==ENDERECO_IP_ZABBIX== -s Projeto_Switch_Netbox -k Trap_Erros_DHCPv6_snooping -o \"" + dev + " - ERRO ao coletar pacotes recebidos de porta untrusted\""
                os.system(erro_zabbix)
            try:
                if res[0][0]['dhcp_sn_v6_destination_validanting_port'] != '0' or res[0][0]['dhcp_sn_v6_reply_validating_port'] != '0':
                    texto += "DHCP-SNOOPING V6 - Detectado tráfego em porta em validação. IP: " + dev + ", valor: " + res[0][0]['dhcp_sn_v6_destination_validanting_port'] + ".\n"
                    log_ex.warning(f"FALHA,DHCP-SNOOPING V6 - Detectado tráfego em porta em validação. Valor: {res[0][0]['dhcp_sn_v6_destination_validanting_port']},{dev}")
                    log_dat.warning(f"FALHA,DHCP-SNOOPING V6,Detectado tráfego em porta em validação,{res[0][0]['dhcp_sn_v6_destination_validanting_port']},{dev}")
                    erro_zabbix = "zabbix_sender -z ==ENDERECO_IP_ZABBIX== -s Projeto_Switch_Netbox -k Trap_Erros_DHCPv6_snooping -o \"" + dev + " - Detectado tráfego em porta em validação. Pacotes recebidos: " + str(res[0][0]['dhcp_sn_v6_destination_validanting_port']) + "\""
                    os.system(erro_zabbix)
                    cont_erro_update += 1
                    cont_erros += 1
            except Exception:
                texto += "ERRO ao coletar tráfego em porta em validação DHCPv6-snooping. IP: " + dev + ".\n"
                log_ex.warning(f"FALHA,DHCP-SNOOPING V6 - ERRO ao coletar tráfego em porta em validação,{dev}")
                log_dat.warning(f"FALHA,DHCP-SNOOPING V6,ERRO ao coletar tráfego em porta em validação,,{dev}")
                erro_zabbix = "zabbix_sender -z ==ENDERECO_IP_ZABBIX== -s Projeto_Switch_Netbox -k Trap_Erros_DHCPv6_snooping -o \"" + dev + " - ERRO ao coletar tráfego em porta em validação\""
                os.system(erro_zabbix)
            try:
                if res[0][0]['dhcp_sn_v6_max_bind'] != '0':
                    texto += "DHCP-SNOOPING V6 - Quantidade máxima de bindings. IP: " + dev + ", valor: " + res[0][0]['dhcp_sn_v6_max_bind'] + ".\n"
                    log_ex.warning(f"FALHA,DHCP-SNOOPING V6 - Quantidade máxima de bindings. Valor: {res[0][0]['dhcp_sn_v6_max_bind']},{dev}")
                    log_dat.warning(f"FALHA,DHCP-SNOOPING V6,Quantidade máxima de bindings,{res[0][0]['dhcp_sn_v6_max_bind']},{dev}")
                    erro_zabbix = "zabbix_sender -z ==ENDERECO_IP_ZABBIX== -s Projeto_Switch_Netbox -k Trap_Erros_DHCPv6_snooping -o \"" + dev + " - Quantidade máxima de bindings: " + str(res[0][0]['dhcp_sn_v6_max_bind']) + "\""
                    os.system(erro_zabbix)
                    cont_erros += 1
            except Exception:
                texto += "ERRO ao coletar quantidade máxima de bindings DHCPv6-snooping. IP: " + dev + ".\n"
                log_ex.warning(f"FALHA,DHCP-SNOOPING V6 - ERRO ao coletar quantidade máxima de bindings,{dev}")
                log_dat.warning(f"FALHA,DHCP-SNOOPING V6,ERRO ao coletar quantidade máxima de bindings,,{dev}")
                erro_zabbix = "zabbix_sender -z ==ENDERECO_IP_ZABBIX== -s Projeto_Switch_Netbox -k Trap_Erros_DHCPv6_snooping -o \"" + dev + " - ERRO ao coletar quantidade máxima de bindings\""
                os.system(erro_zabbix)
            # ENCONTRAR PORTA UPLINK E VALIDAR PORTA TRUST
        else:
            texto += "DHCP-SNOOPING V6 desabilitado. IP: " + dev + ".\n"
            log_ex.warning(f"FALHA,DHCP-SNOOPING V6 - Desabilitado,{dev}")
            log_dat.warning(f"FALHA,DHCP-SNOOPING V6,Desabilitado,,{dev}")
            erro_zabbix = "zabbix_sender -z ==ENDERECO_IP_ZABBIX== -s Projeto_Switch_Netbox -k Trap_Erros_DHCPv6_snooping -o \"" + dev + " - DESABILITADO\""
            os.system(erro_zabbix)
            cont_erro_update += 1
            cont_erros += 1
    else:
        texto += "DHCP-SNOOPING V6 desabilitado. IP: " + dev + ".\n"
        log_ex.warning(f"FALHA,DHCP-SNOOPING V6 - Desabilitado,{dev}")
        log_dat.warning(f"FALHA,DHCP-SNOOPING V6,Desabilitado,,{dev}")
        erro_zabbix = "zabbix_sender -z ==ENDERECO_IP_ZABBIX== -s Projeto_Switch_Netbox -k Trap_Erros_DHCPv6_snooping -o \"" + dev + " - DESABILITADO\""
        os.system(erro_zabbix)
        cont_erro_update += 1
        cont_erros += 1
    # Reseta contadores
    try:
        net_connect.send_command("clear dhcpv6-snooping statistics")
    except Exception:
        texto += "ERRO ao resetar contadores do DHCP-SNOOPING V6. IP: " + dev + ".\n"
        log_ex.warning(f"FALHA,DHCP-SNOOPING V6 - ERRO ao resetar contadores,{dev}")
        log_dat.warning(f"FALHA,DHCP-SNOOPING V6,ERRO ao resetar contadores,,{dev}")
        erro_zabbix = "zabbix_sender -z ==ENDERECO_IP_ZABBIX== -s Projeto_Switch_Netbox -k Trap_Erros_DHCPv6_snooping -o \"" + dev + " - ERRO ao resetar contadores\""
        os.system(erro_zabbix)
        cont_reset += 1
    # Atualiza a configuração caso tenha encontrado erros de configuração
    if cont_erro_update > 0:
        config_ar2530.update_dhcp_snoop_v6(net_connect, dev, log_ex, log_dat)
    # Mensagem caso não encontre nenhum erro
    if cont_erros == 0:
        log_ex.warning(f"SUCESSO,DHCP-SNOOPING V6 - Configurado corretamente,{dev}")
        log_dat.warning(f"SUCESSO,DHCP-SNOOPING V6,Configuraçãp correta,,{dev}")
    if cont_reset == 0:
        log_ex.warning(f"SUCESSO,DHCP-SNOOPING V6 - Contadores resetados,{dev}")
        log_dat.warning(f"SUCESSO,DHCP-SNOOPING V6,Contadores resetados,,{dev}")
    # ENCONTRAR PORTA UPLINK E VALIDAR PORTA TRUST
    return texto


# show system information (firmware-[firmware], rom-[versao_rom], serial-[serial], mac-[mac_add])
# show system memory (part number-[part_number])
# show banner motd
# show banner motd
ttp_system_memory = """"
  System Name        : {{sysname}}
  Product SKU        : {{part_number}}
  Flash Size         : {{memoria_fhash | ORPHRASE}}
  RAM Size           : {{memoria_ram | ORPHRASE}}
"""
def validar_dados_ativo_cmdb(net_connect, dev, mac_cmdb, modelo_cmdb, serial_cmdb, tombo_cmdb):
    # Variável de retorno
    texto = ''
    cont_erros = 0
    # Templates TTP
    # Acima da função
    # Aplicando o template a resposta do ativo
    parser = ttp(data=net_connect.send_command("show system informatio"), template=ttp_system_info, log_level='CRITICAL')
    parser.parse()
    res = parser.result()
    try:
        if res[0][0]['firmware'][:-5] != 'YA.16.11' or res[0][0]['firmware'][:-5] != 'WC.16.11':
            texto += "FIRMWARE desatualizado. IP: " + dev + ", Firmware: " + res[0][0]['firmware'] + ".\n"
            logging.warning(f"FALHA,FIRMWARE desatualizado. Firmware: {res[0][0]['firmware']},{dev}")
            erro_zabbix = "zabbix_sender -z ==ENDERECO_IP_ZABBIX== -s Projeto_Switch_Netbox -k Trap_Erros_Cadastro_CMDB -o \"" + dev + " - FIRMWARE desatualizado. Firmware: " + str(res[0][0]['firmware']) + "\""
            os.system(erro_zabbix)
            cont_erros += 1
    except Exception:
            texto += "ERRO ao coletar firmware do ativo. IP: " + dev + ".\n"
            logging.warning(f"FALHA,ERRO ao coletar firmware do ativo,{dev}")
            erro_zabbix = "zabbix_sender -z ==ENDERECO_IP_ZABBIX== -s Projeto_Switch_Netbox -k Trap_Erros_Cadastro_CMDB -o \"" + dev + " - ERRO ao coletar firmware do ativo\""
            os.system(erro_zabbix)
    try:
        if res[0][0]['serial'].upper() != serial_cmdb.upper():
            texto += "SERIAL incorreto entre o CMB e ATIVO. IP: " + dev + ", Serial ATIVO: " + res[0][0]['serial'] + ", Serial CMDB: " + serial_cmdb + ".\n"
            logging.warning(f"FALHA,SERIAL incorreto entre o CMB e ATIVO. Serial ATIVO: {res[0][0]['serial']}. Serial CMDB: {serial_cmdb},{dev}")
            erro_zabbix = "zabbix_sender -z ==ENDERECO_IP_ZABBIX== -s Projeto_Switch_Netbox -k Trap_Erros_Cadastro_CMDB -o \"" + dev + " - SERIAL incorreto entre o CMB e ATIVO. Serial ATIVO: " + str(res[0][0]['serial']) + ", Serial CMDB: " + str(serial_cmdb) + "\""
            os.system(erro_zabbix)
            cont_erros += 1
    except Exception:
            texto += "ERRO ao coletar serial do ativo. IP: " + dev + ".\n"
            logging.warning(f"FALHA,ERRO ao coletar serial do ativo,{dev}")
            erro_zabbix = "zabbix_sender -z ==ENDERECO_IP_ZABBIX== -s Projeto_Switch_Netbox -k Trap_Erros_Cadastro_CMDB -o \"" + dev + " - ERRO ao coletar serial do ativo\""
            os.system(erro_zabbix)
    # Comparando os dois endereços MAC
    try:
        if res[0][0]['mac_add'].replace(':', '').replace('-', '').upper() != mac_cmdb:
            texto += "MACs diferentes entre o CMDB e o ATIVO: " + dev + ", MAC ATIVO: " + res[0][0]['mac_add'].replace(':', '').replace('-', '').upper() + ", MAC CMDB: " + mac_cmdb + ".\n"
            logging.warning(f"FALHA,MACs diferentes entre o CMDB e o ATIVO. MAC ATIVO: {res[0][0]['mac_add'].replace(':', '').replace('-', '').upper()}. MAC CMDB: {mac_cmdb},{dev}")
            erro_zabbix = "zabbix_sender -z ==ENDERECO_IP_ZABBIX== -s Projeto_Switch_Netbox -k Trap_Erros_Cadastro_CMDB -o \"" + dev + " - MACs diferentes entre o CMDB e o ATIVO. MAC ATIVO: " + str(res[0][0]['mac_add'].replace(':', '').replace('-', '').upper()) + ", MAC CMDB: " + str(mac_cmdb) + "\""
            os.system(erro_zabbix)
            cont_erros += 1
    except Exception:
            texto += "ERRO ao coletar MAC do ativo. IP: " + dev + ".\n"
            logging.warning(f"FALHA,ERRO ao coletar MAC do ativo,{dev}")
            erro_zabbix = "zabbix_sender -z ==ENDERECO_IP_ZABBIX== -s Projeto_Switch_Netbox -k Trap_Erros_Cadastro_CMDB -o \"" + dev + " - ERRO ao coletar MAC do ativo\""
            os.system(erro_zabbix)
    # Aplicando o template a resposta do ativo
    parser = ttp(data=net_connect.send_command("show system memory"), template=ttp_system_memory, log_level='CRITICAL')
    parser.parse()
    res = parser.result()
    # Comparando os dois part numbers
    try:
        if res[0][0]['part_number'].upper() != modelo_cmdb:
            texto += "PART NUMBER diferentes entre o CMDB e o ATIVO: " + dev + ", PART NUMBER ATIVO: " + res[0][0]['part_number'].upper() + ", PART NUMBER CMDB: " + modelo_cmdb + ".\n"
            logging.warning(f"FALHA,PART NUMBER diferentes entre o CMDB e o ATIVO. PART NUMBER ATIVO: {res[0][0]['part_number'].upper()}. PART NUMBER CMDB: {modelo_cmdb},{dev}")
            erro_zabbix = "zabbix_sender -z ==ENDERECO_IP_ZABBIX== -s Projeto_Switch_Netbox -k Trap_Erros_Cadastro_CMDB -o \"" + dev + " - PART NUMBER incorreto entre o CMB e ATIVO. PART NUMBER ATIVO: " + str(res[0][0]['part_number'].upper()) + ", PART NUMBER CMDB: " + str(modelo_cmdb) + "\""
            os.system(erro_zabbix)
            cont_erros += 1
    except Exception:
            texto += "ERRO ao coletar PART NUMBER do ativo. IP: " + dev + ".\n"
            logging.warning(f"FALHA,ERRO ao coletar PART NUMBER do ativo,{dev}.")
            erro_zabbix = "zabbix_sender -z ==ENDERECO_IP_ZABBIX== -s Projeto_Switch_Netbox -k Trap_Erros_Cadastro_CMDB -o \"" + dev + " - ERRO ao coletar PART NUMBER do ativo\""
            os.system(erro_zabbix)
    # Consultando dados do PATRIMONIO
    # ATIVO
    banner = net_connect.send_command("show banner motd")
    # Caso o patrimônio seja FUNPEC
    if 'FUNPEC' in banner.upper():
        match = re.search(r'FUNPEC\s(\d+)', banner)
        if match:
            patrimonio_ativo = match.group(0).upper()
        else:
            patrimonio_ativo = ''
    # Caso seja UFRN padrão 10 dígitos
    else:
        match = re.search(r'\d{10}', banner)
        if match:
            patrimonio_ativo =  match.group()
        else:
            patrimonio_ativo = ''
    # Comparando o PATRIMONIO
    try:
        if patrimonio_ativo != tombo_cmdb:
            texto += "PATRIMÔNIOS diferentes entre o CMDB e o ATIVO: " + dev + ", PATRIMÔNIO ATIVO: " + patrimonio_ativo + ", PATRIMÔNIO CMDB: " + tombo_cmdb + ".\n"
            logging.warning(f"FALHA,PATRIMÔNIOS diferentes entre o CMDB e o ATIVO. PATRIMÔNIO ATIVO: {patrimonio_ativo}. PATRIMÔNIO CMDB: {tombo_cmdb},{dev}")
            erro_zabbix = "zabbix_sender -z ==ENDERECO_IP_ZABBIX== -s Projeto_Switch_Netbox -k Trap_Erros_Cadastro_CMDB -o \"" + dev + " - PATRIMÔNIOS diferentes entre o CMDB e o ATIVO. PATRIMÔNIO ATIVO: " + str(patrimonio_ativo) + ", PATRIMÔNIO CMDB: " + str(tombo_cmdb) + "\""
            os.system(erro_zabbix)
            cont_erros += 1
    except Exception:
            texto += "ERRO ao coletar PATRIMÔNIO do ativo. IP: " + dev + ".\n"
            logging.warning(f"FALHA,ERRO ao coletar PATRIMÔNIO do ativo,{dev}")
            erro_zabbix = "zabbix_sender -z ==ENDERECO_IP_ZABBIX== -s Projeto_Switch_Netbox -k Trap_Erros_Cadastro_CMDB -o \"" + dev + " - ERRO ao coletar PATRIMÔNIO do ativo\""
            os.system(erro_zabbix)
    # Imprime mensagem de sucesso caso não tenha encontrado nenhum erro
    if cont_erros == 0:
        logging.warning(f"SUCESSO,Todas as informações cadastradas no CMDB foram validadas,{dev}")
    return texto


# show ip route
ttp_ip_route = "  {{destino}}          {{gateway}}      {{vlan}} {{tipo}}               {{metrica}}        {{dist}}"
# show ipv6 route
ttp_ipv6_route = """
 {{destino}}
 {{gateway | ORPHRASE}}              {{tipo}}   NA  {{distancia}}        {{metrica}}
 """
# show ipv6 routers
ttp_ipv6_routers = """"
  Router Address : {{ip_roteador}}
  Interface      : {{interface}}
  MTU            : {{mtu}}
  Hop Limit      : {{hop_limit}}
  """
def validar_rotas(net_connect, dev, gateway_v4_esperado):
    # Variável de retorno
    texto = ''
    cont_erros = 0
    # Templates TTP
    # Acima da função
    # Aplicando o template a resposta do ativo
    # Verificando rota IPv4
    parser = ttp(data=net_connect.send_command("show ip route"), template=ttp_ip_route, log_level='CRITICAL')
    parser.parse()
    res = parser.result()
    for rota in res[0][0]:
        try:
            if rota['destino'] == '0.0.0.0/0':
                # Compara com o coletado no ativo
                if rota['gateway'] != gateway_v4_esperado:
                    texto += "ROTA IPv4 DEFAULT incorreta. IP: " + dev + ", Gateway: " + rota['gateway'] + ".\n"
                    logging.warning(f"FALHA,ROTA IPv4 DEFAULT incorreta. Gateway: {rota['gateway']},{dev}")
                    erro_zabbix = "zabbix_sender -z ==ENDERECO_IP_ZABBIX== -s Projeto_Switch_Netbox -k Trap_Erros_Rotas -o \"" + dev + " - ROTA IPv4 DEFAULT incorreta. Gateway: " + str(rota['gateway']) + "\""
                    os.system(erro_zabbix)
                    cont_erros += 1
        except Exception:
                texto += "ERRO ao coletar rota IPv4 default no ativo. IP: " + dev + ".\n"
                logging.warning(f"FALHA,ERRO ao coletar rota IPv4 default no ativo,{dev}")
                erro_zabbix = "zabbix_sender -z ==ENDERECO_IP_ZABBIX== -s Projeto_Switch_Netbox -k Trap_Erros_Rotas -o \"" + dev + " - ERRO ao coletar rota IPv4 default no ativo\""
                os.system(erro_zabbix)
                cont_erros += 1
    # # Verificando rota IPv6 - COMENTADO, O 2530 RECEBE O ROTEADOR VIA LINK-LOCAL
    # parser = ttp(data=net_connect.send_command("show ipv6 route"), template=ttp_ipv6_route, log_level='CRITICAL')
    # parser.parse()
    # res = parser.result()
    # gateway_v6_esperado = ''
    # for rota in res[0][0]:
    #     try:
    #         if rota['destino'] == '::/0':
    #             # Identifica o gateway v6 esperado
    #             if dev['primary_ip6'] == None:
    #                 gateway_v6_esperado = ''
    #             else:
    #                 ultimo_ponto = str(dev['primary_ip6']['address']).rfind(':')
    #                 ipv6_gw = str(dev['primary_ip6']['address'])[:ultimo_ponto]
    #                 gateway_v6_esperado = ipv6_gw + ':1'
    #             # Compara com o coletado no ativo
    #             if rota['gateway'] != gateway_v6_esperado:
    #                 print(f"ROTA IPv6 DEFAULT incorreta. IP: {dev['primary_ip4']['address'][:-3]}, Gateway: {rota['gateway']}")
    #                 log_ex.warning("FALHA,ROTA IPv6 DEFAULT incorreta. IP: %s, Gateway: %s", dev['primary_ip4']['address'][:-3], rota['gateway'])
    #     except Exception:
    #         print(f"ROTA IPv6 DEFAULT incorreta. IP: {dev['primary_ip4']['address'][:-3]}, Gateway: {rota['gateway']}")
    #         log_ex.warning("FALHA,ROTA IPv6 DEFAULT incorreta. IP: %s, Gateway: %s", dev['primary_ip4']['address'][:-3], rota['gateway'])
    # Verificando a quantidade de roteadores IPv6
    parser = ttp(data=net_connect.send_command("show ipv6 routers"), template=ttp_ipv6_routers, log_level='CRITICAL')
    parser.parse()
    res = parser.result()
    quant_roteador_ipv6 = 0
    # Conta a quantidade de roteadores IPv6 coletados
    for roteador_v6 in res[0]:
        quant_roteador_ipv6 += 1
    # Mensagem de erro caso não encontre nenhum
    if quant_roteador_ipv6 == 0:
        texto += "NENHUM ROTEADOR IPv6 encontrado. IP: " + dev + ".\n"
        logging.warning(f"FALHA,NENHUM ROTEADOR IPv6 encontrado,{dev}")
        erro_zabbix = "zabbix_sender -z ==ENDERECO_IP_ZABBIX== -s Projeto_Switch_Netbox -k Trap_Erros_Rotas -o \"" + dev + " - NENHUM ROTEADOR IPv6 encontrado\""
        os.system(erro_zabbix)
        cont_erros += 1
    # Mensagem de erro caso encontre mais de 1
    if quant_roteador_ipv6 >1:
        texto += "MAIS DE 1 ROTEADOR IPv6 encontrado. IP: " + dev + ", Quantidade: " + str(quant_roteador_ipv6) + ".\n"
        logging.warning(f"FALHA,MAIS DE 1 ROTEADOR IPv6 encontrado. Quantidade: {quant_roteador_ipv6},{dev}")
        erro_zabbix = "zabbix_sender -z ==ENDERECO_IP_ZABBIX== -s Projeto_Switch_Netbox -k Trap_Erros_Rotas -o \"" + dev + " - MAIS DE 1 ROTEADOR IPv6 encontrado\""
        os.system(erro_zabbix)
        cont_erros += 1
    # Imprime mensagem de sucesso caso não tenha encontrado nenhum erro
    if cont_erros == 0:
        logging.warning(f"SUCESSO,Rotas IPv4 e IPv6 configuradas corretamente,{dev}")
    return texto


# show lldp info remote detail
ttp_lldp_info_remote_detail = """
  Local Port   : {{local_porta}}
  ChassisType  : {{remote_chassi_type | ORPHRASE}}
  ChassisId    : {{remote_chassi_id | ORPHRASE}}
  PortType     : {{remote_port_type | ORPHRASE}}
  PortId       : {{remoto_port_id | ORPHRASE}}
  SysName      : {{remoto_sysname | ORPHRASE}}
  System Descr : {{remoto_system_desc | ORPHRASE}}
  PortDescr    : {{remoto_port_desc | ORPHRASE}}
  Pvid         : {{remoto_pvid | ORPHRASE}}
     Address : 10{{remoto_ipv4 | ORPHRASE}}
     Address : 28{{remoto_ipv6 | ORPHRASE}}
"""
def validar_vizinhos_lldp(net_connect, dev, cabos_conectados, ativo_nome):
    # Variável de retorno
    texto = ''
    cont_erros = 0
    erros_lldp_temp = []
    erros_cmdb_temp = []
    # Templates TTP
    # Acima da função
    # Aplicando o template a resposta do ativo
    # Verificando vizinhos via LLDP no switch
    parser = ttp(data=net_connect.send_command("show lldp info remote detail"), template=ttp_lldp_info_remote_detail, log_level='CRITICAL')
    parser.parse()
    res = parser.result()
    # Ajusta o tamanho da variável de retorno
    try:
        if len(res[0][0][0]) > 0:
            res = res[0][0]
    except Exception:
        res = res[0]
    # Remover vizinhos não interessantes: aparelhos VoIP, câmeras, alguns computadores
    for item in res[:]:
        if 'remoto_sysname' not in item:
            res.remove(item)
            continue
        if 'remoto_system_desc' not in item:
            item['remoto_system_desc'] = ''
        if 'remote_chassi_id' not in item:
            item['remote_chassi_id'] = ''
        if 'T19' in item['remoto_sysname'] or 'T20' in item['remoto_sysname'] or 'T21' in item['remoto_sysname'] or 'T22' in item['remoto_sysname'] or 'T23' in item['remoto_sysname'] or '310HD' in item['remoto_sysname'] or 'axis' in item['remoto_sysname'] or 'IP Phone' in item['remoto_system_desc'] or 'armv5tej' in item['remoto_system_desc'] or 'Linux' in item['remoto_system_desc'] or 'DESKTOP' in item['remote_chassi_id'] or 'GXP1610' in item['remote_chassi_id']:
            res.remove(item)
    # VERIFICAR SE VIZINHOS LLDP ESTÁ VAZIO
    if len(res) == 0:
        texto += "NENHUM VIZINHO encontrado via LLDP. IP: " + dev + ".\n"
        logging.warning(f"FALHA,NENHUM VIZINHO encontrado via LLDP,,,{dev}")
        erro_zabbix = "zabbix_sender -z ==ENDERECO_IP_ZABBIX== -s Projeto_Switch_Netbox -k Trap_Erros_Vizinhos -o \"" + dev + " - NENHUM VIZINHO encontrado via LLDP\""
        os.system(erro_zabbix)
        # print(f'NENHUM LLDP: {dev}')
        cont_erros += 1
        return texto
    # VERIFICAR SE VIZINHOS CMDB ESTÁ VAZIO
    if len(cabos_conectados) == 0:
        texto += "NENHUMA LIGAÇÃO encontrada no CMDB. IP: " + dev + ".\n"
        logging.warning(f"FALHA,NENHUMA LIGAÇÃO encontrada no CMDB,,,{dev}")
        erro_zabbix = "zabbix_sender -z ==ENDERECO_IP_ZABBIX== -s Projeto_Switch_Netbox -k Trap_Erros_Vizinhos -o \"" + dev + " - NENHUMA LIGAÇÃO encontrada no CMDB\""
        os.system(erro_zabbix)
        # print(f'NENHUM CMDB: {dev}')
        cont_erros += 1
        return texto
    # print(cabos_conectados)
    # print()
    # print(res)
    # print()
    # print()
    # Remover Vizinhos Ruckus
    for lldp in res[:]:
        # Verifica se um AP Ruckus está identificado como vizinho no LLDP
        if 'Ruckus' in lldp['remoto_system_desc']:
            #Varre os cabos conectados no CMDB
            for vizinho_cmdb in cabos_conectados[:]:
                # Procura a mesma porta identificada no LLDP
                #print('AP PROCURA')
                if vizinho_cmdb['termination_a']['name'].replace('Gig ','GigabitEthernet').replace('Eth ','Ethernet').replace('Ten-Gig ','Ten-GigabitEthernet') == lldp['local_porta']:
                    # Compara os modelos dos APS encontrados no LLDP e CMDB
                    # print(f'AP LADO A - {dev}')
                    if vizinho_cmdb['termination_b']['device']['name'].split('-')[0] != re.findall(r"\b[R|T]\d+[a-zA-Z]*\b", lldp['remoto_system_desc'])[0]:
                        #texto += "AP VIZINHO LLDP inconsistente. IP: " + dev + ", Vizinho: " + str(lldp['remoto_sysname']) + ", Vizinho esperado: " + str(vizinho_cmdb) + ".\n"
                        texto += "AP VIZINHO LLDP inconsistente. IP: " + dev + ", Vizinho esperado: " + str(vizinho_cmdb['termination_b']['device']['name']) + "-https://cmdb.info.ufrn.br/dcim/devices/" + str(vizinho_cmdb['termination_b']['device']['id']) + ", Vizinho encontrado: " + str(lldp['remoto_sysname']) + "-10" + str(lldp['remoto_ipv4']) + ".\n"
                        #logging.warning(f"FALHA,AP VIZINHO LLDP inconsistente. Vizinho: {str(lldp).replace(',',';')}. Vizinho esperado: {str(vizinho_cmdb).replace(',',';')},{dev}")
                        logging.warning(f"FALHA,AP VIZINHO inconsistente,{vizinho_cmdb['termination_b']['device']['name']}-https://cmdb.info.ufrn.br/dcim/devices/{vizinho_cmdb['termination_b']['device']['id']},{lldp['remoto_sysname']}-10{lldp['remoto_ipv4']},{dev}")
                        erro_zabbix = "zabbix_sender -z ==ENDERECO_IP_ZABBIX== -s Projeto_Switch_Netbox -k Trap_Erros_Vizinhos -o \"" + dev + " - AP VIZINHO inconsistente. Vizinho esperado: " + str(vizinho_cmdb['termination_b']['device']['name']) + "-https://cmdb.info.ufrn.br/dcim/devices/" + str(vizinho_cmdb['termination_b']['device']['id']) + ", Vizinho encontrado: " + str(lldp['remoto_sysname']) + "-10" + str(lldp['remoto_ipv4']) + "\""
                        os.system(erro_zabbix)
                        # print(f'ERRO RUCKUS: {dev}')
                        # # Adiciona os incorretos as variáveis temporárias de erro
                        # erros_lldp_temp.append(lldp)
                        # erros_cmdb_temp.append(vizinho_cmdb)
                        # Remove item das listas
                        res.remove(lldp)
                        #cabos_conectados.remove(vizinho_cmdb)
                        cont_erros += 1
                    else:
                        # print(f'AP VIZINHO VALIDADO - {dev}')
                        logging.warning(f"SUCESSO,AP VIZINHO validado,{vizinho_cmdb['termination_b']['device']['name']}-https://cmdb.info.ufrn.br/dcim/devices/{vizinho_cmdb['termination_b']['device']['id']},{lldp['remoto_sysname']}-10{lldp['remoto_ipv4']},{dev}")
                        # Remove item das listas
                        res.remove(lldp)
                        cabos_conectados.remove(vizinho_cmdb)
                        break
                    # Caso não encontre, loga mensagem de erro
                    if vizinho_cmdb['termination_b']['device']['name'].split('-')[0] != re.findall(r"\b[R|T]\d+[a-zA-Z]*\b", lldp['remoto_system_desc'])[0]:
                        # Sai do loop caso encontre 2530 no nome o device
                        if '2530' in vizinho_cmdb['termination_b']['device']['name']:
                            break
                        #texto += "AP VIZINHO CMDB não encontrado no LLDP. IP: " + dev + ", Vizinho: " + str(vizinho_cmdb) + ".\n"
                        texto += "AP VIZINHO CMDB não encontrado no LLDP. IP: " + dev + ", Vizinho: " + str(vizinho_cmdb['termination_b']['device']['name']) + "-https://cmdb.info.ufrn.br/dcim/devices/" + str(vizinho_cmdb['termination_b']['device']['id']) + ".\n"
                        # print(f'NO MATCH - {dev}')
                        # print(str(vizinho_lldp).replace(',',';'))
                        logging.warning(f"FALHA,AP VIZINHO CMDB não encontrado no LLDP,{vizinho_cmdb['termination_b']['device']['name']}-https://cmdb.info.ufrn.br/dcim/devices/{vizinho_cmdb['termination_b']['device']['id']},,{dev}")
                        erro_zabbix = "zabbix_sender -z ==ENDERECO_IP_ZABBIX== -s Projeto_Switch_Netbox -k Trap_Erros_Vizinhos -o \"" + dev + " - AP VIZINHO CMDB não encontrado no LLDP. Vizinho: " + str(vizinho_cmdb['termination_b']['device']['name']) + "-https://cmdb.info.ufrn.br/dcim/devices/" + str(vizinho_cmdb['termination_b']['device']['id']) + "\""
                        os.system(erro_zabbix)
                        cont_erros += 1
                        break
                if vizinho_cmdb['termination_b']['name'].replace('Gig ','GigabitEthernet').replace('Eth ','Ethernet').replace('Ten-Gig ','Ten-GigabitEthernet') == lldp['local_porta']:
                    # Compara os modelos dos APS encontrados no LLDP e CMDB
                    # print(f'AP LADO B - {dev}')
                    if vizinho_cmdb['termination_a']['device']['name'].split('-')[0] != re.findall(r"\b[R|T]\d+[a-zA-Z]*\b", lldp['remoto_system_desc'])[0]:
                        texto += "AP VIZINHO LLDP inconsistente. IP: " + dev + ", Vizinho esperado: " + str(vizinho_cmdb['termination_a']['device']['name']) + "-https://cmdb.info.ufrn.br/dcim/devices/" + str(vizinho_cmdb['termination_a']['device']['id']) + ", Vizinho encontrado: " + str(lldp['remoto_sysname']) + "-10" + str(lldp['remoto_ipv4']) + ".\n"
                        logging.warning(f"FALHA,AP VIZINHO inconsistente,{vizinho_cmdb['termination_a']['device']['name']}-https://cmdb.info.ufrn.br/dcim/devices/{vizinho_cmdb['termination_a']['device']['id']},{lldp['remoto_sysname']}-10{lldp['remoto_ipv4']},{dev}")
                        erro_zabbix = "zabbix_sender -z ==ENDERECO_IP_ZABBIX== -s Projeto_Switch_Netbox -k Trap_Erros_Vizinhos -o \"" + dev + " - AP VIZINHO LLDP inconsistente. Vizinho esperado: " + str(vizinho_cmdb['termination_a']['device']['name']) + "-https://cmdb.info.ufrn.br/dcim/devices/" + str(vizinho_cmdb['termination_a']['device']['id']) + ", Vizinho encontrado: " + str(lldp['remoto_sysname']) + "-10" + str(lldp['remoto_ipv4']) + "\""
                        os.system(erro_zabbix)
                        # print(f'ERRO RUCKUS: {dev}')
                        # # Adiciona os incorretos as variáveis temporárias de erro
                        # erros_lldp_temp.append(lldp)
                        # erros_cmdb_temp.append(vizinho_cmdb)
                        # Remove item das listas
                        res.remove(lldp)
                        #cabos_conectados.remove(vizinho_cmdb)
                        cont_erros += 1
                    else:
                        # print(f'AP VIZINHO VALIDADO - {dev}')
                        logging.warning(f"SUCESSO,AP VIZINHO validado,{vizinho_cmdb['termination_a']['device']['name']}-https://cmdb.info.ufrn.br/dcim/devices/{vizinho_cmdb['termination_a']['device']['id']},{lldp['remoto_sysname']}-10{lldp['remoto_ipv4']},{dev}")
                        # Remove item das listas
                        res.remove(lldp)
                        cabos_conectados.remove(vizinho_cmdb)
                        break
                    # Caso não encontre, loga mensagem de erro
                    if vizinho_cmdb['termination_a']['device']['name'].split('-')[0] != re.findall(r"\b[R|T]\d+[a-zA-Z]*\b", lldp['remoto_system_desc'])[0]:
                        # print(lldp['remoto_system_desc'])
                        # print(vizinho_cmdb['termination_b']['device']['name'].split('-')[0])
                        # print()
                        # Sai do loop caso encontre 2530 no nome o device
                        if '2530' in vizinho_cmdb['termination_a']['device']['name']:
                            break
                        texto += "AP VIZINHO CMDB não encontrado no LLDP. IP: " + dev + ", Vizinho: " + str(vizinho_cmdb['termination_a']['device']['name']) + "-https://cmdb.info.ufrn.br/dcim/devices/" + str(vizinho_cmdb['termination_a']['device']['id']) + ".\n"
                        # print(f'NO MATCH - {dev}')
                        # print(str(vizinho_lldp).replace(',',';'))
                        logging.warning(f"FALHA,AP VIZINHO CMDB não encontrado no LLDP,{vizinho_cmdb['termination_a']['device']['name']}-https://cmdb.info.ufrn.br/dcim/devices/{vizinho_cmdb['termination_a']['device']['id']},,{dev}")
                        erro_zabbix = "zabbix_sender -z ==ENDERECO_IP_ZABBIX== -s Projeto_Switch_Netbox -k Trap_Erros_Vizinhos -o \"" + dev + " - AP VIZINHO CMDB não encontrado no LLDP. Vizinho: " + str(vizinho_cmdb['termination_a']['device']['name']) + "-https://cmdb.info.ufrn.br/dcim/devices/" + str(vizinho_cmdb['termination_a']['device']['id']) + "\""
                        os.system(erro_zabbix)
                        cont_erros += 1
                        break
    # Remover demais vizinhos
    # Cicla pela resposta do CMDB
    for vizinho_cmdb in cabos_conectados[:]:
        # Verifica se o nome do ativo testado está no lado A ou B da resposta do CMDB
        if vizinho_cmdb['termination_a']['device']['name'] == ativo_nome:
            # Chama a função de teste com o parˆsmetro 'termination_b', indicando que o vizinho está no lado B
            # print(f'LADO A - {dev}')
            for vizinho_lldp in res[:]:
                if vizinho_cmdb['termination_b']['device']['name'] == vizinho_lldp['remoto_sysname']:
                    # print('MATCH')
                    # Valida o identificador da porta remota
                    if vizinho_lldp['remoto_port_id'] == vizinho_cmdb['termination_b']['name'].replace('Gig ','GigabitEthernet').replace('Eth ','Ethernet').replace('Ten-Gig ','Ten-GigabitEthernet'):
                        # print('VIZINHO VALIDADO')
                        # Remove vizinho da lista do LLDP
                        # print('A VALIDADO')
                        logging.warning(f"SUCESSO,VIZINHO LLDP validado,{vizinho_cmdb['termination_b']['device']['name']}-https://cmdb.info.ufrn.br/dcim/devices/{vizinho_cmdb['termination_b']['device']['id']},{vizinho_lldp['remoto_sysname']}-10{vizinho_lldp['remoto_ipv4']},{dev}")
                        res.remove(vizinho_lldp)
                        cabos_conectados.remove(vizinho_cmdb)
                        break
                    else:
                        # print('ERRO')
                        # print(f"LLDP: {vizinho_lldp['remoto_port_id']}")
                        # print(str(vizinho_lldp))
                        # print(vizinho_cmdb['termination_a']['name'].replace('Gig ','GigabitEthernet').replace('Eth ','Ethernet').replace('Ten-Gig ','Ten-GigabitEthernet'))
                        #texto += "VIZINHO LLDP inconsistente. IP: " + dev + ", Vizinho: " + str(vizinho_lldp) + ", Vizinho esperado: " + str(vizinho_cmdb) + ".\n"
                        texto += "VIZINHO LLDP inconsistente. IP: " + dev + ", Vizinho esperado: " + str(vizinho_cmdb['termination_b']['device']['name']) + "-https://cmdb.info.ufrn.br/dcim/devices/" + str(vizinho_cmdb['termination_b']['device']['id']) + ", Vizinho encontrado: " + str(vizinho_lldp['remoto_sysname']) + "-10" + str(vizinho_lldp['remoto_ipv4']) + ".\n"
                        #logging.warning(f"FALHA,VIZINHO LLDP inconsistente. Vizinho: {str(vizinho_lldp).replace(',',';')}. Vizinho esperado: {str(vizinho_cmdb).replace(',',';')},{dev}")
                        logging.warning(f"FALHA,VIZINHO LLDP inconsistente,{vizinho_cmdb['termination_b']['device']['name']}-https://cmdb.info.ufrn.br/dcim/devices/{vizinho_cmdb['termination_b']['device']['id']},{vizinho_lldp['remoto_sysname']}-10{lldp['remoto_ipv4']},{dev}")
                        erro_zabbix = "zabbix_sender -z ==ENDERECO_IP_ZABBIX== -s Projeto_Switch_Netbox -k Trap_Erros_Vizinhos -o \"" + dev + " - VIZINHO LLDP inconsistente. Vizinho esperado: " + str(vizinho_cmdb['termination_b']['device']['name']) + "-https://cmdb.info.ufrn.br/dcim/devices/" + str(vizinho_cmdb['termination_b']['device']['id']) + ", Vizinho encontrado: " + str(vizinho_lldp['remoto_sysname']) + "-10" + str(vizinho_lldp['remoto_ipv4']) + "\""
                        os.system(erro_zabbix)
                        # print(f'ERRO VIZINHO: {dev}')
                        # # Adiciona os incorretos as variáveis temporárias de erro
                        # erros_lldp_temp.append(vizinho_lldp)
                        # erros_cmdb_temp.append(vizinho_cmdb)
                        # Remove item das listas
                        # print('A INCONSISTENTE')
                        # print(vizinho_lldp)
                        # print(vizinho_cmdb)
                        res.remove(vizinho_lldp)
                        cabos_conectados.remove(vizinho_cmdb)
                        cont_erros += 1
                        break
            else:
                #texto += "VIZINHO CMDB não encontrado no LLDP. IP: " + dev + ", Vizinho: " + str(vizinho_cmdb) + ".\n"
                texto += "VIZINHO CMDB não encontrado no LLDP. IP: " + dev + ", Vizinho: " + str(vizinho_cmdb['termination_b']['device']['name']) + "-https://cmdb.info.ufrn.br/dcim/devices/" + str(vizinho_cmdb['termination_b']['device']['id']) + ".\n"
                # print(f'NO MATCH - {dev}')
                # print(str(vizinho_lldp).replace(',',';'))
                #logging.warning(f"FALHA,VIZINHO CMDB não encontrado no LLDP. Vizinho: {str(vizinho_cmdb).replace(',',';')},{dev}")
                logging.warning(f"FALHA,VIZINHO CMDB não encontrado no LLDP,{vizinho_cmdb['termination_b']['device']['name']}-{vizinho_cmdb['termination_b']['device']['url']},,{dev}")
                erro_zabbix = "zabbix_sender -z ==ENDERECO_IP_ZABBIX== -s Projeto_Switch_Netbox -k Trap_Erros_Vizinhos -o \"" + dev + " - VIZINHO CMDB não encontrado no LLDP. Vizinho: " + str(vizinho_cmdb['termination_b']['device']['name']) + "-https://cmdb.info.ufrn.br/dcim/devices/" + str(vizinho_cmdb['termination_b']['device']['id']) + "\""
                os.system(erro_zabbix)
                cont_erros += 1
                # # Adiciona os incorretos as variáveis temporárias de erro
                # erros_cmdb_temp.append(vizinho_cmdb)
                # Remove item das listas
                # print('A NAO ENONTRADO')
                #cabos_conectados.remove(vizinho_cmdb)
                # print(f'NO MATCH - {dev}')
        if vizinho_cmdb['termination_b']['device']['name'] == ativo_nome:
            # Chama a função de teste com o parˆsmetro 'termination_a', indicando que o vizinho está no lado A
            # print(f'LADO B - {dev}')
            for vizinho_lldp in res[:]:
                if vizinho_cmdb['termination_a']['device']['name'] == vizinho_lldp['remoto_sysname']:
                    # print('MATCH')
                    # Valida o identificador da porta remota
                    if vizinho_lldp['remoto_port_id'] == vizinho_cmdb['termination_a']['name'].replace('Gig ','GigabitEthernet').replace('Eth ','Ethernet').replace('Ten-Gig ','Ten-GigabitEthernet'):
                        # print('VIZINHO VALIDADO')
                        # Remove vizinho da lista do LLDP
                        # print('B VALIDADO')
                        # print(vizinho_cmdb)
                        # print(cabos_conectados)
                        logging.warning(f"SUCESSO,VIZINHO LLDP validado,{vizinho_cmdb['termination_a']['device']['name']}-https://cmdb.info.ufrn.br/dcim/devices/{vizinho_cmdb['termination_a']['device']['id']},{vizinho_lldp['remoto_sysname']}-10{lldp['remoto_ipv4']},{dev}")
                        # print()
                        res.remove(vizinho_lldp)
                        cabos_conectados.remove(vizinho_cmdb)
                        break
                    else:
                        # print('ERRO')
                        # print(f"LLDP: {vizinho_lldp['remoto_port_id']}")
                        # print(str(vizinho_lldp))
                        # print(vizinho_cmdb['termination_a']['name'].replace('Gig ','GigabitEthernet').replace('Eth ','Ethernet').replace('Ten-Gig ','Ten-GigabitEthernet'))
                        #texto += "VIZINHO LLDP inconsistente. IP: " + dev + ", Vizinho: " + str(vizinho_lldp) + ", Vizinho esperado: " + str(vizinho_cmdb) + ".\n"
                        texto += "VIZINHO LLDP inconsistente. IP: " + dev + ", Vizinho esperado: " + str(vizinho_cmdb['termination_a']['device']['name']) + "-https://cmdb.info.ufrn.br/dcim/devices/" + str(vizinho_cmdb['termination_a']['device']['id']) + ", Vizinho encontrado: " + str(vizinho_lldp['remoto_sysname']) + "-10" + str(vizinho_lldp['remoto_ipv4']) + ".\n"
                        logging.warning(f"FALHA,VIZINHO LLDP inconsistente,{vizinho_cmdb['termination_a']['device']['name']}-https://cmdb.info.ufrn.br/dcim/devices/{vizinho_cmdb['termination_a']['device']['id']},{vizinho_lldp['remoto_sysname']}-10{lldp['remoto_ipv4']},{dev}")
                        erro_zabbix = "zabbix_sender -z ==ENDERECO_IP_ZABBIX== -s Projeto_Switch_Netbox -k Trap_Erros_Vizinhos -o \"" + dev + " - VIZINHO LLDP inconsistente. Vizinho esperado: " + str(vizinho_cmdb['termination_a']['device']['name']) + "-https://cmdb.info.ufrn.br/dcim/devices/" + str(vizinho_cmdb['termination_a']['device']['id']) + ", Vizinho encontrado: " + str(vizinho_lldp['remoto_sysname']) + "-10" + str(vizinho_lldp['remoto_ipv4']) + "\""
                        os.system(erro_zabbix)
                        # print(f'ERRO VIZINHO: {dev}')
                        # # Adiciona os incorretos as variáveis temporárias de erro
                        # erros_lldp_temp.append(vizinho_lldp)
                        # erros_cmdb_temp.append(vizinho_cmdb)
                        # Remove item das listas
                        # print('B INCONSISTENTE')
                        res.remove(vizinho_lldp)
                        cabos_conectados.remove(vizinho_cmdb)
                        cont_erros += 1
                        break
            else:
                #texto += "VIZINHO CMDB não encontrado no LLDP. IP: " + dev + ", Vizinho: " + str(vizinho_cmdb) + ".\n"
                texto += "VIZINHO CMDB não encontrado no LLDP. IP: " + dev + ", Vizinho: " + str(vizinho_cmdb['termination_a']['device']['name']) + "-https://cmdb.info.ufrn.br/dcim/devices/" + str(vizinho_cmdb['termination_a']['device']['id']) + ".\n"
                # print(f'NO MATCH - {dev}')
                # print(str(vizinho_lldp).replace(',',';'))
                logging.warning(f"FALHA,VIZINHO CMDB não encontrado no LLDP,{vizinho_cmdb['termination_a']['device']['name']}-{vizinho_cmdb['termination_a']['device']['url']},,{dev}")
                erro_zabbix = "zabbix_sender -z ==ENDERECO_IP_ZABBIX== -s Projeto_Switch_Netbox -k Trap_Erros_Vizinhos -o \"" + dev + " - VIZINHO CMDB não encontrado no LLDP. Vizinho: " + str(vizinho_cmdb['termination_a']['device']['name']) + "-https://cmdb.info.ufrn.br/dcim/devices/" + str(vizinho_cmdb['termination_a']['device']['id']) + "\""
                os.system(erro_zabbix)
                cont_erros += 1
                # # Adiciona os incorretos as variáveis temporárias de erro
                # erros_cmdb_temp.append(vizinho_cmdb)
                # # Remove item das listas
                # print('B NAO ENCONTRADO')
                # print(vizinho_cmdb)
                # print()
                # print()
                #cabos_conectados.remove(vizinho_cmdb)
                # print(f'NO MATCH - {dev}')
        #print()
    #print(res)
    #print(f"erros: {cont_erros}")
    # # Verificar tamanho da lista da consulta CMDB
    # if len(erros_cmdb_temp) > 0:
    #     texto += "VIZINHO(S) RESTANTE(S) NO CMDB. IP: " + dev + ", Vizinho(s) restantes(s): " + str(erros_cmdb_temp) + ".\n"
    #     logging.warning(f"FALHA,VIZINHO(S) RESTANTE(S) NO CMDB. Total: {len(erros_cmdb_temp)}. Vizinho(s) restantes(s): {str(erros_cmdb_temp).replace(',',';')},{dev}")
    #     # print(f'SOBRA CMDB: {dev}')
    #     cont_erros += 1
    # Verificar tamanho da lista da consulta LLDP
    if len(res) > 0:
        for vizinho_lldp in res:
            #texto += "VIZINHO LLDP não encontrado no CMDB. IP: " + dev + ", Vizinho restantes: " + str(vizinho_lldp) + ".\n"
            texto += "VIZINHO LLDP não encontrado no CMDB. IP: " + dev + ", Vizinho restantes: " + str(vizinho_lldp['remoto_sysname']) + "-10" + str(vizinho_lldp['remoto_ipv4']) + ".\n"
#            logging.warning(f"FALHA,VIZINHO LLDP não encontrado no CMDB. Vizinho restantes: {str(vizinho_lldp).replace(',',';')},,,{dev}")
            logging.warning(f"FALHA,VIZINHO LLDP não encontrado no CMDB,,{vizinho_lldp['remoto_sysname']}-10{vizinho_lldp['remoto_ipv4']},{dev}")
            erro_zabbix = "zabbix_sender -z ==ENDERECO_IP_ZABBIX== -s Projeto_Switch_Netbox -k Trap_Erros_Vizinhos -o \"" + dev + " - VIZINHO LLDP não encontrado no CMDB. Vizinho restantes: " + str(vizinho_lldp['remoto_sysname']) + "-10" + str(vizinho_lldp['remoto_ipv4']) + "\""
            os.system(erro_zabbix)
            # print(f'SOBRA LLDP: {dev}')
            cont_erros += 1
    # Imprime mensagem de sucesso caso não tenha encontrado nenhum erro
    # print(f"{cont_erros} - {dev}")
    if cont_erros == 0:
        logging.warning(f"SUCESSO,Vizinhos LLDP homologados com o CMDB,,,{dev}")
    else:
        logging.warning(f"FALHA,Vizinhos LLDP inconsistentes com o CMDB,,,{dev}")
    # print(f"erros: {cont_erros}")
    return texto


# def testar_vizinho_switch(dev, vizinho_cmdb, lado_vizinho_cmdb, res, cabos_conectados):
#     # TEMPORARIAMENTE SEM USO
#     # Variável de retorno
#     texto_retorno = ''
#     cont_retorno = 0
#     # Compara com o coletado no ativo
#     # Identifica os vizinhos pelo sysname remoto
#     for vizinho_lldp in res[:]:
#         if vizinho_cmdb[lado_vizinho_cmdb]['device']['name'] == vizinho_lldp['remoto_sysname']:
#             print('MATCH')
#             # Valida o identificador da porta remota
#             if vizinho_lldp['remoto_port_id'] != vizinho_cmdb[lado_vizinho_cmdb]['name'].replace('Gig ','GigabitEthernet').replace('Eth ','Ethernet').replace('Ten-Gig ','Ten-GigabitEthernet'):
#                 texto_retorno += "VIZINHO LLDP inconsistente. IP: " + dev + ", Vizinho: " + vizinho_lldp + ", Vizinho esperado: " + vizinho_cmdb + ".\n"
#                 log_ex.warning(f"FALHA,VIZINHO LLDP inconsistente. Vizinho: {vizinho_lldp}. Vizinho esperado: {vizinho_cmdb},{dev}")
#                 print(f'ERRO VIZINHO: {dev}')
#                 cont_retorno += 1
#                 # Remove vizinho da lista do LLDP
#                 res.remove(vizinho_lldp)
#                 cabos_conectados.remove(vizinho_cmdb)
#                 print(texto_retorno)
#                 print(cont_retorno)
#                 return texto_retorno, cont_retorno
#             else:
#                 #print('VIZINHO VALIDADO')
#                 # Remove vizinho da lista do LLDP
#                 #res.remove(vizinho_lldp)
#                 res.remove(vizinho_lldp)
#                 cabos_conectados.remove(vizinho_cmdb)
#                 print(texto_retorno)
#                 print(cont_retorno)
#                 return texto_retorno, cont_retorno
#         else:
#             texto_retorno += "VIZINHO LLDP não encontrado. IP: " + dev + ", Vizinho: " + vizinho_lldp + ".\n"
#             log_ex.warning(f"FALHA,VIZINHO LLDP não encontrado. Vizinho: {vizinho_lldp},{dev}")
#             cont_retorno += 1
#             print(f'NO MATCH - {dev}')
#     print('END FOR')
#     print(texto_retorno)
#     print(cont_retorno)
#     return texto_retorno, cont_retorno


# show interfaces brief
ttp_sh_int_br = "  {{interface}}     {{interface_tipo}} | {{interface_alerta}}        {{interface_enable}}     {{interface_status}}   {{interface_modo}}    {{interface_mdi_modo}}  {{interface_flow_control}}"
# show interfaces
ttp_show_interfaces = "  {{interface}}          {{total_bytes}}              {{total_frames}}              {{erros_rx}}            {{drops_tx}}            {{interface_flow_control}}"
def validar_links_ativos(net_connect, dev, cabos_conectados, ativo_nome, log_ex, log_dat):
    # Variável de retorno
    texto = ''
    cont_erros = 0
    # Templates TTP
    # Acima da função
    # Aplicando o template a resposta do ativo
    # Verificando interfaces
    parser = ttp(data=net_connect.send_command("show interfaces brief"), template=ttp_sh_int_br, log_level='CRITICAL')
    parser.parse()
    res = parser.result()
    res = res[0][0]
    # Lista os cabos conectados no CMDB
    for vizinho_cmdb in cabos_conectados[:]:
        # Lista os dados das interfaces do ativo
        for interf in res:
            # Desconsidera o cabeçalho da tabela gerada pelo ativo
            if 'ort' in interf['interface']:
                continue
            # Confirma o lado que está o ativo
            if vizinho_cmdb['termination_a']['device']['name'] == ativo_nome:
                # Identifica a interface
                if interf['interface'] == vizinho_cmdb['termination_a']['name']:
                    texto_temp = ''
                    cont_temp = 0
                    texto_temp,cont_temp = validar_status_links(dev, interf, log_ex, log_dat)
                    texto += texto_temp
                    cont_erros += cont_temp
            # Confirma o lado que está o ativo
            if vizinho_cmdb['termination_b']['device']['name'] == ativo_nome:
                # Identifica a interface
                if interf['interface'] == vizinho_cmdb['termination_b']['name']:
                    texto_temp = ''
                    cont_temp = 0
                    texto_temp,cont_temp = validar_status_links(dev, interf, log_ex, log_dat)
                    texto += texto_temp
                    cont_erros += cont_temp
    # Imprime mensagem caso não tenham sido encontrados erros
    if cont_erros == 0:
        log_ex.warning(f"SUCESSO,Todos os enlaces ativos,{dev}")
        log_dat.warning(f"SUCESSO,Todos os enlaces ativos,,{dev}")
    return texto


def validar_status_links(dev, int, log_e, log_da):
    # Variável de retorno
    texto_retorno = ''
    cont_retorno = 0
    # Verifica se a interface está desabilitada
    try:
        if int['interface_enable'] != 'Yes':
            texto_retorno += "Interface ENTRE ATIVOS DESABILITADA. IP: " + dev + ", Interface: " + str(int['interface']) + ".\n"
            log_e.warning(f"FALHA,Interface ENTRE ATIVOS DESABILITADA. Interface: {int['interface']},{dev}")
            log_da.warning(f"FALHA,Interface ENTRE ATIVOS DESABILITADA,{int['interface']},{dev}")
            erro_zabbix = "zabbix_sender -z ==ENDERECO_IP_ZABBIX== -s Projeto_Switch_Netbox -k Trap_Erros_Estado_Enlaces -o \"" + dev + " - Interface ENTRE ATIVOS DESABILITADA. Interface: " + str(int['interface']) + "\""
            os.system(erro_zabbix)
            cont_retorno += 1
            return texto_retorno, cont_retorno
    except Exception:
        texto_retorno += "Não foi possível validar o STATUS da interface entre ativos: ENABLED. IP: " + dev + ", Interface: " + str(int['interface']) + ".\n"
        log_e.warning(f"FALHA,Não foi possível validar o STATUS da interface entre ativos: ENABLED. Interface: {int['interface']},{dev}")
        log_da.warning(f"FALHA,Não foi possível validar o STATUS da interface entre ativos: ENABLED,{int['interface']},{dev}")
        erro_zabbix = "zabbix_sender -z ==ENDERECO_IP_ZABBIX== -s Projeto_Switch_Netbox -k Trap_Erros_Estado_Enlaces -o \"" + dev + " - Não foi possível validar o STATUS da interface entre ativos ENABLED. Interface: " + str(int['interface']) + "\""
        os.system(erro_zabbix)
        cont_retorno += 1
        return texto_retorno, cont_retorno
    # Verifica se a interface está DOWN
    try:
        if int['interface_status'] != 'Up':
            texto_retorno += "Interface ENTRE ATIVOS DOWN. IP: " + dev + ", Interface: " + str(int['interface']) + ".\n"
            log_e.warning(f"FALHA,Interface ENTRE ATIVOS DOWN. Interface: {int['interface']},{dev}")
            log_da.warning(f"FALHA,Interface ENTRE ATIVOS DOWN,{int['interface']},{dev}")
            erro_zabbix = "zabbix_sender -z ==ENDERECO_IP_ZABBIX== -s Projeto_Switch_Netbox -k Trap_Erros_Estado_Enlaces -o \"" + dev + " - Interface ENTRE ATIVOS DOWN. Interface: " + str(int['interface']) + "\""
            os.system(erro_zabbix)
            cont_retorno += 1
            return texto_retorno, cont_retorno
    except Exception:
        texto_retorno += "Não foi possível validar o STATUS da interface entre ativos: STATUS. IP: " + dev + ", Interface: " + str(int['interface']) + ".\n"
        log_e.warning(f"Não foi possível validar o STATUS da interface entre ativos: STATUS. Interface: {int['interface']},{dev}")
        log_da.warning(f"FALHA,Não foi possível validar o STATUS da interface entre ativos: STATUS,{int['interface']},{dev}")
        erro_zabbix = "zabbix_sender -z ==ENDERECO_IP_ZABBIX== -s Projeto_Switch_Netbox -k Trap_Erros_Estado_Enlaces -o \"" + dev + " - Não foi possível validar o STATUS da interface entre ativos STATUS. Interface: " + str(int['interface']) + "\""
        os.system(erro_zabbix)
        cont_retorno += 1
        return texto_retorno, cont_retorno
    # Verifica se a interface está com a transerência correta
    if 'interface_tipo' not in int.keys():
        texto_retorno += "Não foi possível validar o STATUS da interface entre ativos: TIPO. IP: " + dev + ", Interface: " + str(int['interface']) + ".\n"
        log_e.warning(f"Não foi possível validat o STATUS da interface entre ativos: TIPO. Interface: {int['interface']},{dev}")
        log_da.warning(f"FALHA,Não foi possível validat o STATUS da interface entre ativos: TIPO,{int['interface']},{dev}")
        erro_zabbix = "zabbix_sender -z ==ENDERECO_IP_ZABBIX== -s Projeto_Switch_Netbox -k Trap_Erros_Estado_Enlaces -o \"" + dev + " - Interface ENTRE ATIVOS TIPO. Interface: " + str(int['interface']) + "\""
        os.system(erro_zabbix)
        cont_retorno += 1
        return texto_retorno, cont_retorno
    int['interface_tipo'] = int['interface_tipo'].split('/')[-1]
    try:
        if int['interface_modo'][:-3] != int['interface_tipo'][:-1]:
            texto_retorno += "Interface ENTRE ATIVOS DOWN. IP: " + dev + ", Interface: " + str(int['interface']) + ".\n"
            log_e.warning(f"FALHA,Interface ENTRE ATIVOS DOWN. Interface: {int['interface']},{dev}")
            log_da.warning(f"FALHA,Interface ENTRE ATIVOS DOWN,{int['interface']},{dev}")
            erro_zabbix = "zabbix_sender -z ==ENDERECO_IP_ZABBIX== -s Projeto_Switch_Netbox -k Trap_Erros_Estado_Enlaces -o \"" + dev + " - Interface ENTRE ATIVOS DOWN. Interface: " + str(int['interface']) + "\""
            os.system(erro_zabbix)
            cont_retorno += 1
            return texto_retorno, cont_retorno
    except Exception:
        texto_retorno += "Não foi possível validar o STATUS da interface entre ativos: ENLACE. IP: " + dev + ", Interface: " + str(int['interface']) + ".\n"
        log_e.warning(f"Não foi possível validar o STATUS da interface entre ativos: ENLACE. Interface: {int['interface']},{dev}")
        log_da.warning(f"Não foi possível validar o STATUS da interface entre ativos: ENLACE,{int['interface']},{dev}")
        erro_zabbix = "zabbix_sender -z ==ENDERECO_IP_ZABBIX== -s Projeto_Switch_Netbox -k Trap_Erros_Estado_Enlaces -o \"" + dev + " - Não foi possível validar o STATUS da interface entre ativos: ENLACE. Interface: " + str(int['interface']) + "\""
        os.system(erro_zabbix)
        cont_retorno += 1
        return texto_retorno, cont_retorno
    return texto_retorno, cont_retorno


# show mac-address detail
ttp_sh_mac_add = "  {{mac_add}} {{mac_porta}}    {{mac_vlan}}  {{mac_age}}"
def encontrar_mac(net_connect, ip_add, mac):
    # Variavel de retorno
    texto = ''
    # Templates TTP
    # Acima da função
    # Aplicando o template a resposta do ativo
    # Verificando vizinhos via LLDP no switch
    parser = ttp(data=net_connect.send_command("show mac-address detail"), template=ttp_sh_mac_add, log_level='CRITICAL')
    parser.parse()
    res = parser.result()
    res = res[0][0]
    # Encontrando a porta de UPLINK e DERIVAÇÃO
    interfaces = net_connect.send_command("show running-config interface")
    # Encontrando a porta de UPLINK, DERIVAÇÃO E RUCKUS
    # Dividir a configuração por blocos de interface
    interfaces = interfaces.strip().split("interface ")    
    # Armazenar interfaces de uplink
    links = []
    # Processar cada bloco
    for bloco in interfaces:
        if bloco.strip():  # Ignorar linhas vazias
            linhas = bloco.strip().split("\n")
            nome_interface = linhas[0].strip()  # Nome da interface
            # Verificar UPLINK na string'
            if any("UPLINK" in linha.upper() for linha in linhas):
                links.append(nome_interface)
            if any("DERIVACAO" in linha.upper() for linha in linhas):
                links.append(nome_interface)
    # Cicla pelos MACS encontrados no ativo
    for consulta in res:
        # Cerifica se o MAC encontrado é igual ao esperado
        if consulta['mac_add'].replace(':', '').replace('-', '').upper() == mac:
            # Verifica se a interface é de enlace com outroa ativos
            if consulta['mac_porta'] not in links:
                texto += "Endereço encontrado. IP: " + ip_add + ", Porta: " + consulta['mac_porta'] + ", VLAN: " + consulta['mac_vlan'] + '.\n'
                logging.warning(f"SUCESSO,Endereço encontrado. Porta: {consulta['mac_porta']}. VLAN: {consulta['mac_vlan']},{ip_add}")
                return texto
    logging.warning(f"FALHA,Nenhum endereço encontrado,{ip_add}")
    return texto


# show interfaces all
ttp_show_interfaces_all = """
 Status and Counters - Port Counters for port {{interface_number}}

  Name  : {{interface_name}}
  MAC Address      : {{interface_mac}}
  Link Status      : {{interface_link_status}}
  Port Enabled     : {{interface_port_status}}
  Totals (Since boot or last clear) :
   Bytes Rx        : {{int_total_bytes_rx}}        Bytes Tx        : {{int_total_bytes_tx}}
   Unicast Rx      : {{int_total_unic_bytes_rx}}          Unicast Tx      : {{int_total_unic_bytes_tx}}
   Bcast/Mcast Rx  : {{int_total_bcast_mcast_bytes_rx}}           Bcast/Mcast Tx  : {{int_total_bcast_mcast_bytes_tx}}
  Errors (Since boot or last clear) :
   FCS Rx          : {{int_error_fcs_rx}}                    Drops Tx        : {{int_error_drop_tx}}
   Alignment Rx    : {{int_error_aligment_rx}}                    Collisions Tx   : {{int_error_collision_tx}}
   Runts Rx        : {{int_error_runts_rx}}                    Late Colln Tx   : {{int_error_late_colis_tx}}
   Giants Rx       : {{int_error_giant_rx}}                    Excessive Colln : {{int_error_excessive_colis_tx}}
   Total Rx Errors : {{int_error_total_rx}}                    Deferred Tx     : {{int_error_deferred_tx}}
  Others (Since boot or last clear) :
   Discard Rx      : {{int_other_discard_rx}}                    Out Queue Len   : {{int_other_out_queue_len}}
   Unknown Protos  : {{int_other_unk_protocol}}
  Rates (5 minute weighted average) :
   Total Rx (bps) : {{int_rate5min_total_bytes_rx}}             Total Tx (bps) : {{int_rate5min_total_bytes_tx}}
   Unicast Rx (Pkts/sec) : {{int_rate5min_unic_pkt_sec_rx}}            Unicast Tx (Pkts/sec) : {{int_rate5min_unic_pkt_sec_tx}}
   B/Mcast Rx (Pkts/sec) : {{int_rate5min_bcast_mcast_pkt_sec_rx}}              B/Mcast Tx (Pkts/sec) : {{int_rate5min_bcast_mcast_pkt_sec_tx}}
   Utilization Rx  : {{int_rate5min_util_percent_rx}} %		  Utilization Tx  : {{int_rate5min_util_percent_tx}} %
"""
ttp_show_interfaces_all_erros = """
 Status and Counters - Port Counters for port {{interface_number}}
  Errors (Since boot or last clear) :
   FCS Rx          : {{int_error_fcs_rx}}                    Drops Tx        : {{int_error_drop_tx}}
   Alignment Rx    : {{int_error_aligment_rx}}                    Collisions Tx   : {{int_error_collision_tx}}
   Runts Rx        : {{int_error_runts_rx}}                    Late Colln Tx   : {{int_error_late_colis_tx}}
   Giants Rx       : {{int_error_giant_rx}}                    Excessive Colln : {{int_error_excessive_colis_tx}}
   Total Rx Errors : {{int_error_total_rx}}                    Deferred Tx     : {{int_error_deferred_tx}}
  Others (Since boot or last clear) :
   Discard Rx      : {{int_other_discard_rx}}                    Out Queue Len   : {{int_other_out_queue_len}}
   Unknown Protos  : {{int_other_unk_protocol}}
"""
ttp_show_interfaces_all_rate5min = """
 Status and Counters - Port Counters for port {{interface_number}}

  Name  : {{interface_name}}
  MAC Address      : {{interface_mac}}
  Link Status      : {{interface_link_status}}
  Port Enabled     : {{interface_port_status}}
  Rates (5 minute weighted average) :
   Total Rx (bps) : {{int_rate5min_total_bytes_rx}}             Total Tx (bps) : {{int_rate5min_total_bytes_tx}}
   Unicast Rx (Pkts/sec) : {{int_rate5min_unic_pkt_sec_rx}}            Unicast Tx (Pkts/sec) : {{int_rate5min_unic_pkt_sec_tx}}
   B/Mcast Rx (Pkts/sec) : {{int_rate5min_bcast_mcast_pkt_sec_rx}}              B/Mcast Tx (Pkts/sec) : {{int_rate5min_bcast_mcast_pkt_sec_tx}}
   Utilization Rx  : {{int_rate5min_util_percent_rx}} %		  Utilization Tx  : {{int_rate5min_util_percent_tx}} %
"""
def verificar_contadores_interfaces(net_connect, dev, log_ex, log_dat):
    # Variável de retorno
    texto = ''
    cont_erros = 0
    cont_reset = 0
    # Templates TTP
    # Acima da função
    # Aplicando o template a resposta do ativo
    # Verificando dados de todas as interfaces
    dados_interfaces = net_connect.send_command("show interfaces all")
    # INICIALMENTE SERÃO TRATADOS OS ERROS NAS INTERFACES
    # Lista e coleta apenas as mensagens de erro
    parser = ttp(dados_interfaces, template=ttp_show_interfaces_all_erros, log_level='CRITICAL')
    parser.parse()
    res = parser.result()
    res = res[0][0]
    # Lista entre todas as interfaces consultadas a procura dos erros
    for porta in res:
        # Obtém o identificador da interface, atribuindo o valor 'desconhecida' caso não encontre
        interface = porta.get('interface_number', 'DESCONHECIDA')
        for key, value in porta.items():
            # Ignora a chave que contém o identificador da interface
            if key == 'interface_number':
                continue
            # Verifica se o valor do erro é maior que 10
            if int(value.replace(',','')) > 50:
                    texto += "Taxa incomum de ERROS na interface " + interface + ". IP: " + dev + ". Tipo de erro: " + key + ". Valor: " + value.replace(',','') + ".\n"
                    log_ex.warning(f"FALHA,Taxa incomum de ERROS na interface {interface}. Tipo de erro: {key}. Valor: {value.replace(',','')},{dev}")
                    log_dat.warning(f"FALHA,{interface},{key},{value.replace(',','')},{dev}")
                    erro_zabbix = "zabbix_sender -z ==ENDERECO_IP_ZABBIX== -s Projeto_Switch_Netbox -k Trap_Erros_Contadores_Interfaces -o \"" + dev + " - Taxa incomum de ERROS na interface " + str(interface) + "Tipo de erro: " + str(key) + ". Valor: " + str(value.replace(',','')) + "\""
                    os.system(erro_zabbix)
                    cont_erros += 1
    # EM SEGUIDA SERÃO TRATADOS AS TAXAS DE TRANSFERÊNCIAS NOS ÚLTIMOS % MINUTOS
    # Lista e coleta apenas os dados dos últimos 5 minutos
    parser = ttp(dados_interfaces, template=ttp_show_interfaces_all_rate5min, log_level='CRITICAL')
    parser.parse()
    res = parser.result()
    res = res[0][0]
    # Lista entre todas as interfaces consultadas a procura valores fora do normal
    for porta in res:
        # Obtém o identificador da interface, atribuindo o valor 'desconhecida' caso não encontre
        interface = porta.get('interface_number', 'DESCONHECIDA')
        if int(porta['int_rate5min_util_percent_rx'][:2]) > 75:
            texto += "Taxa de DOWNLOAD ACIMA de 75% na interface " + interface + ". IP: " + dev + ". Valor: " + porta['int_rate5min_util_percent_rx'].replace(',','') + ".\n"
            log_ex.warning(f"FALHA,Taxa de DOWNLOAD ACIMA de 75% na interface {interface}. Valor: {porta['int_rate5min_util_percent_rx'].replace(',','')},{dev}")
            log_dat.warning(f"FALHA,{interface},Taxa de DOWNLOAD ACIMA de 75%,{porta['int_rate5min_util_percent_rx'].replace(',','')},{dev}")
            erro_zabbix = "zabbix_sender -z ==ENDERECO_IP_ZABBIX== -s Projeto_Switch_Netbox -k Trap_Erros_Contadores_Interfaces -o \"" + dev + " - Taxa de DOWNLOAD ACIMA de 75% na interface " + str(interface) + ". Valor: " + str(porta['int_rate5min_util_percent_rx'].replace(',','')) + "\""
            os.system(erro_zabbix)
            cont_erros += 1
        if int(porta['int_rate5min_util_percent_tx'][:2]) > 75:
            texto += "Taxa de UPLOAD ACIMA de 75% na interface " + interface + ". IP: " + dev + ". Valor: " + porta['int_rate5min_util_percent_tx'].replace(',','') + ".\n"
            log_ex.warning(f"FALHA,Taxa de UPLOAD ACIMA de 75% na interface {interface}. Valor: {porta['int_rate5min_util_percent_tx'].replace(',','')},{dev}")
            log_dat.warning(f"FALHA,{interface},Taxa de UPLOAD ACIMA de 75%,{porta['int_rate5min_util_percent_tx'].replace(',','')},{dev}")
            erro_zabbix = "zabbix_sender -z ==ENDERECO_IP_ZABBIX== -s Projeto_Switch_Netbox -k Trap_Erros_Contadores_Interfaces -o \"" + dev + " - Taxa de DOWNLOAD ACIMA de 75% na interface " + str(interface) + ". Valor: " + str(porta['int_rate5min_util_percent_tx'].replace(',','')) + "\""
            os.system(erro_zabbix)
            cont_erros += 1
    # Resetar contadores
    try:
        net_connect.send_command("clear statistics all")
    except Exception:
        texto += "ERRO ao resetar contadores das interfaces. IP: " + dev + ".\n"
        log_ex.warning(f"FALHA,ERRO ao resetar contadores das interfaces,{dev}.")
        log_dat.warning(f"FALHA,,ERRO ao resetar contadores das interfaces,,{dev}")
        erro_zabbix = "zabbix_sender -z ==ENDERECO_IP_ZABBIX== -s Projeto_Switch_Netbox -k Trap_Erros_Contadores_Interfaces -o \"" + dev + " - ERRO ao resetar contadores das interfaces\""
        os.system(erro_zabbix)
        cont_reset += 1
    # Imprime mensagens de sucesso caso não tiverem sido encontradas nenhuma anomalia nos contadores das interfaces
    if cont_erros == 0:
        texto += "SUCESSO, contadores das interfaces dentro do padrão. IP: " + dev + ".\n"
        log_ex.warning(f"SUCESSO,Contadores das interfaces dentro do padrão,{dev}")
        log_dat.warning(f"SUCESSO,,Contadores das interfaces dentro do padrão,,{dev}")
    if cont_reset == 0:
        texto += "SUCESSO, contadores das interfaces resetados. IP: " + dev + ".\n"
        log_ex.warning(f"SUCESSO,Contadores das interfaces resetados,{dev}")
        log_dat.warning(f"SUCESSO,,Contadores das interfaces resetados,,{dev}")
    return texto


# show running-config interface
ttp_sh_run_interface = """
interface {{interface_id}}
   name "{{int_descricao}}"
   tagged vlan {{ tagged_vlan | joinmatches(',') }}
   untagged vlan {{ untagged_vlan | to_int }}
"""
# show vlan custom id name:30 ipconfig
ttp_show_ip_custom_id_name_ipconfig = """
 {{vlan_id}}      {{vlan_name}}                   {{vlan_ip_config}}
"""
def validar_vlans_uplink(net_connect, dev, log_ex, log_dat):
    '''
    Verificar encaminhamento vlans:

    -listar todas as interfaces
    sh run int
    -identificar as interfaces da mesma maneira que foi feito no stp (LINHAS 244 a 258)
    -ciclar entre cada interface identificada
    -criar uma lista e ir adicionando as vlans tag e unt de cada interface (EXCETO A INTERFACE DE UPLINK)
    -listar as vlans da interface de uplink em outra lista
    -em outro loop, verificar se as vlans das portas de acesso/derivação estão na porta de uplink
    -ir retirando as vlans encontradas de cada lista [:]
    -logar as vlans restantes
    '''
    # Variável de retorno
    texto = ''
    cont_erros = 0
    # Templates TTP
    # Acima da função
    # Aplicando o template a resposta do ativo
    # Verificando interfaces
    parser = ttp(data=net_connect.send_command("show running-config interface"), template=ttp_sh_run_interface, log_level='CRITICAL')
    parser.parse()
    res = parser.result()
    res = res[0][0]
    vlans_uplink = []
    vlans_interfaces = []
    interface_uplink = 0
    vlanid_gerencia = ''
    # Cicla pelas interfaces consultadas
    for int in res:
        # Verifica se a interface possui nome (ou descrição)
        if 'int_descricao' in int.keys():
            # Identifica a interface de UPLINK
            if 'UPLINK' in int['int_descricao']:
                # Chama função para identificar a vlan e ajustar a coleta
                vlan_upl_temp = []
                # Incrementa o contador de interfaces de uplink
                interface_uplink += 1
                # Verifica se mais de uma interface está indicada como uplink
                # print(f"Int UPL {interface_uplink}")
                if interface_uplink > 1:
                    texto += "MAIS de uma interface está indicada como UPLINK. IP: " + dev + ".\n"
                    log_ex.warning(f"FALHA,MAIS de uma interface está indicada como UPLINK,{dev}")
                    log_dat.warning(f"FALHA,MAIS de uma interface está indicada como UPLINK,,{dev}")
                    # print(f"MAIS de uma interface está indicada como UPLINK. IP: {dev}")
                    erro_zabbix = "zabbix_sender -z ==ENDERECO_IP_ZABBIX== -s Projeto_Switch_Netbox -k Trap_Erros_Vlans -o \"" + dev + " - MAIS de uma interface está indicada como UPLINK\""
                    os.system(erro_zabbix)
                    cont_erros += 1
                vlan_upl_temp.extend(separa_vlans_tag(int['tagged_vlan']))
                # print("VLANS TAG separadas")
                # print(str(vlan_upl_temp))
                for vl in vlan_upl_temp:
                    if vl not in vlans_uplink:
                        vlans_uplink.append(vl)
                # print(str(vlan_upl_temp))
                # Verifica se tem vlans untagged na porta de uplink
                if 'untagged_vlan' in int.keys():
                    # Verifica se a vlan não foi listada anteriormente
                    # print("VLAN UNT encontrada")
                    if int['untagged_vlan'] not in vlans_uplink:
                        vlans_uplink.append(int['untagged_vlan'])
                    # Imprime mensagem de erro. Não deve ter nenhuma vlan untagged na interface de uplink
                    # print("VLAN untag na int de upl")
                    texto += "VLANs Untagged na interface de UPLINK. IP: " + dev + ", VLANs Untagged: " + str(int['untagged_vlan']) + ".\n"
                    log_ex.warning(f"FALHA,VLANs Untagged na interface de UPLINK. VLANs Untagged: {int['untagged_vlan']},{dev}")
                    log_dat.warning(f"FALHA,VLANs Untagged na interface de UPLINK,{int['untagged_vlan']},{dev}")
                    # print(f"VLANs Untagged na interface de UPLINK. IP: {dev}, VLANs Untagged: {str(int['untagged_vlan'])}")
                    erro_zabbix = "zabbix_sender -z ==ENDERECO_IP_ZABBIX== -s Projeto_Switch_Netbox -k Trap_Erros_Vlans -o \"" + dev + " - VLANs Untagged na interface de UPLINK: " + str(int['untagged_vlan']) + "\""
                    os.system(erro_zabbix)
                    cont_erros += 1
            else:
                # Trata as interfaces de derivação/APs
                # print("INT de deriv/APs")
                if 'tagged_vlan' in int.keys():
                    # Chama função para identificar a vlan e ajustar a coleta
                    tag_temp = separa_vlans_tag(int['tagged_vlan'])
                    # Verifica se a VLAN foi inserida anteriormente
                    # print(f"VLAN TAG deriv/APs: {str(tag_temp)}")
                    for vl in tag_temp:
                        if vl not in vlans_interfaces:
                            vlans_interfaces.append(vl)
                    # print(f"VLAN TAG deriv/APs: {str(vlans_interfaces)}")
                # Verifica se tem vlans untagged nas ports de acesso e dervação
                if 'untagged_vlan' in int.keys():
                    # print("VLAN UNT deriv/APs")
                    # Descarta a vlan 1
                    if int['untagged_vlan'] != 1:
                        # Verifica se a VLAN foi inserida anteriormente
                        if int['untagged_vlan'] not in vlans_interfaces:
                            vlans_interfaces.append(int['untagged_vlan'])
                    # print(f"VLAN UNT na deriv/APs: {vlans_interfaces}")
        # Coleta das portas de acesso/derivação
        else:
            # print("INT ACESSO")
            if 'tagged_vlan' in int.keys():
                # Chama função para identificar a vlan e ajustar a coleta
                tag_temp = separa_vlans_tag(int['tagged_vlan'])
                # Verifica se a VLAN foi inserida anteriormente
                for vl in tag_temp:
                    if vl not in vlans_interfaces:
                        vlans_interfaces.append(vl)
                # print(f"VLANs TAG: {vlans_interfaces}")
            # Verifica se tem vlans untagged nas ports de acesso e dervação
            if 'untagged_vlan' in int.keys():
                # Descarta a vlan 1
                if int['untagged_vlan'] != 1:
                    # Verifica se a VLAN foi inserida anteriormente
                    if int['untagged_vlan'] not in vlans_interfaces:
                        vlans_interfaces.append(int['untagged_vlan'])
                # print(f"VLAN UNT no ACESSO: {vlans_interfaces}")
    # Valida as vlans configuradas nas interfaces de acesso com o uplink
    #print(f"VLAN UPL: {vlans_uplink}")
    #print(f"VLAN DEMAIS: {vlans_interfaces}")
    for vl_int in vlans_interfaces[:]:
        for vl_upl in vlans_uplink[:]:
            if vl_int == vl_upl:
                vlans_interfaces.remove(vl_int)
                vlans_uplink.remove(vl_upl)
    #print(f"VLAN UPL: {vlans_uplink}")
    #print(f"VLAN DEMAIS: {vlans_interfaces}")
    # Um caso bem comum é o ativo possuir a vlan de gerência apenas na interface de uplink
    # Para remover da maneira mais correta, é importante identificar essa vlan e removê-la da lista de uplink
    # Encontra a vlan de gerência do ativo
    parser = ttp(data=net_connect.send_command("show vlan custom id name:30 ipconfig"), template=ttp_show_ip_custom_id_name_ipconfig, log_level='CRITICAL')
    parser.parse()
    res = parser.result()
    res = res[0][0]
    # Encontra o ID da vlan de gerência
    for vl in res:
        # Ignorando a primeira linha da consulta
        if vl['vlan_id'] == '------':
            continue
        if 'vlan_ip_config' in vl.keys():
            if vl['vlan_ip_config'] == 'Manual':
                vlanid_gerencia = vl['vlan_id']
    # Verifica se alguma vlan não foi removida da lista de interfaces de acesso/derivação
    if len(vlans_interfaces) > 0:
        texto += "VLANs não referenciadas restantes nas interfaces de ACESSO/DERIVAÇÃO. IP: " + dev + ", VLANs: " + str(vlans_interfaces) + ".\n"
        log_ex.warning(f"FALHA,VLANs não referenciadas restantes nas interfaces de ACESSO/DERIVAÇÃO. VLANs: {str(vlans_interfaces).replace(',',';')},{dev}")
        log_dat.warning(f"FALHA,VLANs não referenciadas restantes nas interfaces de ACESSO/DERIVAÇÃO,{str(vlans_interfaces).replace(',',';')},{dev}")
        erro_zabbix = "zabbix_sender -z ==ENDERECO_IP_ZABBIX== -s Projeto_Switch_Netbox -k Trap_Erros_Vlans -o \"" + dev + " - VLANs não referenciadas restantes nas interfaces de ACESSO/DERIVAÇÃO: " + str(vlans_interfaces) + "\""
        os.system(erro_zabbix)
        cont_erros += 1
    # Verifica se alguma vlan não foi removida da lista da interface de uplink
    if len(vlans_uplink) > 0:
        # Remove a vlan de gerência identificada anteriormente da interface de uplink
        for vl in vlans_uplink:
            if str(vl) == vlanid_gerencia:
                vlans_uplink.remove(vl)
    # Verifica novamente se alguma vlan não foi removida da lista da interface de uplink
    if len(vlans_uplink) > 0:
        texto += "VLANs não referenciadas restantes nas interfaces de UPLINK. IP: " + dev + ", VLANs: " + str(vlans_uplink) + ".\n"
        log_ex.warning(f"FALHA,VLANs não referenciadas restantes nas interfaces de UPLINK. VLANs: {str(vlans_uplink).replace(',',';')},{dev}")
        log_dat.warning(f"FALHA,VLANs não referenciadas restantes nas interfaces de UPLINK,{str(vlans_uplink).replace(',',';')},{dev}")
        erro_zabbix = "zabbix_sender -z ==ENDERECO_IP_ZABBIX== -s Projeto_Switch_Netbox -k Trap_Erros_Vlans -o \"" + dev + " - VLANs não referenciadas restantes nas interfaces de UPLINK: " + str(vlans_uplink) + "\""
        os.system(erro_zabbix)
        cont_erros += 1
    # Imprime mensagem de sucesso caso não tenha encontrado nenhum erro
    if cont_erros == 0:
        log_ex.warning(f"SUCESSO,VLANs configuradas corretamente,{dev}")
        log_dat.warning(f"SUCESSO,VLANs configuradas corretamente,,{dev}")
    return texto


def separa_vlans_tag(string_switch):
    # Encontra todas as vlans tageadas configuradas
    resultado = []
    vlans_tagged = [vlan.strip() for vlan in string_switch.split(",")]
    for vlan in vlans_tagged:
        if '-' in vlan:
            start, end = map(int, vlan.split('-'))
            resultado.extend(range(start, end+1))
        else:
            resultado.append(int(vlan))
    return resultado

