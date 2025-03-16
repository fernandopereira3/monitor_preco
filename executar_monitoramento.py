from monitor_preco import MonitorPreco
import time
import schedule

def executar_monitoria():
    monitor = MonitorPreco()
    monitor.monitorar()

# Agendar execução a cada 5 minutos
schedule.every(1).minutes.do(executar_monitoria)

# Executar imediatamente pela primeira vez
executar_monitoria()
MonitorPreco.enviar_inicio()

# Manter o script rodando
while True:
    schedule.run_pending()
    time.sleep(1) 