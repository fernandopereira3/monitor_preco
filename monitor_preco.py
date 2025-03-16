from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import csv
import time
from plyer import notification
import smtplib
from email.mime.text import MIMEText
import json

class MonitorPrecoKabum:
    def __init__(self):
        # Configurar opções do Chrome
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--headless')  # Executar em modo headless
        self.options.add_argument('--disable-gpu')
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--disable-dev-shm-usage')
        
        # URL do produto 1
        self.url_pichau = "https://www.pichau.com.br/processador-amd-ryzen-9-7900x-12-core-24-threads-4-7ghz-5-6ghz-turbo-cache-76mb-am5-100-100000589wof"
        self.url_kabum = "https://www.kabum.com.br/produto/378412/processador-amd-ryzen-9-7900x-5-6ghz-max-turbo-cache-76mb-am5-12-nucleos-video-integrado-100-100000589wof"

        # Carregar último preço conhecido
        self.ultimo_preco = self.carregar_ultimo_preco()
        self.ultimo_preco_pichau = self.carregar_pichau()
        
        # Configurações de email (adicione seus dados em config.json)
        self.config = self.carregar_config()
        
    def carregar_config(self):
        try:
            with open('config.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {
                'email_remetente': '',
                'email_senha': '',
                'email_destinatario': '',
                'preco_alvo': 0
            }
    
    def carregar_ultimo_preco(self):
        try:
            with open('historico_precos.csv', 'r') as file:
                linhas = list(csv.reader(file))
                if len(linhas) > 0:
                    return float(linhas[-1][1])
        except (FileNotFoundError, IndexError):
            return None
        
    def carregar_pichau(self):
        try:
            with open('historico_pichau.csv', 'r') as file:
                linhas = list(csv.reader(file))
                if len(linhas) > 0:
                    return float(linhas[-1][1])
        except (FileNotFoundError, IndexError):
            return None
            

    def enviar_email(self, assunto, mensagem):
        if not all([self.config['email_remetente'], 
                   self.config['email_senha'], 
                   self.config['email_destinatario']]):
            return
            
        try:
            msg = MIMEText(mensagem)
            msg['Subject'] = assunto
            msg['From'] = self.config['email_remetente']
            msg['To'] = self.config['email_destinatario']
            
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.login(self.config['email_remetente'], self.config['email_senha'])
            server.send_message(msg)
            server.quit()
            
        except Exception as e:
            print(f"Erro ao enviar email: {str(e)}")
    
    def verificar_alteracao_preco(self, preco_atual):
        if self.ultimo_preco is None:
            return
            
        diferenca = preco_atual - self.ultimo_preco
        if diferenca != 0:
            variacao = (diferenca / self.ultimo_preco) * 100
            mensagem = (
                f"Alteração no preço detectada!\n"
                f"Preço anterior: R$ {self.ultimo_preco:.2f}\n"
                f"Preço atual: R$ {preco_atual:.2f}\n"
                f"Variação: {variacao:.2f}%"
            )
            
            # Notificação por email
            self.enviar_email(
                f"Alteração de Preço",
                mensagem
            )
            
        # Verificar se atingiu preço alvo
        if self.config['preco_alvo'] > 0 and preco_atual <= self.config['preco_alvo']:
            mensagem_alvo = (
                f"Preço alvo atingido!\n"
                f"Preço atual: R$ {preco_atual:.2f}\n"
                f"Preço alvo: R$ {self.config['preco_alvo']:.2f}"
            )
            
            self.enviar_email(
                "Preço Alvo Atingido! - Ryzen 9 7900X",
                mensagem_alvo
            )
    
    def iniciar_navegador(self):
        self.driver = webdriver.Chrome(options=self.options)
        
    def fechar_navegador(self):
        self.driver.quit()
        
    #OBTER PREÇO KABUM => RETORNA preco
    def obter_preco(self):
        try:
            self.driver.get(self.url_kabum)
            
            # Aguardar 10 segundos até que o elemento de preço seja visível
            preco_element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//b [contains(@class, 'regularPrice')]"))
            )
            preco = preco_element.text.replace('R$', '').replace('.', '').replace(',', '.').strip()
            return float(preco)
            
        except Exception as e:
            print(f"Erro ao obter preço: {str(e)}")
            return None
        
    #OBTER PREÇO PICHAU => RETORNA preco_pichau
    def obter_preco_pichau(self):
        try:
            self.driver.get(self.url_pichau)
            
            # Aguardar 10 segundos até que o elemento de preço seja visível
            preco_element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div [contains(@class, 'jss356')]"))
            )
            preco_pichau = preco_element.text.replace('R$', '').replace('.', '').replace(',', '.').strip()
            return float(preco_pichau)
            
        except Exception as e:
            print(f"Erro ao obter preço: {str(e)}")
            return None
            
    def salvar_dados(self, preco):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        with open('historico_precos.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([timestamp, preco])
            
    #SALVAR DADOS PICHAU
    def dados_pichau(self, preco_pichau):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        with open('historico_pichau.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([timestamp, preco_pichau])

    #MONITORAR PICHAU
    def monitorar_pichau(self):
        try:
            self.iniciar_navegador()
            preco_pichau = self.obter_preco_pichau()
            
            if preco_pichau:
                self.verificar_alteracao_preco(preco_pichau)
                self.salvar_dados(preco_pichau)
                self.ultimo_preco = preco_pichau
                print(f"Preço atual: R$ {preco_pichau:.2f}")
                print(f"Dados salvos em: historico_pichau.csv")
                
        finally:
            self.fechar_navegador()


    def monitorar(self):
        try:
            self.iniciar_navegador()
            preco = self.obter_preco()
            preco_pichau = self.obter_preco_pichau()
            
            if preco:
                self.verificar_alteracao_preco(preco)
                self.salvar_dados(preco)
                self.ultimo_preco = preco
                print(f"Preço atual: R$ {preco:.2f}")
                print(f"Dados salvos em: historico_precos.csv")

            elif preco_pichau:
                self.verificar_alteracao_preco(preco_pichau)
                self.salvar_dados(preco_pichau)
                self.ultimo_preco = preco
                print(f"Preço atual: R$ {preco_pichau:.2f}")
                print(f"Dados salvos em: historico_pichau.csv")
                
        finally:
            self.fechar_navegador()

if __name__ == "__main__":
    monitor = MonitorPrecoKabum()
    monitor.monitorar() 