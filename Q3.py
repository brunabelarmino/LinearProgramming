import pulp
from pulp import *

#número de lugares onde os corredores se encontram
n=8

#matriz nxn com os valores binários para cada encontro
A={}

A=[
[0,1,0,1,0,0,0,0], 
[1,0,1,0,1,0,0,0],
[0,1,0,0,0,1,0,0],
[1,0,0,0,1,0,0,1],
[0,1,0,1,0,1,1,0],
[0,0,1,0,1,0,0,0],
[0,0,0,0,1,0,0,1],
[0,0,0,1,0,0,1,0]
]

prob = LpProblem("Problema das Câmeras", LpMinimize)

#declara variáveis de decisão
status_camera_encontro = pulp.LpVariable.dicts("status_camera_encontro",[(j) for j in range(n)],0,1,cat = 'Integer') #Definir variável do status de cada local

prob += (pulp.lpSum([status_camera_encontro[x] for x in range(n)])), "Soma do número de cameras" #Função objetivo

#for i in range(n):
 # prob += (
 #     pulp.lpSum([A[i][numero]*status_camera_encontro[i] for numero in range(i+1,8)]) ==  [A[i][numero] for numero in range(i+1,8)]
 # )
for i in range(n):
  for numero in range(n):
    if A[i][numero] != 0:
      prob += lpSum([A[i][numero]*(status_camera_encontro[numero]+status_camera_encontro[i])])>= 1

  
prob.solve()

for v in prob.variables():
  print(v.name, "=", v.varValue)

  