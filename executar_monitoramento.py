from monitor_preco import MonitorPrecoKabum
from monitor_preco import enviar_email
import time
import schedule

def executar_monitoria():
    monitor = MonitorPrecoKabum()
    monitor.monitorar()

# Agendar execução a cada 5 minutos
schedule.every(1).minutes.do(executar_monitoria)

# Executar imediatamente pela primeira vez
executar_monitoria()
enviar_email()

# Manter o script rodando
while True:
    schedule.run_pending()
    time.sleep(1) 