#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import time
import logging
import smtplib
from email.mime.text import MIMEText
import json
import os
from datetime import datetime

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("monitor_preco.log"),
        logging.StreamHandler()
    ]
)

# Arquivo para armazenar os preços anteriores
PRECOS_ARQUIVO = "precos_anteriores.json"

# Configurações de email
EMAIL_CONFIG = {
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587,
    "email_from": "sap.fernando.pereira@gmail.com",
    "email_password": "gplk gsoz saed icdt",  # Use uma senha de aplicativo para Gmail
    "email_to": "destinatario@email.com"
}

def carregar_produtos():
    """Carrega a lista de produtos a serem monitorados de um arquivo JSON."""
    try:
        with open("produtos.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        logging.error("Arquivo produtos.json não encontrado.")
        # Criar um arquivo de exemplo
        produtos_exemplo = [
            {
                "nome": "Exemplo de Produto",
                "url": "https://www.exemplo.com/produto",
                "seletor_preco": ".preco-produto"
            }
        ]
        with open("produtos.json", "w", encoding="utf-8") as f:
            json.dump(produtos_exemplo, f, indent=4, ensure_ascii=False)
        logging.info("Arquivo produtos.json de exemplo criado. Por favor, edite-o com seus produtos.")
        return produtos_exemplo
    except json.JSONDecodeError:
        logging.error("Erro ao decodificar o arquivo produtos.json. Verifique se o formato está correto.")
        return []

def carregar_precos_anteriores():
    """Carrega os preços anteriores do arquivo JSON."""
    try:
        with open(PRECOS_ARQUIVO, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def salvar_precos_anteriores(precos):
    """Salva os preços atuais no arquivo JSON."""
    with open(PRECOS_ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(precos, f, indent=4, ensure_ascii=False)

def obter_preco(url, seletor_preco):
    """Obtém o preço de um produto a partir da URL e do seletor CSS."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()  # Levanta exceção para códigos de erro HTTP
        
        soup = BeautifulSoup(response.text, "html.parser")
        elemento_preco = soup.select_one(seletor_preco)
        
        if not elemento_preco:
            logging.warning(f"Seletor de preço '{seletor_preco}' não encontrado na página {url}")
            return None
        
        # Limpa o texto do preço (remove espaços, símbolos de moeda, etc.)
        preco_texto = elemento_preco.text.strip()
        preco_limpo = ''.join(filter(lambda x: x.isdigit() or x == ',', preco_texto))
        preco_limpo = preco_limpo.replace(',', '.')
        
        try:
            return float(preco_limpo)
        except ValueError:
            logging.warning(f"Não foi possível converter o preço '{preco_texto}' para float")
            return None
            
    except requests.RequestException as e:
        logging.error(f"Erro ao acessar {url}: {e}")
        return None

def enviar_email(assunto, mensagem):
    """Envia um email de notificação."""
    try:
        msg = MIMEText(mensagem)
        msg['Subject'] = assunto
        msg['From'] = EMAIL_CONFIG["email_from"]
        msg['To'] = EMAIL_CONFIG["email_to"]
        
        server = smtplib.SMTP(EMAIL_CONFIG["smtp_server"], EMAIL_CONFIG["smtp_port"])
        server.starttls()
        server.login(EMAIL_CONFIG["email_from"], EMAIL_CONFIG["email_password"])
        server.send_message(msg)
        server.quit()
        
        logging.info(f"Email enviado: {assunto}")
        return True
    except Exception as e:
        logging.error(f"Erro ao enviar email: {e}")
        return False

def monitorar_precos():
    """Função principal para monitorar os preços dos produtos."""
    produtos = carregar_produtos()
    precos_anteriores = carregar_precos_anteriores()
    precos_atualizados = {}
    
    for produto in produtos:
        nome = produto["nome"]
        url = produto["url"]
        seletor = produto["seletor_preco"]
        
        logging.info(f"Verificando preço de: {nome}")
        
        preco_atual = obter_preco(url, seletor)
        if preco_atual is None:
            logging.warning(f"Não foi possível obter o preço de {nome}")
            continue
        
        precos_atualizados[nome] = {
            "preco": preco_atual,
            "url": url,
            "ultima_verificacao": datetime.now().isoformat()
        }
        
        # Verifica se o preço mudou
        if nome in precos_anteriores:
            preco_anterior = precos_anteriores[nome]["preco"]
            
            if preco_atual < preco_anterior:
                diferenca = preco_anterior - preco_atual
                percentual = (diferenca / preco_anterior) * 100
                
                mensagem = f"""
                O preço de {nome} diminuiu!
                
                Preço anterior: R$ {preco_anterior:.2f}
                Preço atual: R$ {preco_atual:.2f}
                Economia: R$ {diferenca:.2f} ({percentual:.2f}%)
                
                Confira em: {url}
                """
                
                enviar_email(f"Alerta de Preço: {nome} está mais barato!", mensagem)
            
            elif preco_atual > preco_anterior:
                diferenca = preco_atual - preco_anterior
                percentual = (diferenca / preco_anterior) * 100
                
                logging.info(f"Preço de {nome} aumentou: R$ {preco_anterior:.2f} → R$ {preco_atual:.2f} (+{percentual:.2f}%)")
            
            else:
                logging.info(f"Preço de {nome} manteve-se em R$ {preco_atual:.2f}")
        
        else:
            logging.info(f"Primeiro registro de preço para {nome}: R$ {preco_atual:.2f}")
    
    # Salva os preços atualizados
    salvar_precos_anteriores(precos_atualizados)

def main():
    """Função principal que executa o monitoramento periodicamente."""
    try:
        logging.info("Iniciando monitoramento de preços")
        
        # Verifica se o arquivo de configuração de email existe
        if not os.path.exists("email_config.json"):
            with open("email_config.json", "w", encoding="utf-8") as f:
                json.dump(EMAIL_CONFIG, f, indent=4, ensure_ascii=False)
            logging.info("Arquivo email_config.json criado. Por favor, configure suas credenciais de email.")
        
        # Carrega configurações de email
        try:
            with open("email_config.json", "r", encoding="utf-8") as f:
                email_config = json.load(f)
                for key, value in email_config.items():
                    EMAIL_CONFIG[key] = value
        except (FileNotFoundError, json.JSONDecodeError) as e:
            logging.warning(f"Erro ao carregar configurações de email: {e}")
        
        # Executa o monitoramento uma vez
        monitorar_precos()
        
        logging.info("Monitoramento concluído com sucesso")
        
    except KeyboardInterrupt:
        logging.info("Monitoramento interrompido pelo usuário")
    except Exception as e:
        logging.error(f"Erro não tratado: {e}", exc_info=True)

if __name__ == "__main__":
    main()