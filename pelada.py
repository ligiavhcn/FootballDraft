import random
import pandas as pd




def create_teams(players_dict, selected_players):
    # create the selected_players and remaing lists
    selected = [p for p in selected_players if p in players_dict]
    remaining = [p for p in players_dict if p not in selected]

    # Add the players to teams
    team1 = selected[:6]
    team2 = selected[6:]

    # Ensure that each team has at least 1 defender, 1 forward, and 1 midfielder.
    for i in range(6):
            if len(team1) < 6 and len(remaining) > 0:
                if 'Zagueira' not in [players_dict[p] for p in team1]:
                    zagueira_index = [i for i, r in enumerate(remaining) if players_dict[r] == 'Zagueira'][0] # defender
                    team1.append(remaining[zagueira_index])
                    remaining.remove(remaining[zagueira_index])
                elif 'Atacante' not in [players_dict[p] for p in team1]:
                    atacante_index = [i for i, r in enumerate(remaining) if players_dict[r] == 'Atacante'][0] # forward
                    team1.append(remaining[atacante_index])
                    remaining.remove(remaining[atacante_index])
                elif 'Meio-Campo' not in [players_dict[p] for p in team1]:
                    meio_campo_index = [i for i, r in enumerate(remaining) if players_dict[r] == 'Meio-Campo'][0] # midfielder
                    team1.append(remaining[meio_campo_index])
                    remaining.remove(remaining[meio_campo_index])
            if len(team2) < 6 and len(remaining) > 0:
                team2.append(remaining[i])

    return team1, team2

# Create a dictionary with the players and their positions
tabela_atletas = pd.read_excel('data.xlsx')
# display(tabela_atletas)

players_dict = tabela_atletas.set_index('name')['position'].to_dict()
# print(players_dict)


# Load the .txt file with the selected team
with open('selected_players.txt', 'r') as file:
    selected_players = file.read().splitlines()

if tuple(selected_players) in players_dict.keys():

    # Create randomized teams
    team1, team2 = create_teams(players_dict, selected_players)

    # Print randomized teams
    print("Time Vermelho:", team1)
    print("Time Branco:", team2)
else:
    # Asks if there is someone outside of the list in the data.
    nome_convidada = input('Qual o nome da convidada? ') # name
    posicao_convidada = input('Qual posição da convidada? ') # position
    players_dict[nome_convidada] = posicao_convidada # add to the dict
    
    # Create randomized teams
    team1, team2 = create_teams(players_dict, selected_players)

    # Print randomized teams
    print("Time Vermelho:", team1)
    print("Time Branco:", team2)
    
    
