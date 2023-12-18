import pandas as pd

nome_arquivo = input('Digite o nome do arquivo: ')

df = pd.read_csv(nome_arquivo, sep=',')

def converter_moeda_para_float(valor):
    return float(valor.replace('R$', '').replace(',', '.').strip())

df["Preço"] = df["Preço"].apply(converter_moeda_para_float)

def separar_valor_lance(string):
    return int(string.replace('lances', '').replace('lance', '').strip())

df["Qtd Lances"] = df["Qtd Lances"].apply(separar_valor_lance)

def somar_leilão():
    linhas_com_lances = df[df["Qtd Lances"] > 0]
    soma = linhas_com_lances["Preço"].sum()
    return soma

def calcular_valor_liquido():
    descontos = (somar_leilão() * 35) /100
    liquido = somar_leilão() - descontos
    return liquido

print(f'Valor total do leilão: R$ {somar_leilão()}')
print(f'Valor líquido do leilão: R$ {calcular_valor_liquido()}')
input('Aperte <ENTER> para sair.')

