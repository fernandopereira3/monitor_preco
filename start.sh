date=$(date '+%Y-%m-%d')

cd /home/fernando/repositorios/monitor_preco/ #linux
python3 -m venv .
source /home/fernando/repositorios/monitor_preco/bin/activate #linux
pip install -r requirements.txt
git add .
git commit -m "$date"
git push origin main
python3 /home/fernando/repositorios/monitor_preco/executar_monitoramento.py #Linux