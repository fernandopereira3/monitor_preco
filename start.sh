date=$(date '+%Y-%m-%d')

#cd /home/fernando/repositorios/monitor_preco/ #linux
cd /Users/fernando/Repositorios_Git/monitor_preco/ #mac
python3 -m venv .
#source /home/fernando/repositorios/monitor_preco/bin/activate #linux
source /Users/fernando/Repositorios_Git/monitor_preco/bin/activate # mac
pip install -r requirements.txt
git add .
git commit -m "$date"
git push orgin main
#python3 /home/fernando/repositorios/monitor_preco/executar_monitoramento.py #Linux
python3 /Users/fernando/Repositorios_Git/monitor_preco/executar_monitoramento.py