import ipaddress
import yaml
import os
import git
import logging
import datetime

# Importando script customizado
from CMDB import cmdb_rest


def update_git(mensagem):
    # Atualizar Git com os arquivos coletados
    logging.warning("Atualizando repositório Git")
    repo = git.Repo(repo_path)
    repo.git.add('--all')
    repo.index.commit(mensagem)
    repo.remotes.origin.push()
    return()


def coletar_dados_ativos(devices):
    # Lista, coleta e salva arquivos com informações relevantes de cada dispositivo
    # Obtém o nome do site do loop
    # Em versões futuras, alterar essa coleta
    for dev in devices:
        if dev['device_role']['id'] == 4 or dev['device_role']['id'] == 5 or dev['device_role']['id'] == 6 or dev['device_role']['id'] == 7:
            if dev['primary_ip4']['address'] == None:
                logging.error("ERRO: SEM IPv4 configurado no ativo: %s, ID: %s", dev['name'], dev['id'])
                continue
            template_ativo = {}
            template_ativo['netbox_site_id'] = dev['site']['id']
            site_name = dev['site']['name']
            template_ativo['netbox_site_slug'] = dev['site']['slug']
            template_ativo['netbox_device_id'] = dev['id']
            if dev['device_type'] == None:
                logging.error("ERRO: SEM DEVICE TYPE configurado no ativo: %s, ID: %s", dev['name'], dev['id'])
                continue
            else:
                template_ativo['netbox_modelo_slug'] = dev['device_type']['slug']
            if dev['device_role'] == None:
                    logging.error("ERRO: SEM DEVICE ROLE configurado no ativo: %s, ID: %s", dev['name'], dev['id'])
                    continue
            else:
                    template_ativo['netbox_role_slug'] = dev['device_role']['slug']
            if dev['platform'] == None:
                logging.error("ERRO: SEM PLATAFORMA configurada no ativo: %s, ID: %s", dev['name'], dev['id'])
                continue
            else:
                template_ativo['netbox_plataforma_slug'] = dev['platform']['slug']
            template_ativo['nome'] = dev['name']
            template_ativo['serial'] = dev['serial']
            template_ativo['patrimonio'] = dev['asset_tag']
            template_ativo['ipv4_principal'] = dev['primary_ip4']['address']
            ultimo_ponto = dev['primary_ip4']['address'].rfind('.')
            ipv4_gw = dev['primary_ip4']['address'][:ultimo_ponto]
            template_ativo['ipv4_gateway'] = ipv4_gw + '.1'
            if dev['primary_ip6'] == None:
                template_ativo['ipv6_principal'] = None
                template_ativo['ipv6_gateway'] = None
            else:
                template_ativo['ipv6_principal'] = str(dev['primary_ip6']['address'])
                ultimo_ponto = str(dev['primary_ip6']['address']).rfind(':')
                ipv6_gw = str(dev['primary_ip6']['address'])[:ultimo_ponto]
                template_ativo['ipv6_gateway'] = ipv6_gw + ':1'
            # Lista todas as interfaces do ativo
            device_int = cmdb_rest.list_interfaces_por_device(str(dev['id']))
            interfaces = {}
            vlans = {}
            for int in device_int:
                int_temp = {}
                vlan_temp = {}
                if int['type']['label'] == 'Virtual':
                    vlan_temp['netbox_id'] = int['id']
                    vlan_temp['netbox_tipo'] = int['type']['value']
                    vlan_temp['nome'] = str.lower(int['name'])
                    vlan_temp['descricao'] = int['description']
                    device_ip = cmdb_rest.list_ips_por_interface(str(int['id']))
                    for ip in device_ip:
                        if ip['address'].endswith("/64") is True or ip['address'].endswith("/128") is True or ip['address'].endswith("/127") is True:
                            vlan_temp['ipv6_address'] = ip['address']
                        else:
                            vlan_temp['ipv4_address'] = ip['address'][:-3]
                            mascara_temp = ip['address'][-2:]
                            vlan_temp['ipv4_address_mascara'] = str(ipaddress.IPv4Network(f"0.0.0.0/{mascara_temp}", strict=False).netmask)
                    vlans[vlan_temp['nome']] = vlan_temp
                else:
                    int_temp['netbox_id'] = int['id']
                    if int['type'] == None:
                        int_temp['netbox_tipo'] = None
                    else:
                        int_temp['netbox_tipo'] = int['type']['value']
                    int_temp['nome'] = int['name']
                    int_temp['descricao'] = int['description']
                    int_temp['habilitada'] = int['enabled']
                    if int['untagged_vlan'] == None:
                        int_temp['untag_vlan'] = None
                    else:
                        int_temp['untag_vlan_id'] = int['untagged_vlan']['vid']
                    if int['tagged_vlans'] == None:
                        int_temp['tagged_vlan'] = None
                    else:
                        tag_vlan = []
                        for tag in int['tagged_vlans']:
                            tag_vlan.append(tag['vid'])
                        int_temp['tagged_vlan_id'] = tag_vlan
                    interfaces[int_temp['nome']] = int_temp
            template_ativo['interfaces'] = interfaces
            template_ativo['vlans'] = vlans
            template_yaml = yaml.dump(template_ativo, default_flow_style=False, sort_keys=False)

            dir = repo_path + '/' + str(template_ativo['netbox_site_id']) + '_' + str(template_ativo['netbox_site_slug'])
            print(f"Salvando o template IaC do ativo {template_ativo['nome']}")
            if not os.path.exists(dir):
                os.makedirs(dir)
            logging.warning("Salvando template do ativo: %s, ID: %s", dev['name'], dev['id'])
            with open(dir + '/'+ template_ativo['nome'] + '-' + (template_ativo['ipv4_principal'][:-3]) + '.yaml', 'w') as f:
                f.write(template_yaml)


# Adicionar a chave SSH para liberar acesso ao servidor Git
os.system('eval "$(ssh-agent -s)" && ssh-add ~/.ssh/==CHAVE_SSH==')
# Diretório configurado para o Git (arquivos serão salvos aqui)
repo_path = os.getcwd()
repo_path = os.path.abspath(os.path.join(repo_path, os.pardir))
repo_path = repo_path + '/CMDB_IaC/Config_IaC'
# Atualizando repositótio Git local
g = git.cmd.Git(repo_path)
g.pull()
# Configurações de log
log_dir = repo_path + '/LOG'
hora = datetime.datetime.now()
logfile = log_dir + '/' + 'Coleta_' + str(hora.strftime("%Y-%m-%d") + '.txt')
# Caso não exista, cria o diretório de log
if not os.path.exists(log_dir):
    os.makedirs(log_dir)
# Configuração do log
logging.basicConfig(filename=logfile,
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    level=logging.WARN)

# Lista todos os sites cadastrados no CMDB
logging.warning("============ Iniciando consulta ============")
sites = cmdb_rest.list_all_sites()
for site in sites:
    # Função para coletar os dados dos switches a partir de ativos cadastrados no CMDB
    print(f"Iniciando modelo IaC dos ativos do site: {site['name']}, ID: {site['id']}")
    logging.warning("Iniciando coleta dos ativos do site: %s, ID: %s", site['slug'], site['id'])
    coletar_dados_ativos(cmdb_rest.list_device_todos_role_id_por_site(str(site['id'])))

# Lista devices IDs de switches de um determinado site
# site_id = '36'
# coletar_dados_ativos(cmdb_rest.list_device_todos_role_id_por_site(site_id))


# Coleta a hora de término da coleta para registro no Git
hora = datetime.datetime.now()
comm_mensgem = 'Commit com todos os sites. Data: ' + str(hora.strftime("%d-%m-%Y %H:%M"))

# Atualiza repositório remoto
update = update_git(comm_mensgem)
