import requests
from lxml import html
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
import pandas as pd

def obter_dados_ebay(url):
    req = requests.get(url)
    tree = html.fromstring(req.text)
    produto = tree.xpath('//span[@class="ux-textspans ux-textspans--BOLD"]/text()')[1].strip()
    preco = tree.xpath('//span[@class="ux-textspans ux-textspans--SECONDARY ux-textspans--BOLD"]/text()')[0].strip()
    qtd_lances = tree.xpath('//span[@class="ux-textspans"]/text()')[14].strip()
    data = lambda: datetime.now().strftime('%d-%m-%Y %H:%M:%S')
    return produto, preco, qtd_lances, data()

def obter_dados_ebay_ativamente(url):
    req = requests.get(url)
    tree = html.fromstring(req.text)
    produto = tree.xpath('//span[@class="ux-textspans ux-textspans--BOLD"]/text()')[0].strip()
    preco = tree.xpath('//span[@class="ux-textspans ux-textspans--SECONDARY ux-textspans--BOLD"]/text()')[0].strip()
    qtd_lances = tree.xpath('//span[@class="ux-textspans"]/text()')[12].strip()
    data = lambda: datetime.now().strftime('%d-%m-%Y %H:%M:%S')
    return produto, preco, qtd_lances, data()

def ler_urls_do_arquivo(nome_arquivo):
    try:
        with open(nome_arquivo, 'r') as file:
            urls = [line.strip() for line in file if line.strip()]
        return urls
    except FileNotFoundError:
        print(f"Arquivo '{nome_arquivo}' não encontrado.")
        return []

def tarefa_agendada(urls):
    resultados = []

    for url in urls:
        resultado = obter_dados_ebay(url)
        resultados.append(resultado)
        print(resultado)
    print('======================================================================================')
    df = pd.DataFrame(resultados, columns=['Produto', 'Preço', 'Qtd Lances', 'Data'])
    df.to_csv('dados_leilão_finalizado.csv', index=False)

def tarefa_agendada_ativamente(urls):
    resultados = []

    for url in urls:
        resultado = obter_dados_ebay_ativamente(url)
        resultados.append(resultado)
        print(resultado)
    print('======================================================================================')
    df = pd.DataFrame(resultados, columns=['Produto', 'Preço', 'Qtd Lances', 'Data'])
    df.to_csv('dados_leilão_em_progresso.csv', index=False)

def monitorar_ativamente(urls):
    sched = BlockingScheduler()

    @sched.scheduled_job('interval', seconds=10)
    def job():
        tarefa_agendada_ativamente(urls)

    sched.start()

if __name__ == '__main__':
    # nome_arquivo = input("Digite o nome do arquivo TXT que contém os URLs: ")
    urls = 'url.txt'

    if urls:
        print("Escolha uma opção:")
        print("1. Monitorar ativamente")
        print("2. Apurar resultado final")
        opcao = input("Digite o número da opção desejada: ")

        if opcao == '1':
            monitorar_ativamente(urls)
        elif opcao == '2':
            tarefa_agendada(urls)
        else:
            print("Opção inválida. Encerrando o programa.")
