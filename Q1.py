import pulp
from pulp import *

#número de regiões
n=5

#número de locais
m=5

#matriz nxm com os valores binários para cada região
A={}

A=[
[1,1,0,0,0], 
[1,1,1,0,0],
[0,1,0,1,0],
[0,1,0,1,1],
[0,0,1,1,1]
]

prob = LpProblem("Problema do Samu", LpMinimize)

#declara variáveis de decisão
status_local = pulp.LpVariable.dicts("status_local",[(j) for j in range(m)],0,1,cat = 'Integer') #Definir variável do status de cada local

prob += (pulp.lpSum([status_local[x] for x in range(m)])), "Soma das unidades abertas" #Função objetivo

for i in range(n):
  prob += (
      pulp.lpSum([A[i][numero]*status_local[numero] for numero in range(m)]) >= 1
  )

prob.solve()

for v in prob.variables():
  print(v.name, "=", v.varValue)