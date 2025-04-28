import requests
import json
from CMDB import cmdb_token

# Ocultar avisos sobre Unverified HTTPS request
import urllib3
urllib3.disable_warnings()

# Imprime a versão do CMDB_rest
print('='*80)
print('CMDB_REST VERSÃO: 1.0.0.0 - Agosto/2024')
print('='*80)

link = 'https://cmdb.algo.br/'

headers = {
  'Accept': 'application/json',
  'Content-Type': 'application/json',
  'Authorization': 'Token ' + cmdb_token.token
}
"""
Funções para acessar o CMDB Netbox via API REST
O documento está separado por tipo de interação:
- SITES
- LISTAR DISPOSITIVOS
- OPERAÇOES COM INTERFACES
- OPERAÇOES COM VLANS
- OPERAÇOES COM CABOS
- DIVERSOS
- IPAM

Foram desenvolvidas apenas as funções necessárias para a arquitetura
"""

# ============================================================================================
# SITES
# ============================================================================================
def list_all_sites():
    # Obtendo lista de TODOS OS SITES
    payload = {}
    url = link + "api/dcim/sites/?limit=1000"
    response = requests.request("GET", url, headers=headers, data=payload, verify=False)
    resp_json = response.json()
    resp = resp_json['results']
    return(resp)


def list_site_nome(slug):
    # Obtendo lista site especificado pelo SLUG DO SITE
    payload = {}
    url = link + "api/dcim/sites/?slug=" + slug
    response = requests.request("GET", url, headers=headers, data=payload, verify=False)
    resp_json = response.json()
    resp = resp_json['results']
    return(resp)


def list_site_id(id):
    # Obtendo lista site especificado pelo ID DO SITE
    payload = {}
    url = link + "api/dcim/sites/?id=" + id
    response = requests.request("GET", url, headers=headers, data=payload, verify=False)
    resp_json = response.json()
    resp = resp_json['results']
    return(resp)


def update_site(id, dados):
    # Alterando dados do site informado
    payload = dados
    url = link + "api/dcim/sites/"+ str(id) + "/"
    response = requests.request("PATCH", url, headers=headers, json=payload, verify=False)
    return(response)


# ============================================================================================
# LISTAR DISPOSITIVOS
# ============================================================================================
def list_device_site_nome(slug):
    # Obtendo lista dos dispositivos pelo SLUG DO SITE
    payload = {}
    url = link + "api/dcim/devices/?site=" + slug + "&has_primary_ip=True&limit=1000"
    response = requests.request("GET", url, headers=headers, data=payload, verify=False)
    resp_json = response.json()
    resp = resp_json['results']
    return(resp)


def list_device_site_id(id):
    # Obtendo lista dos dispositivos pelo ID DO SITE
    payload = {}
    url = link + "api/dcim/devices/?site_id=" + id + "&has_primary_ip=True&limit=1000"
    response = requests.request("GET", url, headers=headers, data=payload, verify=False)
    resp_json = response.json()
    resp = resp_json['results']
    return(resp)


def list_device_fabricante_nome(fabricante):
    # Obtendo lista dos dispositivos pelo SLUG DO FABRICANTE
    payload = {}
    url = link + "api/dcim/devices/?manufacturer=" + fabricante + "&has_primary_ip=True&limit=1000"
    response = requests.request("GET", url, headers=headers, data=payload, verify=False)
    resp_json = response.json()
    resp = resp_json['results']
    return(resp)


def list_device_fabricante_id_por_site(fabricante, site_id):
    # Obtendo lista dos dispositivos pelo ID DO FABRICANTE EM UM DETERMINADO SITE ID
    payload = {}
    url = link + "api/dcim/devices/?manufacturer_id=" + fabricante + "&site_id=" + site_id + "&has_primary_ip=True&limit=1000"
    response = requests.request("GET", url, headers=headers, data=payload, verify=False)
    resp_json = response.json()
    resp = resp_json['results']
    return(resp)


def list_device_role_nome_por_site(role, site_id):
    # Obtendo lista dos dispositivos pelo NOME DA FUNÇÃO DO ATIVO EM UM DETERMINADO SITE ID
    payload = {}
    url = link + "api/dcim/devices/?role=" + role + "&site_id=" + site_id + "&has_primary_ip=True&limit=1000"
    response = requests.request("GET", url, headers=headers, data=payload, verify=False)
    resp_json = response.json()
    resp = resp_json['results']
    return(resp)


def list_device_role_id_por_site(role, site_id):
    # Obtendo lista dos dispositivos pelo ID DA FUNÇÃO DO ATIVO EM UM DETERMINADO SITE ID
    payload = {}
    url = link + "api/dcim/devices/?role_id=" + role + "&site_id=" + site_id + "&has_primary_ip=True&limit=1000"
    response = requests.request("GET", url, headers=headers, data=payload, verify=False)
    resp_json = response.json()
    resp = resp_json['results']
    return(resp)


def list_device_todos_role_id_por_site(site_id):
    # Obtendo lista dos dispositivos pelo ID DA FUNÇÃO DO ATIVO EM UM DETERMINADO SITE ID
    payload = {}
    url = link + "api/dcim/devices/?role_id=4&role_id=5&role_id=6&role_id=7&site_id=" + site_id + "&has_primary_ip=True&limit=1000"
    response = requests.request("GET", url, headers=headers, data=payload, verify=False)
    resp_json = response.json()
    resp = resp_json['results']
    return(resp)


def list_device_type_id_por_site(type, site_id):
    # Obtendo lista dos dispositivos pelo ID DO DEVICE TYPE DO ATIVO EM UM DETERMINADO SITE ID
    payload = {}
    url = link + "api/dcim/devices/?device_type_id=" + type + "&site_id=" + site_id + "&has_primary_ip=True&limit=1000"
    response = requests.request("GET", url, headers=headers, data=payload, verify=False)
    resp_json = response.json()
    resp = resp_json['results']
    return(resp)


def list_plataforma_id_por_site(plataforma, site_id):
    # Obtendo lista dos dispositivos pelo ID DA PLATAFORMA DO ATIVO EM UM DETERMINADO SITE ID
    payload = {}
    url = link + "api/dcim/devices/?platform_id=" + plataforma + "&site_id=" + site_id + "&has_primary_ip=True&limit=1000"
    response = requests.request("GET", url, headers=headers, data=payload, verify=False)
    resp_json = response.json()
    resp = resp_json['results']
    return(resp)


def list_device_dev_id(device_id):
    # Obtendo lista dos dispositivos pelo ID DO DISPOSITIVO
    payload = {}
    url = link + "api/dcim/devices/" + device_id
    response = requests.request("GET", url, headers=headers, data=payload, verify=False)
    resp_json = response.json()
    resp = resp_json
    return(resp)


def list_devide_por_ip(ip):
    # Obtendo o dispositivo a partir do ip cadastrado no CMDB
    payload = {}
    url = link + "api/ipam/ip-addresses/?address=" + ip
    response = requests.request("GET", url, headers=headers, data=payload, verify=False)
    resp_json = response.json()
    resp = resp_json['results']
    return(resp)


# ============================================================================================
# OPERAÇOES COM INTERFACES
# ============================================================================================
def list_interfaces_por_device(device_id):
    # Obtendo lista todas as INTERFACES DE UM DISPOSITIVO
    payload = {}
    url = link + "api/dcim/interfaces/?device_id=" + str(device_id) + "&limit=1000"
    response = requests.request("GET", url, headers=headers, data=payload, verify=False)
    resp_json = response.json()
    resp = resp_json['results']
    return(resp)


def consultar_interface_pelo_id(id):
    # Obtendo detalhes de uma interface espeçifica
    payload = {}
    url = link + "api/dcim/interfaces/" + str(id)
    response = requests.request("GET", url, headers=headers, data=payload, verify=False)
    resp_json = response.json()
    return(resp_json)


def list_ips_por_device(device_id):
    # Obtendo lista todas os ENDEREÇOS IPS DE UM DISPOSITIVO
    payload = {}
    url = link + "api/ipam/ip-addresses/?device_id=" + device_id + "&limit=1000"
    response = requests.request("GET", url, headers=headers, data=payload, verify=False)
    resp_json = response.json()
    resp = resp_json['results']
    return(resp)


def list_ips_por_interface(interface_id):
    # Obtendo lista todas os ENDEREÇOS IPS DE UMA INTERFACE
    payload = {}
    url = link + "api/ipam/ip-addresses/?interface_id=" + interface_id + "&limit=1000"
    response = requests.request("GET", url, headers=headers, data=payload, verify=False)
    resp_json = response.json()
    resp = resp_json['results']
    return(resp)


def alterar_interface(int_id, dados):
    # Alterar dados de uma interface
    payload = dados
    url = link + "api/dcim/interfaces/" + int_id + '/'
    response = requests.request("PATCH", url, headers=headers, json=payload, verify=False)
    return(response)


def criar_interfaces(dados):
    # Criando uma INTERFACES EM UM DISPOSITIVO
    payload = dados
    url = link + "api/dcim/interfaces/"
    response = requests.request("POST", url, headers=headers, json=payload, verify=False)
    return(response)


# ============================================================================================
# OPERAÇOES COM VLANS
# ============================================================================================
def list_vlans_por_funcao(role):
    # Obtendo todas as VLANS cadastradas por função
    payload = {}
    url = link + "api/ipam/vlans/?role_id=" + role + "&limit=1000"
    response = requests.request("GET", url, headers=headers, data=payload, verify=False)
    resp_json = response.json()
    resp = resp_json['results']
    return(resp)


def list_vlans_por_site(site):
    # Obtendo todas as VLANS cadastradas por site
    payload = {}
    url = link + "api/ipam/vlans/?site_id=" + site + "&limit=1000"
    response = requests.request("GET", url, headers=headers, data=payload, verify=False)
    resp_json = response.json()
    resp = resp_json['results']
    return(resp)


def update_vlan(id, dados):
    # Alterando dados da vlan informada
    payload = dados
    url = link + "api/ipam/vlans/"+ str(id) + "/"
    response = requests.request("PATCH", url, headers=headers, json=payload, verify=False)
    return(response)


# ============================================================================================
# OPERAÇOES COM CABOS
# ============================================================================================
def list_cabos_por_device(device_id):
    # Obtendo lista todos os CABOS DE UM DISPOSITIVO
    payload = {}
    url = link + "api/dcim/cables/?device_id=" + str(device_id)
    response = requests.request("GET", url, headers=headers, data=payload, verify=False)
    resp_json = response.json()
    resp = resp_json['results']
    return(resp)


# ============================================================================================
# DIVERSOS
# ============================================================================================
def list_plataformas():
    # Obtendo lista das PLATAFORMAS
    payload = {}
    url = link + "api/dcim/platforms"
    response = requests.request("GET", url, headers=headers, data=payload, verify=False)
    resp_json = response.json()
    resp = resp_json['results']
    return(resp)


def list_device_type():
    # Obtendo lista dos DEVICE TYPES
    payload = {}
    url = link + "api/dcim/device-types"
    response = requests.request("GET", url, headers=headers, data=payload, verify=False)
    resp_json = response.json()
    resp = resp_json['results']
    return(resp)


def list_device_type_por_id(id):
    # Obtendo lista dos DEVICE TYPES
    payload = {}
    url = link + "api/dcim/device-types/" + str(id) + "/"
    response = requests.request("GET", url, headers=headers, data=payload, verify=False)
    resp_json = response.json()
    return(resp_json)


def list_device_role():
    # Obtendo lista dos DEVICE ROLES
    payload = {}
    url = link + "api/dcim/device-roles"
    response = requests.request("GET", url, headers=headers, data=payload, verify=False)
    resp_json = response.json()
    resp = resp_json['results']
    return(resp)


def list_fabricantes():
    # Obtendo lista dos FABRICANTES
    payload = {}
    url = link + "api/dcim/manufacturers"
    response = requests.request("GET", url, headers=headers, data=payload, verify=False)
    resp_json = response.json()
    resp = resp_json['results']
    return(resp)


# ============================================================================================
# IPAM
# ============================================================================================
def listar_prefixos_pools_ipv4(role):
    # Lista os prefixos IPv4 com pools, espera o tipo de rede como entrada. 1200 resultados listados
    payload = {}
    url = link + "api/ipam/prefixes/?is_pool=True&family=4&role_id=" + role + "&limit=1200"
    response = requests.request("GET", url, headers=headers, json=payload, verify=False)
    resp_json = response.json()
    resp_json = resp_json['results']
    return(resp_json)


def buscar_prefix_id_ipv4(site_id, vlan_id):
    # Consulta o ID do prefixo da vlan informada
    payload = {}
    url = link + "api/ipam/prefixes/?family=4&site_id="+ str(site_id) + "&vlan_vid=" + str(vlan_id)
    response = requests.request("GET", url, headers=headers, json=payload, verify=False)
    resp_json = response.json()
    resp_json = resp_json['results']
    return(resp_json)


def buscar_ip_livre(prefix_id):
    # Consulta os IPs livres do prefixo informado, retorna uma lista com o IPs
    payload = {}
    url = link + "api/ipam/prefixes/" + str(prefix_id) + "/available-ips"
    response = requests.request("GET", url, headers=headers, json=payload, verify=False)
    resp_json = response.json()
    return(resp_json)


def remover_ip(id):
    # Remove o IP com o ID informado
    payload = {}
    url = link + "api/ipam/ip-addresses/" + str(id) + "/"
    response = requests.request("DELETE", url, headers=headers, json=payload, verify=False)
    return(response)


def verificar_ip_existente(dados):
    # Verifica se um IP esta cadastrado. Retorna o dict como resposta
    payload = {}
    url = link + "api/ipam/ip-addresses/?address=" + dados
    response = requests.request("GET", url, headers=headers, json=payload, verify=False)
    resp_json = response.json()
    return(resp_json)


def inserir_ip(dados):
    # Insere novo IP (utilizado para reservas de IP no DHCP)
    payload = dados
    url = link + "api/ipam/ip-addresses/"
    response = requests.request("POST", url, headers=headers, json=payload, verify=False)
    return(response)


def update_ip(id, dados):
    # Atualiza dados de um IP
    payload = dados
    url = link + "api/ipam/ip-addresses/" + str(id) + "/"
    response = requests.request("PUT", url, headers=headers, json=payload, verify=False)
    return(response)


def listar_ips_pelo_id(id):
    # Obtendo detalhes de um IP específico
    payload = {}
    url = link + "api/ipam/ip-addresses/" + str(id) + "/"
    response = requests.request("GET", url, headers=headers, data=payload, verify=False)
    resp_json = response.json()
    return(resp_json)


def listar_ips():
    # Obtendo lista de TODOS (verificar) OS IPS cadastrados
    payload = {}
    url = link + "api/ipam/ip-addresses/"
    response = requests.request("GET", url, headers=headers, data=payload, verify=False)
    resp_json = response.json()
    resp = resp_json['results']
    return(resp)


def listar_prefixos_site(site_id):
    # Obtendo lista de TODOS os presixos de determinado site
    payload = {}
    url = link + "api/ipam/prefixes/?site_id=" + site_id
    response = requests.request("GET", url, headers=headers, data=payload, verify=False)
    resp_json = response.json()
    resp = resp_json['results']
    return(resp)


def listar_prefixos_vlan(vlan_id):
    # Obtendo lista de TODOS os presixos de determinado site
    payload = {}
    url = link + "api/ipam/prefixes/?vlan_id=" + vlan_id
    response = requests.request("GET", url, headers=headers, data=payload, verify=False)
    resp_json = response.json()
    resp = resp_json['results']
    return(resp)


# ====================================================
# ====================================================

# ====================================================
# ====================================================

# ====================================================
# ====================================================

# ====================================================
# ====================================================
