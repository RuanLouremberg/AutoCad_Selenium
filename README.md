# 🖥️ Cadastro Automático de Peças — Selenium + CSV

Script de automação web que lê um arquivo CSV contendo peças de hardware e as cadastra automaticamente em um sistema local via Selenium.

Esse código foi criado para complementar com WebPcBuilder, cadastrando novos componentes no sistema.

---

## 📋 Descrição

O script `tratamento_dados.py` percorre cada linha do arquivo `pecas_cadastrar.csv`, trata os dados de acordo com a categoria da peça e preenche automaticamente os formulários do sistema rodando em `http://localhost:5000/builder`.

Categorias suportadas:

- **Processador** — socket, núcleos, threads, frequência base,frequência oc, PCIe, TDP
- **GPU** — chip, PCIe, VRAM, TDP
- **Placa-mãe** — socket, chipset, PCIe, DDR, form factor
- **Memória** — tipo, capacidade, velocidade
- **Armazenamento** — tipo, capacidade, velocidade
- **Fonte** — watts, certificação, modularidade
- **Gabinete** — tipo, form factor suportado, limites de cooler/GPU/water cooler
- **Cooler** — tipo, TDP suportado, altura, fans de WC

---

## 📁 Estrutura do projeto

```
.
├── tratamento_dados.py   # Script principal de automação
└── pecas_cadastrar.csv   # Base de dados com as peças a cadastrar
```

---

## 📄 Formato do CSV

Cada linha representa uma peça. O primeiro campo é sempre a **categoria** e o último é sempre o **preço**. Os campos intermediários variam por categoria.

Exemplos:

```
Processador, AMD Ryzen 9 9950X, AMD, AM5, 16, 32, 4.3, 5.7, 5, 170, 4500.0
GPU, NVIDIA RTX 5070, Zotac, GB205, 5, 12, 250, 4200.0
Fonte, Corsair RM1200x Shift, Corsair, 1200, 80+ Gold, Full, 1600.0
```

> ⚠️ Linhas com **qualquer campo vazio** são automaticamente ignoradas para preservar a integridade do banco de dados.

---

## ⚙️ Requisitos

- Python 3.8+
- Google Chrome instalado
- ChromeDriver compatível com a versão do Chrome
- Sistema local rodando em `http://localhost:5000`

### Dependências Python

```bash
pip install selenium
```

---

## 🚀 Como usar

1. Certifique-se de que o sistema principal está rodando em `http://localhost:5000/builder`.

2. Coloque o arquivo `pecas_cadastrar.csv` na mesma pasta do script.

3. Execute o script:

```bash
python tratamento_dados.py
```

O script irá:
- Abrir o Chrome automaticamente
- Fazer login com as credenciais configuradas
- Percorrer cada linha do CSV
- Preencher e submeter o formulário para cada peça válida

---

## 🔐 Credenciais

As credenciais de login tem que ser definidas no `.env_example` no arquivo principal

```bash
ADMIN_NOME=seu_nome
ADMIN_EMAIL=seu_email
ADMIN_SENHA=sua_senha
```

> 💡 Renomeie o `.env_example` para `.env` e modifique suas credenciais no arquivo

---

## 🧹 Tratamento de dados

O script normaliza os dados antes de enviá-los ao formulário:

| Tratamento | Exemplo |
|---|---|
| Nomes de marcas em maiúsculas | `amd` → `AMD` |
| Correção de capitalização especial | `nzxt` → `NZXT`, `evga` → `EVGA`, `icue` → `iCUE` |
| Form factors padronizados | `matx` / `MATX` → `mATX` |
| Tipos de cooler normalizados | `aircooler` → `AirCooler` |
| Modulares sem acento corrigidos | `Nao` → `Não` |
| Evita prefixo de marca duplicado no nome | `AMD AMD Ryzen...` → `AMD Ryzen...` |

---

## ⚠️ Observações

- O arquivo CSV de exemplo contém dados de teste com valores repetidos e intencionalmente incompletos para validar o tratamento de erros.
- Linhas com campos faltando geram um aviso no terminal e são puladas.
- O script usa `time.sleep()` entre ações para garantir estabilidade — ajuste os tempos conforme a velocidade do seu dispositivo.
- O site principal deve estar rodando simultâneamente para que o cadasstro ocorra