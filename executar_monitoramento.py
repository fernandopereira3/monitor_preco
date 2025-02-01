from monitor_preco import MonitorPrecoKabum
import time
import schedule

def executar_monitoria():
    monitor = MonitorPrecoKabum()
    monitor.monitorar()

# Agendar execução a cada 5 minutos
schedule.every(5).minutes.do(executar_monitoria)

# Executar imediatamente pela primeira vez
executar_monitoria()

# Manter o script rodando
while True:
    schedule.run_pending()
    time.sleep(1) 