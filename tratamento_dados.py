import csv
import re
from selenium import webdriver
import time
from selenium.webdriver.support.ui import Select

navegador = webdriver.Chrome()
navegador.maximize_window()

navegador.get('http://localhost:5000/builder')
email = navegador.find_element('name', 'email').send_keys('carlos123@gmail.com')
senha = navegador.find_element('name', 'senha').send_keys('carlos123')
enviar = navegador.find_element('id', 'botao_enviar')
enviar.click()
navegador.find_element('id', 'abacadastro').click()
time.sleep(0.5)

# --- Todos os defs para tratamento de dados -------------------
def tratar_processador(linha_limpa):

    socket = linha_limpa[3].upper().strip()
    nucleos = int(float(linha_limpa[4]))
    threads = int(float(linha_limpa[5]))
    freq_base = float(linha_limpa[6])
    freq_boost = float(linha_limpa[7])
    pcie_versao = int(float(linha_limpa[8]))
    tdp_watts = int(float(linha_limpa[9]))
    return socket, nucleos, threads, freq_base, freq_boost, pcie_versao, tdp_watts

def tratar_gpu(linha_limpa):

    chip = linha_limpa[3].strip()
    pcie_versao = int(float(linha_limpa[4]))
    vram_gb = int(float(linha_limpa[5]))
    tdp_gpu = int(float(linha_limpa[6]))
    return chip, pcie_versao, vram_gb, tdp_gpu

def tratar_placamae(linha_limpa):

    socket = linha_limpa[3].strip().upper()
    chipset = linha_limpa[4].upper().strip()
    pcie_versao = int(float(linha_limpa[5]))
    ddr_suporte = str(linha_limpa[6]).strip().upper()
    form_factor = linha_limpa[7].strip().upper()
    form_factor = form_factor.replace('matx', 'mATX').replace('MATX', 'mATX')
    return socket, chipset, pcie_versao, ddr_suporte, form_factor

def tratar_memoria(linha_limpa):

    tipo = linha_limpa[3].upper().strip()
    capacidade_gb = int(float(linha_limpa[4]))
    velocidade_mhz = int(float(linha_limpa[5]))
    return tipo, capacidade_gb, velocidade_mhz

def tratar_armazenamento(linha_limpa):

    tipo = linha_limpa[3].upper().strip()
    capacidade_gb = int(float(linha_limpa[4]))
    velocidade_mbs = int(float(linha_limpa[5]))
    return tipo, capacidade_gb, velocidade_mbs

def tratar_fonte(linha_limpa):

    watts = int(float(linha_limpa[3]))
    certificacao = linha_limpa[4].strip().title()
    modular = linha_limpa[5].title()
    modular = re.sub(r'Nao', 'Não', modular, flags=re.IGNORECASE)
    
    return watts, certificacao, modular

def tratar_gabinete(linha_limpa):

    tipo = linha_limpa[3].title()
    mobo_form_factor = linha_limpa[4].strip().upper()
    mobo_form_factor = mobo_form_factor.replace('matx', 'mATX').replace('MATX', 'mATX')
    max_cooler = int(float(linha_limpa[5]))
    max_gpu = int(float(linha_limpa[6]))
    max_wc = int(float(linha_limpa[7]))
    return tipo, mobo_form_factor, max_cooler, max_gpu, max_wc

def tratar_cooler(linha_limpa):

    tipo = linha_limpa[3].capitalize()
    tipo = re.sub(r'cooler', 'Cooler', tipo, flags=re.IGNORECASE)
    tdp = int(float(linha_limpa[4]))
    altura = int(float(linha_limpa[5]))
    wc_fans = int(float(linha_limpa[6]))
    return tipo, tdp, altura, wc_fans


linha_count = 0
# --- Abrindo o arquivo para o pegar os dados -----------------
# (OBS: arquivo de teste, sem valores reais e com valores repetidos)
with open('pecas_cadastrar.csv', mode='r', encoding='utf-8') as f:
    leitor = csv.reader(f)

# --- 3 coisas que tem em todos os componentes ---------------
    def tratar_base(linha_limpa):
        nome = linha_limpa[1].strip().title()
        nome = nome.replace('Nzxt', 'NZXT').replace('Evga', 'EVGA').replace('Icue','iCUE').replace('Nvme', 'NVME')
        nome = re.sub(r'x3d', 'X3D', nome, flags=re.IGNORECASE)
        marca = linha_limpa[2].upper().strip()
        if marca == "INTEL":
            marca.capitalize()
        preco = float(linha_limpa[-1])

        return nome, marca, preco

# --- Estrutura pra percorrer todas as linhas do arquivo -----
    for linha in leitor:
        navegador.find_element('id', 'abacadastro').click()

        linha_limpa = [coluna.strip() for coluna in linha]
    # Garantindo que não tem valores vazios pra não comprometer a integridade do BD
        if any(campo == '' for campo in linha_limpa):
            print(f'linha incompleta detectada, pulando linha')
            linha_count +=1
            continue

        categoria = linha_limpa[0].capitalize().strip()
        select_element = navegador.find_element('id', 'categoria')
        select_object = Select(select_element)

        mapa_categorias = {
            "Processador": "processadores",
            "Gpu": "gpus",
            "Placa mae": "placas_mae",
            "Memoria": "memorias",
            "Armazenamento": "armazenamentos",
            "Fonte": "fontes",
            "Gabinete": "gabinetes",
            "Cooler": "refrigeracao"
        }

        
        categoria_web = mapa_categorias.get(categoria)
        if not categoria_web:
            continue

        select_object.select_by_value(categoria_web)
        nome, marca, preco = tratar_base(linha_limpa)
        
        navegador.find_element('id', 'abacadastro').click()
        time.sleep(0.5)
        if marca.capitalize() not in nome:
            navegador.find_element('id', 'campo_nome').send_keys(marca.capitalize() + " " + nome)
        else:
            navegador.find_element('id', 'campo_nome').send_keys(nome)
        navegador.find_element('id', 'campo_marca').send_keys(marca)
        
        
    # Cadastro das peças de acordo com o tipo
        if categoria == 'Processador':
            socket, nucleos, threads, freq_base, freq_boost, pcie_versao,tdp_watts = tratar_processador(linha_limpa)
            navegador.find_element('name', 'socket').send_keys(socket)
            navegador.find_element('name', 'nucleos').send_keys(str(nucleos))
            navegador.find_element('name', 'threads').send_keys(str(threads))
            navegador.find_element('name', 'freq_base').send_keys(str(freq_base))
            navegador.find_element('name', 'freq_boost').send_keys(str(freq_boost))

            pcie_select = Select(navegador.find_element('name', 'pcie_versao'))
            pcie_select.select_by_value(f'{float(pcie_versao):.1f}')

            navegador.find_element('name', 'tdp_watts').send_keys(str(tdp_watts))

        elif categoria == 'Gpu':
            chip, pcie_versao, vram_gb, tdp_gpu = tratar_gpu(linha_limpa)
            navegador.find_element('name', 'chip').send_keys(chip)
            pcie_gpu_select = Select(navegador.find_element('name', 'pciegpu_versao'))
            pcie_gpu_select.select_by_value (f'{float(pcie_versao):.1f}')
            navegador.find_element('name', 'vram_gb').send_keys(str(float(vram_gb)))
            navegador.find_element('name', 'tdp_gpu').send_keys(str(float(tdp_gpu)))


        elif categoria == 'Placa mae':
            socket, chipset, pcie_versao, ddr_suporte, form_factor = tratar_placamae(linha_limpa)
            navegador.find_element('name', 'socket_mae').send_keys(socket)
            navegador.find_element('name', 'chipset').send_keys(chipset)
            Select(navegador.find_element('name', 'pciemb_versao')).select_by_value(f'{float(pcie_versao):.1f}')
            Select(navegador.find_element('name', 'ddr_suporte')).select_by_value(ddr_suporte)
            Select(navegador.find_element('name', 'form_factor')).select_by_value(form_factor)
        
        elif categoria == 'Memoria':
            tipo, capacidade_gb, velocidade_mhz = tratar_memoria(linha_limpa)
            Select(navegador.find_element('name', 'tipo_ram')).select_by_value(tipo)
            navegador.find_element('name', 'capacidade_ram').send_keys(str(capacidade_gb))
            navegador.find_element('name', 'velocidade_ram').send_keys(str(velocidade_mhz))
        
        elif categoria == 'Fonte':
            watts, certificacao, modular = tratar_fonte(linha_limpa)
            navegador.find_element('name', 'watts').send_keys(str(watts))
            
            Select(navegador.find_element('name', 'certificacao')).select_by_value(certificacao)
            Select(navegador.find_element('name', 'modular')).select_by_value(modular)
        
        elif categoria == 'Armazenamento':
            tipo, capacidade_gb, velocidade_mbs = tratar_armazenamento(linha_limpa)
            Select(navegador.find_element('name', 'tipo_disco')).select_by_value(tipo)
            navegador.find_element('name', 'capacidade_disco').send_keys(str(capacidade_gb))
            navegador.find_element('name', 'velocidade_disco').send_keys(str(velocidade_mbs))

        elif categoria == 'Gabinete':
            tipo, mobo_form_factor, max_cooler, max_gpu, max_wc = tratar_gabinete(linha_limpa)
            navegador.find_element('name', 'tipo_gabinete').send_keys(tipo)
            Select(navegador.find_element('name', 'mobo_suporte')).select_by_value(mobo_form_factor)
            navegador.find_element('name', 'max_cooler').send_keys(str(max_cooler))
            navegador.find_element('name', 'max_gpu').send_keys(str(max_gpu))
            navegador.find_element('name', 'max_wc').send_keys(str(max_wc))

        elif categoria == 'Cooler':
            tipo, tdp, altura, wc_fans = tratar_cooler(linha_limpa)
            Select(navegador.find_element('name', 'tipo_cooler')).select_by_value(tipo)
            navegador.find_element('name', 'tdp_cooler').send_keys(str(tdp))
            navegador.find_element('name', 'altura_cooler').send_keys(str(altura))
            navegador.find_element('name', 'wc_fans').send_keys(str(wc_fans))

        navegador.find_element('id', 'campo_preco').send_keys(str(preco))
        
        botao_gravar = navegador.find_element('xpath', "//button[text()='Gravar no Banco de Dados']")
        # Rola a tela até o botão aparecer
        navegador.execute_script("arguments[0].scrollIntoView();", botao_gravar)
        time.sleep(1)
        botao_gravar.click()
        
        time.sleep(1.5)
        linha_count += 1
