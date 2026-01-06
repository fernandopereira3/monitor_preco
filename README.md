# 📉 Monitor de Preços - Kabum

Este projeto é uma ferramenta automatizada desenvolvida em Python para monitorar preços de produtos na Kabum (especificamente placas de vídeo, configurável via código). O sistema utiliza Web Scraping para verificar periodicamente o valor do produto e notifica o usuário via e-mail sobre alterações ou quando um preço alvo é atingido.

O projeto é totalmente conteinerizado, facilitando a execução em qualquer ambiente sem necessidade de configuração manual de dependências do sistema.

## � Funcionalidades

- **Monitoramento Contínuo**: Verifica o preço do produto a cada 5 minutos.
- **Web Scraping Avançado**: Utiliza Selenium com Chrome Headless para extrair dados da página do produto.
- **Sistema de Notificações**:
  - Envia e-mail quando há **qualquer alteração** de preço.
  - Envia e-mail quando o **preço alvo** é atingido.
- **Histórico de Dados**: Salva todos os preços coletados com timestamp em um arquivo CSV (`historico_precos.csv`).
- **Conteinerização**: Pronto para rodar com Docker e Docker Compose, isolando o ambiente e garantindo portabilidade.
- **Persistência de Dados**: Utiliza volumes Docker para manter o histórico de preços seguro mesmo após reinicialização do container.

## �️ Tecnologias Utilizadas

- **Linguagem**: Python 3.13
- **Automação Web**: Selenium WebDriver
- **Containerização**: Docker & Docker Compose
- **SO Base da Imagem**: Fedora (para suporte atualizado ao Chrome)
- **Agendamento**: Biblioteca `schedule`

## ⚙️ Configuração

Antes de executar, é necessário criar/configurar o arquivo `config.json` na raiz do projeto com suas credenciais de e-mail e preço alvo.

**Exemplo de `config.json`:**

```json
{
    "email_remetente": "seu_email@gmail.com",
    "email_senha": "sua_senha_de_app_ou_senha",
    "email_destinatario": "email_destino@exemplo.com",
    "preco_alvo": 2500.00
}
```

> **Nota**: Para contas Gmail, recomenda-se o uso de "Senhas de App" (App Passwords) por questões de segurança.

## 🐳 Executando com Docker (Recomendado)

A maneira mais fácil e robusta de executar o monitor é utilizando Docker. Isso garante que todas as dependências (incluindo o Google Chrome) estejam instaladas corretamente.

### Pré-requisitos
- Docker
- Docker Compose

### Passos

1. **Configure o ambiente**: Certifique-se de que o arquivo `config.json` está criado e configurado corretamente na raiz do projeto.

2. **Suba o container**:
   Execute o comando abaixo na raiz do projeto:

   ```bash
   docker-compose up -d --build
   ```

   - A flag `-d` executa em segundo plano (detached).
   - A flag `--build` garante que a imagem seja construída com as últimas alterações.

3. **Verifique os logs** (opcional):
   Para garantir que o monitoramento iniciou:

   ```bash
   docker-compose logs -f
   ```

4. **Acesse os dados**:
   O histórico de preços será salvo automaticamente na pasta `./data` da sua máquina local (mapeada para `/app/data` no container).

   - Arquivo: `data/historico_precos.csv`

### Parar o monitoramento
```bash
docker-compose down
```

## 💻 Executando Localmente (Manual)

Se preferir rodar sem Docker, você precisará configurar o ambiente Python e ter o Google Chrome instalado.

### Pré-requisitos
- Python 3.13+
- Google Chrome instalado
- Pip (gerenciador de pacotes)

### Passos

1. **Crie e ative um ambiente virtual**:
   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # Linux/Mac
   source .venv/bin/activate
   ```

2. **Instale as dependências**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Execute o monitor**:
   ```bash
   python executar_monitoramento.py
   ```

## 📁 Estrutura do Projeto

- `Dockerfile`: Definição da imagem Docker (Fedora + Chrome + Python Env).
- `docker-compose.yml`: Orquestração do serviço e volumes.
- `monitor_preco.py`: Classe principal contendo a lógica de scraping e notificação.
- `executar_monitoramento.py`: Script de entrada que configura o agendamento (schedule).
- `config.json`: Arquivo de configuração (não versionado por segurança).
- `data/`: Diretório onde o CSV de histórico é salvo.
