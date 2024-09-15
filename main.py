import pandas as pd

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

# Dados iniciais em DataFrame
tabela = pd.read_csv('dados.csv', sep=";")

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

# Menu principal
def menu():
    global tabela  # Para permitir atualização do DataFrame dentro da função

    while True:
        print(home)
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            # Entrada de novos dados
            cultura = input("Digite o tipo de cultura (Alface/Tomate): ")
            largura = float(input("Digite a largura do campo em metros: "))
            comprimento = float(input("Digite o comprimento do campo em metros: "))
            espacamento_fileira_cm = float(input("Digite o espaçamento entre fileiras em centímetros: "))
            espacamento_planta_cm = float(input("Digite o espaçamento entre plantas na fileira em centímetros: "))

            area = calcular_area(largura, comprimento)
            fileiras = calcular_fileiras(largura, espacamento_fileira_cm)
            plantas_por_fileira = calcular_plantas_por_fileira(comprimento, espacamento_planta_cm)
            total_plantas = fileiras * plantas_por_fileira
            insumo_total = calcular_insumos(area, cultura)
            tempo_plantio = calcular_tempo(cultura)

            if area and fileiras and plantas_por_fileira and insumo_total is not None and tempo_plantio:
                nova_linha = {
                    "id": tabela['id'].count() + 1,
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
                tabela = pd.concat([tabela, nova_linha_df], ignore_index=True)

                print(f"\nDados inseridos para {cultura}:\n"
                      f"Área Total: {area} m²\n"
                      f"Fileiras: {fileiras}\n"
                      f"Plantas por Fileira: {plantas_por_fileira}\n"
                      f"Total de Plantas: {total_plantas}\n"
                      f"Insumo Total: {insumo_total} unidades\n"
                      f"Tempo de Plantio: {tempo_plantio} dias\n"
                      f"Espaçamento entre Fileiras: {espacamento_fileira_cm} cm\n"
                      f"Espaçamento entre Plantas: {espacamento_planta_cm} cm")

        elif opcao == '2':
            # Exibição de dados
            if tabela.empty:
                print("Nenhum dado disponível.")
            else:
                for index, linha in tabela.iterrows():
                    print(f"\nID {index + 1}:")
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

        elif opcao == '3':
            # Atualizar dados
            index = int(input("Digite o número da cultura que deseja atualizar: ")) - 1
            if 0 <= index < len(tabela):
                nova_largura = float(input("Digite a nova largura do campo em metros: "))
                novo_comprimento = float(input("Digite o novo comprimento do campo em metros: "))
                novo_espacamento_fileira_cm = float(input("Digite o novo espaçamento entre fileiras em centímetros: "))
                novo_espacamento_planta_cm = float(input("Digite o novo espaçamento entre plantas em centímetros: "))

                nova_area = calcular_area(nova_largura, novo_comprimento)
                novas_fileiras = calcular_fileiras(nova_largura, novo_espacamento_fileira_cm)
                novas_plantas_por_fileira = calcular_plantas_por_fileira(novo_comprimento, novo_espacamento_planta_cm)
                novo_total_plantas = novas_fileiras * novas_plantas_por_fileira
                novo_insumo_total = calcular_insumos(nova_area, tabela.iloc[index]["cultura"])

                tabela.loc[index, "largura"] = nova_largura
                tabela.loc[index, "comprimento"] = novo_comprimento
                tabela.loc[index, "area"] = nova_area
                tabela.loc[index, "fileiras"] = novas_fileiras
                tabela.loc[index, "plantas_por_fileira"] = novas_plantas_por_fileira
                tabela.loc[index, "total_plantas"] = novo_total_plantas
                tabela.loc[index, "insumo_total"] = novo_insumo_total
                tabela.loc[index, "espacamento_fileira_cm"] = novo_espacamento_fileira_cm
                tabela.loc[index, "espacamento_planta_cm"] = novo_espacamento_planta_cm

                print("Dados atualizados com sucesso.")
            else:
                print("Índice inválido.")

        elif opcao == '4':
            # Deletar dados
            index = int(input("Digite o número da cultura que deseja deletar: ")) - 1
            if 0 <= index < len(tabela):
                # Mostrando o registro que será deletado
                    print(f"Você selecionou o registro {index + 1}:\n")
                    print(f"  Cultura: {tabela.loc[index, 'cultura']}")
                    print(f"  Largura: {tabela.loc[index, 'largura']} metros")
                    print(f"  Comprimento: {tabela.loc[index, 'comprimento']} metros")
                    print(f"  Área: {tabela.loc[index, 'area']} m²")
                    print(f"  Fileiras: {tabela.loc[index, 'fileiras']}")
                    print(f"  Plantas por Fileira: {tabela.loc[index, 'plantas_por_fileira']}")
                    print(f"  Total de Plantas: {tabela.loc[index, 'total_plantas']}")
                    print(f"  Insumo Total: {tabela.loc[index, 'insumo_total']} unidades")
                    print(f"  Tempo de Plantio: {tabela.loc[index, 'tempo_plantio']} dias")
                    print(f"  Espaçamento entre Fileiras: {tabela.loc[index, 'espacamento_fileira_cm']} cm")
                    print(f"  Espaçamento entre Plantas: {tabela.loc[index, 'espacamento_planta_cm']} cm")

                    # Solicita confirmação do usuário
                    confirmacao = input(f"Tem certeza que deseja deletar o registro {index + 1}? (s/n): ").strip().lower()
                    if confirmacao == 's':
                        tabela = tabela.drop(index).reset_index(drop=True)
                        print("Cultura deletada com sucesso.")
                    else:
                        print("Operação cancelada. Nenhum dado foi deletado.")
            else:
                print("Índice inválido.")

        elif opcao == '5':
            print("Saindo do programa...")
            break

        else:
            print("Opção inválida. Tente novamente.")

# Executando o menu
menu()
