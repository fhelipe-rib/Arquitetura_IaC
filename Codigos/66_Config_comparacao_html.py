import logging
import difflib
import sys
import os
import datetime

# Importando script customizado
from CMDB import cmdb_rest


def gerar_html_diff(run_config, modelo_config, saida_html, dir_site):
    # Diretório do arquivo de backup do ativo
    backup_path = os.getcwd()
    backup_path = os.path.abspath(os.path.join(backup_path, os.pardir))
    backup_path = os.path.abspath(os.path.join(backup_path, os.pardir))
    backup_path = backup_path + '/Backup_ativos/' + dir_site + '/' + run_config
    logging.warning(f"{backup_path}")
    # Diretório do modelo de configuração do ativo
    modelo_path = os.getcwd()
    modelo_path = os.path.abspath(os.path.join(modelo_path, os.pardir))
    modelo_path = os.path.abspath(os.path.join(modelo_path, os.pardir))
    modelo_path = modelo_path + '/CMDB_IaC/Config_default/' + dir_site + '/' + modelo_config
    logging.warning(f"{modelo_config}")
    # Abre os arquivos
    with open(backup_path, 'r', encoding='utf-8') as f1, open(modelo_path, 'r', encoding='utf-8') as f2:
        # Remove as 5 primeiras linhas do running config
        linhas_run = f1.readlines()[5:]
        linhas_modelo = f2.readlines()
    # Compara os arquivos com a biblioteca difflib
    d = difflib.HtmlDiff()
    html_diff = d.make_file(linhas_run, linhas_modelo, fromdesc=run_config, todesc=modelo_config)

    # Diretório para salvar as comparações
    dir_saida = os.getcwd()
    dir_saida = os.path.abspath(os.path.join(dir_saida, os.pardir))
    dir_saida = os.path.abspath(os.path.join(dir_saida, os.pardir))
    dir_saida = dir_saida + '/Codigos/Automacao_flask/static'
    logging.warning(f"{dir_saida}")
    os.makedirs(dir_saida, exist_ok=True)
    filepath = os.path.join(dir_saida, saida_html)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html_diff)
        logging.warning("Comparação salva")
        print('SALVO')
        f.close()
    print(f"Comparação gerada: {saida_html}")
    logging.warning(f"Comparação gerada: {saida_html}")

def main(entrada):
    # Configuraçõa de log
    # Coleta a hora da coleta
    hora = datetime.datetime.now()
    log_dir = os.getcwd()
    log_dir = os.path.abspath(os.path.join(log_dir, os.pardir))
    log_dir = log_dir + '/Switch/LOG'
    logfile = log_dir + '/Comparar_config_' + str(hora.strftime("%Y-%m-%d") + '.txt')
    # Caso não exista, cria o diretório de log
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    # Configuração do log
    logging.basicConfig(filename=logfile,
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    level=logging.WARN)
    logging.warning(f"============ Iniciando Comparação - {entrada} ============")
    # Consulta se o endereço IP inserido está cadastrado
    cadastro_cmdb = cmdb_rest.list_devide_por_ip(entrada)
    # Verifica se a consulta gerou resposta. Caso positivo, encerra o programa
    if cadastro_cmdb == []:
        print(f"O endereço IP não está cadastrado no CMDB: {entrada}")
        logging.error(f"O endereço IP não está cadastrado no CMDB: {entrada}")
        exit()
    # Verifica o equipamento ao qual o IP está associado. Caso não tenha, sai do programa
    if cadastro_cmdb[0]['assigned_object']['device']['id'] == None:
        print(f"O endereço IP não está associado a nenhum equipamento: {entrada}")
        logging.error(f"O endereço IP não está associado a nenhum equipamento: {entrada}")
        exit()
    # Consulta os dados do equipamento
    dados_ativo = cmdb_rest.list_device_dev_id(str(cadastro_cmdb[0]['assigned_object']['device']['id']))
    # Verifica se o equipamento é de acesso
    if dados_ativo['device_role']['id'] == 4 or dados_ativo['device_role']['id'] == 5 or dados_ativo['device_role']['id'] == 6 or dados_ativo['device_role']['id'] == 7:
        # Identidca os ativos Aruba 2530 pelo device_type
        if dados_ativo['device_type']['id'] == 25 or dados_ativo['device_type']['id'] == 26 or dados_ativo['device_type']['id'] == 27 or dados_ativo['device_type']['id'] == 96:
            # Coleta as informações necessárias
            site_id = dados_ativo['site']['id']
            site_slug = dados_ativo['site']['slug']
            device_name =  dados_ativo['name']
            # Gerar nomes dos arquivos
            arquivo_run = f"{device_name}-{entrada}-RUNNING_CONFIG.txt"
            arquivo_modelo = f"{device_name}-{entrada}_config_modelo.txt"
            site_dir = f"{site_id}_{site_slug}"
            # Nome do arquivo a ser salvo
            timestamp = datetime.datetime.now()
            timestamp = str(timestamp.strftime("%Y-%m-%d_%H"))
            savefile = f"Comparar_config_{entrada}_{timestamp}.html"
            # Chama a função para abrir e comparar as configurações
            gerar_html_diff(arquivo_run, arquivo_modelo, savefile, site_dir)
        else:
            print(f"O endereço IP não está associado a nenhum equipamento 2530: {entrada}")
            logging.error(f"O endereço IP não está associado a nenhum equipamento 2530: {entrada}")
            exit()
    else:
        print(f"O endereço IP não está associado a nenhum equipamento de ACESSO: {entrada}")
        logging.error(f"O endereço IP não está associado a nenhum equipamento de ACESSO: {entrada}")
        exit()


if __name__ == "__main__":
    # Passando os argumentos do Python
    main(sys.argv[1])