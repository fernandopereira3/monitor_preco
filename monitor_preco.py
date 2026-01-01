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
        self.url = "https://www.kabum.com.br/produto/725947/placa-de-video-xfx-swift-rx-9070-xt-triple-fan-gaming-edition-with-amd-radeon-16gb-gddr6-hdmi-3xdp-rdna-4-rx-97tswf3b9"

        # Carregar último preço conhecido
        self.ultimo_preco = self.carregar_ultimo_preco()
        
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
            
    def enviar_notificacao_desktop(self, titulo, mensagem):
        notification.notify(
            title=titulo,
            message=mensagem,
            app_icon=None,
            timeout=10,
        )
        
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
                f"Alteração no preço da Placa de Video!\n"
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
                "Preço Alvo Atingido!",
                mensagem_alvo
            )
    
    def iniciar_navegador(self):
        self.driver = webdriver.Chrome(options=self.options)
        
    def fechar_navegador(self):
        self.driver.quit()
        
    def obter_preco(self):
        try:
            self.driver.get(self.url)
            
            # Aguardar até que o elemento de preço seja visível
            preco_element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//*[@id='main-content']/div[1]/div[1]/div[1]/div[3]/div[3]/div[2]/span/b[1]"))
            )
            #//*[@id="main-content"]/div[1]/div[1]/div[1]/div[3]/div[3]/div[2]/span/b[1]
            
            # Extrair o preço
            preco = preco_element.text.replace('R$', '').replace('.', '').replace(',', '.').strip()
            return float(preco)
            
        except Exception as e:
            print(f"Erro ao obter preço: {str(e)}")
            return None
            
    def salvar_dados(self, preco):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        with open('historico_precos.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([timestamp, preco])
            
    def monitorar(self):
        try:
            self.iniciar_navegador()
            preco = self.obter_preco()
            
            if preco:
                self.verificar_alteracao_preco(preco)
                self.salvar_dados(preco)
                self.ultimo_preco = preco
                print(f"Preço atual: R$ {preco:.2f}")
                print(f"Dados salvos em: historico_precos.csv")
                
        finally:
            self.fechar_navegador()

if __name__ == "__main__":
    monitor = MonitorPrecoKabum()
    monitor.monitorar() 