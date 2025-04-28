import yaml
import os
import git
import logging
import datetime

# Importando bibliotecas do Jinja2
from jinja2 import Environment, FileSystemLoader
from jinja2 import Undefined


def update_git(mensagem):
    # Atualizar Git com os arquivos coletados
    logging.warning("Atualizando repositório Git")
    repo = git.Repo(repo_path)
    repo.git.add('--all')
    repo.index.commit(mensagem)
    repo.remotes.origin.push()
    return()


# Adicionar a chave SSH para liberar acesso ao servidor Git
os.system('eval "$(ssh-agent -s)" && ssh-add ~/.ssh/==CHAVE_SSH==')
# Diretorios que os arquivos convertidos sera salvos
repo_path = os.getcwd()
repo_path = os.path.abspath(os.path.join(repo_path, os.pardir))
repo_path = repo_path + '/CMDB_IaC/Config_default'
# Atualizando repositótio Git local
g = git.cmd.Git(repo_path)
g.pull()

# Configurações de log
log_dir = repo_path + '/LOG'
hora = datetime.datetime.now()
logfile = log_dir + '/' + 'Conversao_' + str(hora.strftime("%Y-%m-%d") + '.txt')
# Caso não exista, cria o diretório de log
if not os.path.exists(log_dir):
    os.makedirs(log_dir)
# Configuração do LOG
logging.basicConfig(filename=logfile,
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    level=logging.WARN)

logging.warning("============ Iniciando conversão ============")

# Diretorio com os arquivos .yaml
path_yaml = os.getcwd()
path_yaml = os.path.abspath(os.path.join(path_yaml, os.pardir))
path_yaml = path_yaml + '/CMDB_IaC/Config_IaC'

# Lista arquivos do diretorio
arvore_dir_yaml = os.listdir(path_yaml)

# Varre a arvore de diretorios
for site in arvore_dir_yaml:
    # Elimina o diretorio de LOGs
    if site == 'LOG' or '.' in site:
        continue
    logging.warning("Iniciando consulta no diretório: %s", site)
    # Varre cada diretorio pelos arquivos .yaml
    dir = path_yaml + '/' + site
    arvore_dir_file = os.listdir(dir)
    for dir_file in arvore_dir_file:
        if '.yaml' not in dir_file:
            continue
        # Abre o arquivo yaml
        JINJA2_ENVIRONMENT_OPTIONS = { 'undefined' : Undefined }
        dados = yaml.full_load(open(dir + '/' + dir_file))
        # Valida o modelo do ativo, importa o template Jinja2 correto e converte o arquivo
        if 'switch-2530' in dados['netbox_modelo_slug']:
            print(f'Convertendo equipamento {dir_file}')
            logging.warning("Convertendo template do equipamento: %s", dir_file)
            env = Environment(loader = FileSystemLoader(''), trim_blocks=True, lstrip_blocks=True)
            template = env.get_template('CMDB_iac/Template_j2/template_2530_48-valid_config.j2')
            config = template.render(dados)
        else:
            logging.error("PENDENTE MODELO DE CONFIGURAÇÃO PARA O ATIVO: %s", dir_file)
            continue
        # Salvando arquivo convertido no diretorio correto
        # salvar é a variável que indica se o arquivo deve ser salvo
        dir_save = repo_path + '/' + site
        if not os.path.exists(dir_save):
            os.makedirs(dir_save)
        logging.warning("Salvando modelo do ativo: %s", dir_file)
        dir_file = dir_file.replace(".yaml", "_config_modelo.txt")
#        with open(dir_save + '/' + dir_file + '.txt', 'w') as f:
        with open(dir_save + '/' + dir_file, 'w') as f:
            f.write(config)


# Atualizando repositório Git
hora = datetime.datetime.now()
comm_mensgem = 'Commit com todos os modelos. Data: ' + str(hora.strftime("%d-%m-%Y %H:%M"))
update = update_git(comm_mensgem)
