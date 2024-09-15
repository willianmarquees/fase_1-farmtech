import pandas as pd
import os

# Menu de Navegação
home = """
    ╔═══════╣ FarmCalculator ╠═══════╗
    ║                                ║
    ║    1 -> Entrada de dados       ║
    ║    2 -> Saída de dados         ║
    ║    3 -> Atualizar dados        ║
    ║    4 -> Deletar dados          ║
    ║    5 -> Sair do programa       ║
    ║                                ║
    ╚════════════════════════════════╝
"""

# Verifica se o arquivo 'dados.csv' existe
if os.path.exists('dados.csv'):
    dados = pd.read_csv('dados.csv', sep=";")
else:
    # Se não existir, cria um DataFrame vazio com as colunas necessárias
    dados = pd.DataFrame(columns=["id", "cultura", "largura", "comprimento", "area", "fileiras",
                                  "plantas_por_fileira", "total_plantas", "insumo_total", "tempo_plantio",
                                  "espacamento_fileira_cm", "espacamento_planta_cm"])

# Função para calcular a área
def calcular_area(largura, comprimento):
    return largura * comprimento

# Função para calcular o número de fileiras baseado no espaçamento (em cm) e na largura do campo (em metros)
def calcular_fileiras(largura, espacamento_fileira_cm):
    espacamento_fileira_m = espacamento_fileira_cm / 100  # Converter cm para metros
    return int(largura / espacamento_fileira_m)

# Função para calcular o número de plantas por fileira baseado no espaçamento (em cm) e no comprimento do campo (em metros)
def calcular_plantas_por_fileira(comprimento, espacamento_planta_cm):
    espacamento_planta_m = espacamento_planta_cm / 100  # Converter cm para metros
    return int(comprimento / espacamento_planta_m)

# Função para calcular o manejo de insumos
def calcular_insumos(area, cultura):
    if cultura.lower() == "alface":
        insumo_por_m2 = 3  # Exemplo: 3 kg de cama de aviário por m² para alface
        return area * insumo_por_m2
    elif cultura.lower() == "tomate":
        insumo_por_m2 = 0.5  # Exemplo: 0.5 litros de pesticida por m² para tomate
        return area * insumo_por_m2
    else:
        print("Cultura não suportada.")
        return None

# Função para calcular o tempo de plantio com base na cultura
def calcular_tempo(cultura):
    if cultura.lower() == "alface":
        return 30  # 30 dias
    elif cultura.lower() == "tomate":
        return 90  # 90 dias
    else:
        print("Cultura não suportada.")
        return None

# Função para obter uma opção válida do menu
def obter_opcao_menu():
    while True:
        opcao = input("Escolha uma opção: ")
        if opcao.isdigit() and 1 <= int(opcao) <= 5:
            return int(opcao)
        else:
            print("Opção inválida. Por favor, insira um número entre 1 e 5.")

# Função para obter um número válido (float)
def obter_numero(mensagem):
    while True:
        valor = input(mensagem)
        try:
            numero = float(valor)
            if numero > 0:
                return numero
            else:
                print("Por favor, insira um número maior que zero.")
        except ValueError:
            print("Entrada inválida. Por favor, insira um número válido.")

# Função para obter um número inteiro válido
def obter_inteiro(mensagem):
    while True:
        valor = input(mensagem)
        if valor.isdigit():
            return int(valor)
        else:
            print("Entrada inválida. Por favor, insira um número inteiro válido.")

# Função para obter a cultura válida
def obter_cultura():
    culturas_disponiveis = ['alface', 'tomate']
    while True:
        cultura = input("Digite o tipo de cultura (Alface/Tomate): ").strip().lower()
        if cultura in culturas_disponiveis:
            return cultura.capitalize()
        else:
            print("Opção inválida. Por favor, escolha entre 'Alface' ou 'Tomate'.")

# Função para formatar os nomes das colunas
def formatar_colunas(colunas):
    colunas_formatadas = []
    for coluna in colunas:
        coluna = coluna.replace('_', ' ').title()
        colunas_formatadas.append(coluna)
    return colunas_formatadas

# Menu principal
def menu():
    global dados  # Para permitir atualização do DataFrame dentro da função

    while True:
        print(home)
        opcao = obter_opcao_menu()  # Usando a função de validação

        if opcao == 1:
            # Entrada de novos dados
            cultura = obter_cultura()
            largura = obter_numero("Digite a largura do campo em metros: ")
            comprimento = obter_numero("Digite o comprimento do campo em metros: ")
            espacamento_fileira_cm = obter_numero("Digite o espaçamento entre fileiras em centímetros: ")
            espacamento_planta_cm = obter_numero("Digite o espaçamento entre plantas na fileira em centímetros: ")

            area = calcular_area(largura, comprimento)
            fileiras = calcular_fileiras(largura, espacamento_fileira_cm)
            plantas_por_fileira = calcular_plantas_por_fileira(comprimento, espacamento_planta_cm)
            total_plantas = fileiras * plantas_por_fileira
            insumo_total = calcular_insumos(area, cultura)
            tempo_plantio = calcular_tempo(cultura)

            if area and fileiras and plantas_por_fileira and insumo_total is not None and tempo_plantio:
                nova_linha = {
                    "id": [len(dados) + 1],
                    "cultura": [cultura],
                    "largura": [largura],
                    "comprimento": [comprimento],
                    "area": [area],
                    "fileiras": [fileiras],
                    "plantas_por_fileira": [plantas_por_fileira],
                    "total_plantas": [total_plantas],
                    "insumo_total": [insumo_total],
                    "tempo_plantio": [tempo_plantio],
                    "espacamento_fileira_cm": [espacamento_fileira_cm],
                    "espacamento_planta_cm": [espacamento_planta_cm]
                }
                nova_linha_df = pd.DataFrame(nova_linha)
                dados = pd.concat([dados, nova_linha_df], ignore_index=True)

                # Salvando dados após a inserção
                dados.to_csv('dados.csv', sep=';', index=False)

                print(f"\nDados inseridos para {cultura}:\n"
                      f"  Área Total: {area} m²\n"
                      f"  Fileiras: {fileiras}\n"
                      f"  Plantas por Fileira: {plantas_por_fileira}\n"
                      f"  Total de Plantas: {total_plantas}\n"
                      f"  Insumo Total: {insumo_total} unidades\n"
                      f"  Tempo de Plantio: {tempo_plantio} dias\n"
                      f"  Espaçamento entre Fileiras: {espacamento_fileira_cm} cm\n"
                      f"  Espaçamento entre Plantas: {espacamento_planta_cm} cm")
            else:
                print("Erro ao calcular os dados. Verifique as entradas.")

        elif opcao == 2:
            # Exibição de dados
            if dados.empty:
                print("Nenhum dado disponível.")
            else:
                print("\nEscolha o formato de exibição:")
                print("1 - Lista")
                print("2 - Tabela")
                while True:
                    sub_opcao = input("Opção: ")
                    if sub_opcao == '1':
                        # Exibição em formato de lista
                        for index, linha in dados.iterrows():
                            print(f"\nID {linha['id']}:")
                            print(f"  Cultura: {linha['cultura']}")
                            print(f"  Largura: {linha['largura']} metros")
                            print(f"  Comprimento: {linha['comprimento']} metros")
                            print(f"  Área: {linha['area']} m²")
                            print(f"  Fileiras: {linha['fileiras']}")
                            print(f"  Plantas por Fileira: {linha['plantas_por_fileira']}")
                            print(f"  Total de Plantas: {linha['total_plantas']}")
                            print(f"  Insumo Total: {linha['insumo_total']} unidades")
                            print(f"  Tempo de Plantio: {linha['tempo_plantio']} dias")
                            print(f"  Espaçamento entre Fileiras: {linha['espacamento_fileira_cm']} cm")
                            print(f"  Espaçamento entre Plantas: {linha['espacamento_planta_cm']} cm")
                        break
                    elif sub_opcao == '2':
                        # Exibição em formato de tabela com colunas formatadas
                        dados_formatados = dados.copy()
                        dados_formatados.columns = formatar_colunas(dados.columns)
                        print("\nDados em formato de tabela:\n")
                        print(dados_formatados.to_string(index=False))
                        break
                    else:
                        print("Opção inválida. Por favor, escolha '1' ou '2'.")

        elif opcao == 3:
            # Atualizar dados
            if dados.empty:
                print("Nenhum dado disponível para atualizar.")
                continue

            print(f'Selecione entre 1 e { len(dados) }')
            index = obter_inteiro("Digite o número da cultura que deseja atualizar: ") - 1
            if 0 <= index < len(dados):
                # Obter os valores antigos
                old_largura = dados.loc[index, "largura"]
                old_comprimento = dados.loc[index, "comprimento"]
                old_espacamento_fileira_cm = dados.loc[index, "espacamento_fileira_cm"]
                old_espacamento_planta_cm = dados.loc[index, "espacamento_planta_cm"]
                old_area = dados.loc[index, "area"]
                old_fileiras = dados.loc[index, "fileiras"]
                old_plantas_por_fileira = dados.loc[index, "plantas_por_fileira"]
                old_total_plantas = dados.loc[index, "total_plantas"]
                old_insumo_total = dados.loc[index, "insumo_total"]
                old_tempo_plantio = dados.loc[index, "tempo_plantio"]

                # Solicitar novos valores
                nova_largura = obter_numero("Digite a nova largura do campo em metros: ")
                novo_comprimento = obter_numero("Digite o novo comprimento do campo em metros: ")
                novo_espacamento_fileira_cm = obter_numero("Digite o novo espaçamento entre fileiras em centímetros: ")
                novo_espacamento_planta_cm = obter_numero("Digite o novo espaçamento entre plantas em centímetros: ")

                # Calcular novos valores derivados
                nova_area = calcular_area(nova_largura, novo_comprimento)
                novas_fileiras = calcular_fileiras(nova_largura, novo_espacamento_fileira_cm)
                novas_plantas_por_fileira = calcular_plantas_por_fileira(novo_comprimento, novo_espacamento_planta_cm)
                novo_total_plantas = novas_fileiras * novas_plantas_por_fileira
                novo_insumo_total = calcular_insumos(nova_area, dados.iloc[index]["cultura"])

                # Exibir comparação dos valores
                print("\nComparação dos valores:")
                print(f"Largura: {old_largura} metros                 ----->   Largura: {nova_largura} metros")
                print(f"Comprimento: {old_comprimento} metros             ----->   Comprimento: {novo_comprimento} metros")
                print(f"Área: {old_area} m²                      ----->   Área: {nova_area} m²")
                print(f"Fileiras: {old_fileiras}                       ----->   Fileiras: {novas_fileiras}")
                print(f"Plantas por Fileira: {old_plantas_por_fileira}           ----->   Plantas por Fileira: {novas_plantas_por_fileira}")
                print(f"Total de Plantas: {old_total_plantas}           ----->   Total de Plantas: {novo_total_plantas}")
                print(f"Insumo Total: {old_insumo_total} unidades       ----->   Insumo Total: {novo_insumo_total} unidades")
                print(f"Tempo de Plantio: {old_tempo_plantio} dias           ----->   Tempo de Plantio: {old_tempo_plantio} dias")
                print(f"Espaçamento entre Fileiras: {old_espacamento_fileira_cm} cm   ----->   Espaçamento entre Fileiras: {novo_espacamento_fileira_cm} cm")
                print(f"Espaçamento entre Plantas: {old_espacamento_planta_cm} cm    ----->   Espaçamento entre Plantas: {novo_espacamento_planta_cm} cm")

                # Solicitar confirmação
                confirmacao = input("Tem certeza que deseja aplicar as alterações? (s/n): ").strip().lower()
                if confirmacao == 's':
                    # Aplicar as alterações
                    dados.loc[index, "largura"] = nova_largura
                    dados.loc[index, "comprimento"] = novo_comprimento
                    dados.loc[index, "area"] = nova_area
                    dados.loc[index, "fileiras"] = novas_fileiras
                    dados.loc[index, "plantas_por_fileira"] = novas_plantas_por_fileira
                    dados.loc[index, "total_plantas"] = novo_total_plantas
                    dados.loc[index, "insumo_total"] = novo_insumo_total
                    dados.loc[index, "espacamento_fileira_cm"] = novo_espacamento_fileira_cm
                    dados.loc[index, "espacamento_planta_cm"] = novo_espacamento_planta_cm

                    # Salvando dados após a atualização
                    dados.to_csv('dados.csv', sep=';', index=False)

                    print("Dados atualizados com sucesso.")
                else:
                    print("Operação cancelada. Nenhum dado foi alterado.")
            else:
                print("Índice inválido.")

        elif opcao == 4:
            # Deletar dados
            if dados.empty:
                print("Nenhum dado disponível para deletar.")
                continue

            print(f'Selecione entre 1 e { len(dados) }')
            index = obter_inteiro("Digite o número da cultura que deseja deletar: ") - 1
            if 0 <= index < len(dados):
                # Mostrando o registro que será deletado
                print(f"\nVocê selecionou o registro {dados.loc[index, 'id']}:\n")
                print(f"  Cultura: {dados.loc[index, 'cultura']}")
                print(f"  Largura: {dados.loc[index, 'largura']} metros")
                print(f"  Comprimento: {dados.loc[index, 'comprimento']} metros")
                print(f"  Área: {dados.loc[index, 'area']} m²")
                print(f"  Fileiras: {dados.loc[index, 'fileiras']}")
                print(f"  Plantas por Fileira: {dados.loc[index, 'plantas_por_fileira']}")
                print(f"  Total de Plantas: {dados.loc[index, 'total_plantas']}")
                print(f"  Insumo Total: {dados.loc[index, 'insumo_total']} unidades")
                print(f"  Tempo de Plantio: {dados.loc[index, 'tempo_plantio']} dias")
                print(f"  Espaçamento entre Fileiras: {dados.loc[index, 'espacamento_fileira_cm']} cm")
                print(f"  Espaçamento entre Plantas: {dados.loc[index, 'espacamento_planta_cm']} cm")

                # Solicita confirmação do usuário
                confirmacao = input(f"Tem certeza que deseja deletar o registro {dados.loc[index, 'id']}? (s/n): ").strip().lower()
                if confirmacao == 's':
                    dados = dados.drop(index).reset_index(drop=True)
                    # Atualizar IDs após remoção
                    dados['id'] = range(1, len(dados) + 1)
                    # Salvando dados após a exclusão
                    dados.to_csv('dados.csv', sep=';', index=False)
                    print("Cultura deletada com sucesso.")
                else:
                    print("Operação cancelada. Nenhum dado foi deletado.")
            else:
                print("Índice inválido.")

        elif opcao == 5:
            # Salva as alterações no arquivo CSV antes de sair
            dados.to_csv('dados.csv', sep=';', index=False)
            print("Saindo do programa...")
            break

        else:
            print("Opção inválida. Tente novamente.")

# Executando o menu
menu()
