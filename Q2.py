import pulp
import numpy as np
import json

# Importando parametros de um JSON

with open('data.json') as json_file:
    data = json.load(json_file)

dist_between_points = np.array(data["dist_between_points"])

dist_point_to_company = np.array(data["dist_point_to_company"])

workers_per_point = np.array(data["workers_per_point"])

# Definindo parametros relativos a frota de onibus

capacity = np.concatenate((np.array([48]*10), np.array([16]*30)))
mensal_cost = np.concatenate((np.array([15_000]*10), np.array([4_000]*30)))/22
km_cost = np.concatenate((np.array([3.20]*10), np.array([2.90]*30)))

# Matriz de distancias com a distancia dos pontos ate a empresa e entre pontos

distances = np.array(np.zeros(31*31)).reshape(31,31)
distances[1:,1:] = dist_between_points
distances[0,1:], distances[1:,0] = dist_point_to_company, dist_point_to_company.T

# Variaveis binárias de decisao

bin = pulp.LpVariable.dicts("Uso da rota por veiculo", (range(31), range(31), range(40)), cat='Binary')

# Array de tuplas 

roads = [(i, j, k) for i in range(31) for j in range(31) for k in range(40)]

# Criacao do problema

prob = pulp.LpProblem("Otimizacao", pulp.LpMinimize)

# Definindo a funcao objetivo

prob += (
    pulp.lpSum([bin[i][j][k]*distances[i,j]*km_cost[k] for (i,j,k) in roads]) + pulp.lpSum([(bin[0][j][k]) * mensal_cost[k] for k in range(40) for j in range(1,31)])
)

# Adicionando as constraints 

for i in range(1,31):
  prob += (
      pulp.lpSum([bin[i][j][k] for j in range(31) for k in range(40)]) == 1
  )

for j in range(1,31):
  prob += (
      pulp.lpSum([bin[i][j][k] for i in range(31) for k in range(40)]) == 1
  )

for k in range(40):

  prob += (
      pulp.lpSum([bin[i][0][k] for i in range(31)]) == 1
  )

  prob += (
      pulp.lpSum([bin[i][j][k] * workers_per_point[j] for i in range(31) for j in range(31)]) <= capacity[k]
  )
  
  prob += (
      pulp.lpSum([bin[i][j][k] * (workers_per_point[j]) for i in range(31) for j in range(31)]) == pulp.lpSum([bin[i][j][k] * (workers_per_point[i]) for i in range(31) for j in range(31)])
  )


  prob += (
        pulp.lpSum([bin[i][j][k] + bin[j][i][k] for i in range(1,31) for j in range(1,31)]) <= 1
  )


# Resolvendo o problema
optimization_result = prob.solve()

# Escrevendo o custo total diário
print("Custo total de transporte = ", pulp.value(prob.objective))

# Checando se a solução é ótima
assert optimization_result == pulp.LpStatusOptimal