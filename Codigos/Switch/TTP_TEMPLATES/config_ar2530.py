import logging

# Configurar DHCP-snoopingv4
def update_dhcp_snoop_v4(net_connect, dev, log_ex, log_dat):
    # Contador de erros
    erros = 0
    # Configuração
    config = ['dhcp-snooping',
            'dhcp-snooping option 82 untrusted-policy keep',
            'no dhcp-snooping option 82',
            'dhcp-snooping vlan 1-4000',
            '',
        ]
    # Atualiza a configuração
    try:
        net_connect.send_config_set(config, read_timeout=30)
    except Exception:
        # Loga os erros
        log_ex.warning(f"UPDATE FALHA,DHCP-SNOOPING V4 erro ao atualizar configuração,{dev}")
        log_dat.warning(f"UPDATE FALHA,DHCP-SNOOPING V4,Erro ao atualizar configuração,,{dev}")
        erro_zabbix = "zabbix_sender -z ==ENDERECO_IP_ZABBIX== -s Projeto_Switch_Netbox -k Trap_Erros_Atualizar_Configuracao -o \"" + dev + " - DHCP-SNOOPING V4 - Erro ao atualizar configuração\""
        os.system(erro_zabbix)
        erros += 1
    # Conforma se a atualização foi bem sucedida
    if erros == 0:
        log_ex.warning(f"UPDATE SUCESSO,DHCP-SNOOPING V4 configuração atualizada,{dev}")
        log_dat.warning(f"UPDATE SUCESSO,DHCP-SNOOPING V4,Configuração atualizada,,{dev}")
    # Salva a alteração
    net_connect.save_config()
    # Retorna
    return


# Configurar DHCP-snoopingv6
def update_dhcp_snoop_v6(net_connect, dev, log_ex, log_dat):
    # Contador de erros
    erros = 0
    # Configuração
    config = ['dhcpv6-snooping',
            'dhcpv6-snooping vlan 1-4000',
            '',
        ]
    # Atualiza a configuração
    try:
        net_connect.send_config_set(config, read_timeout=30)
    except Exception:
        # Loga os erros
        log_ex.warning(f"UPDATE FALHA,DHCP-SNOOPING V6 erro ao atualizar configuração,{dev}")
        log_dat.warning(f"UPDATE FALHA,DHCP-SNOOPING V6,Erro ao atualizar configuração,,{dev}")
        erro_zabbix = "zabbix_sender -z ==ENDERECO_IP_ZABBIX== -s Projeto_Switch_Netbox -k Trap_Erros_Atualizar_Configuracao -o \"" + dev + " - DHCP-SNOOPING V6 - Erro ao atualizar configuração\""
        os.system(erro_zabbix)
        # Retorna caso não consiga atualizar a configuração
        return
    # Loga que a atualização foi bem sucedida
    log_ex.warning(f"UPDATE SUCESSO,DHCP-SNOOPING V6 configuração atualizada,{dev}")
    log_dat.warning(f"UPDATE SUCESSO,DHCP-SNOOPING V6,Configuração atualizada,,{dev}")
    # Salva a alteração
    net_connect.save_config()
    # Retorna
    return

# Confogurar STP
def update_stp(net_connect, dev, log_ex, log_dat):
    # Contador de erros
    erros = 0
    # Configuração
    config = ['spanning-tree force-version rstp-operation',
            'spanning-tree priority 8',
            'spanning-tree enable ',
            '',
        ]
    # Atualiza a configuração
    try:
        net_connect.send_config_set(config, read_timeout=30)
    except Exception:
        # Loga os erros
        log_ex.warning(f"UPDATE FALHA,STP erro ao atualizar configuração,{dev}")
        log_dat.warning(f"UPDATE FALHA,STP,Erro ao atualizar configuração,,{dev}")
        erro_zabbix = "zabbix_sender -z ==ENDERECO_IP_ZABBIX== -s Projeto_Switch_Netbox -k Trap_Erros_Atualizar_Configuracao -o \"" + dev + " - STP - Erro ao atualizar configuração\""
        os.system(erro_zabbix)
        # Retorna caso não consiga atualizar a configuração
        return
    # Loga que a atualização foi bem sucedida
    log_ex.warning(f"UPDATE SUCESSO,STP configuração atualizada,{dev}")
    log_dat.warning(f"UPDATE SUCESSO,STP,Configuração atualizada,,{dev}")
    # Salva a alteração
    net_connect.save_config()
    # Retorna
    return
