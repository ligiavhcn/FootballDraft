import pandas as pd
import random

# Função para sortear os times
def sort_teams(players):
    # Separar as jogadoras por posição
    defenders = players[players['Posição'] == 'Zagueira']
    midfielders = players[players['Posição'] == 'Meio-Campo']
    forwards = players[players['Posição'] == 'Atacante']

    # Garantir que temos pelo menos uma jogadora de cada posição em cada time
    if len(defenders) < 2 or len(midfielders) < 2 or len(forwards) < 2:
        print("Não há jogadoras suficientes para formar os times com as posições necessárias.")
        return [], []

    # Sortear uma jogadora de cada posição para cada time
    team1 = []
    team2 = []

    # Amostras garantidas
    team1.append(defenders.sample(1).iloc[0])
    team2.append(defenders.drop(team1[-1].name).sample(1).iloc[0])

    team1.append(midfielders.sample(1).iloc[0])
    team2.append(midfielders.drop(team1[-1].name).sample(1).iloc[0])

    team1.append(forwards.sample(1).iloc[0])
    team2.append(forwards.drop(team1[-1].name).sample(1).iloc[0])

    # Remover as jogadoras sorteadas
    remaining_players = players[~players['Nome'].isin([p['Nome'] for p in team1 + team2])]

    # Embaralhar as jogadoras restantes e completar os times
    remaining_players = remaining_players.sample(frac=1).reset_index(drop=True)
    team1 += remaining_players.iloc[:3].to_dict('records')
    team2 += remaining_players.iloc[3:6].to_dict('records')

    return team1, team2

# Função para exibir os times
def print_teams(team1, team2):
    if team1 and team2:
        print("Time Vermelho:")
        for player in team1:
            # print(f"{player['Nome']} - {player['Posição']}")
            print(player['Nome'], end=', ', sep=" " )

        print("\nTime Branco:")
        for player in team2:
            # print(f"{player['Nome']} - {player['Posição']}")
            print(player['Nome'], end=', ', sep=" " )
    else:
        print("Não foi possível formar os times.")

# Carregar os dados do arquivo Excel
data = pd.read_excel('data.xlsx')

# Ler as jogadoras selecionadas do arquivo de texto
with open('selected_players.txt', 'r') as file:
    selected_players = [line.strip() for line in file if line.strip()]

# Verificar se todas as jogadoras estão no arquivo Excel
data_names = set(data['Nome'].tolist())
new_players = [player for player in selected_players if player not in data_names]

# Se houver novas jogadoras, perguntar as posições e atualizar os dados
if new_players:
    new_data = []
    for player in new_players:
        position = input(f"Qual a posição da nova jogadora {player} (zagueira, meio-campo, atacante)? ")
        new_data.append({'Nome': player, 'Posição': position})
    
    # Atualizar o DataFrame com as novas jogadoras
    if new_data:
        new_df = pd.DataFrame(new_data)
        data = pd.concat([data, new_df], ignore_index=True)

# Filtrar as jogadoras selecionadas
selected_data = data[data['Nome'].isin(selected_players)]

# Sortear os times
team1, team2 = sort_teams(selected_data)

# Exibir os times
print_teams(team1, team2)

# Perguntar ao usuário se deseja sortear novamente
while True:
    novamente = input("\n\nDeseja sortear os times novamente? (s/n): \n").lower()
    if novamente == 's':
        team1, team2 = sort_teams(selected_data)
        print_teams(team1, team2)
    elif novamente == 'n':
        print("Bom jogo! Divirtam-se!")
        break
    else:
        print("Opção inválida. Por favor, escolha 's' para sim ou 'n' para não.")
