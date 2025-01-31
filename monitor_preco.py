from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import csv
import time

class MonitorPrecoKabum:
    def __init__(self):
        # Configurar opções do Chrome
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--headless')  # Executar em modo headless
        self.options.add_argument('--disable-gpu')
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--disable-dev-shm-usage')
        
        # URL do produto
        self.url = "https://www.kabum.com.br/produto/378412/processador-amd-ryzen-9-7900x-5-6ghz-max-turbo-cache-76mb-am5-12-nucleos-video-integrado-100-100000589wof"
        
    def iniciar_navegador(self):
        self.driver = webdriver.Chrome(options=self.options)
        
    def fechar_navegador(self):
        self.driver.quit()
        
    def obter_preco(self):
        try:
            self.driver.get(self.url)
            
            # Aguardar até que o elemento de preço seja visível
            preco_element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//h4[contains(@class, 'finalPrice')]"))
            )
            
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
                self.salvar_dados(preco)
                print(f"Preço atual: R$ {preco:.2f}")
                print(f"Dados salvos em: historico_precos.csv")
                
        finally:
            self.fechar_navegador()

if __name__ == "__main__":
    monitor = MonitorPrecoKabum()
    monitor.monitorar() 