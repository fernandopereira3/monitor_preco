from monitor_preco import *
import time
import schedule
import smtplib
from email.mime.text import MIMEText


def executar_monitoria():
    monitor = MonitorPrecoKabum()
    monitor.monitorar()

def start():
        config = {
            'email_remetente': '',
            'email_senha': '',
            'email_destinatario': ''
        }
    
        if not all([config['email_remetente'], 
                    config['email_senha'], 
                    config['email_destinatario']]):
            return
        
        try:
            msg = MIMEText("Iniciado o Monitoramento da Placa de Video")
            msg['Subject'] = "Monitoramento iniciado"
            msg['From'] = config['email_remetente']
            msg['To'] = config['email_destinatario']
        
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.login(config['email_remetente'], config['email_senha'])
            server.send_message(msg)
            server.quit()
        
        except Exception as e:
            print(f"Erro ao enviar email: {str(e)}")


# Agendar execução a cada 5 minutos
schedule.every(1).minutes.do(executar_monitoria)

# Executar imediatamente pela primeira vez
executar_monitoria()
start()

# Manter o script rodando
while True:
    schedule.run_pending()
    time.sleep(1) 