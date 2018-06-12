from __future__ import print_function
from ortools.linear_solver import pywraplp


def main():
  # Instantiate a mixed-integer solver
  solver = pywraplp.Solver('SolveSupplyProblem', pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)
  cost1 = [[843, 1379, 682, 872, 483, 432, 1600, 2184, 684, 1361, 1213, 860, 760, 485, 748,
            888, 541, 1090, 502, 414, 577, 493, 1026, 1155, 902, 938, 1039, 123, 331, 552],
           [612, 1016, 1510, 832, 867, 764, 246, 1021, 738, 1724, 1393, 699, 1078, 742, 763,
            713, 699, 813, 817, 763, 967, 789, 1329, 738, 643, 897, 1238, 632, 744, 1008],
           [899, 957, 248, 980, 758, 648, 1002, 1831, 808, 1736, 1611, 752, 233, 560, 864,
            674, 826, 1033, 901, 826, 765, 686, 394, 977, 639, 470, 1320, 729, 977, 646],
           [782, 1267, 1018, 574, 602, 582, 1600, 1505, 780, 1086, 1033, 681, 1073, 744, 600,
            928, 595, 360, 492, 566, 814, 701, 1090, 789, 841, 744, 940, 650, 717, 929],
           [800, 1500, 700, 900, 800, 700, 1500, 1600, 800, 1800, 1600, 1000, 800, 1100, 1600, 700, 700,
            1600, 800, 800, 900, 900, 1000, 800, 1000, 1100, 1600, 1200, 1200, 1400]]

  cost2 = [[951, 1262, 0, 0, 0, 0, 0, 1055, 0, 1858, 2759, 0, 0, 0, 0, 949, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1152, 0, 0, 0],
           [976, 1312, 0, 0, 0, 0, 0, 1112, 0, 1932, 3041, 0, 0, 0, 0, 974, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1249, 0, 0, 0],
           [948, 1409, 0, 0, 0, 0, 0, 1127, 0, 1966, 3605, 0, 0, 0, 0, 945, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1323, 0, 0, 0],
           [1024, 1269, 0, 0, 0, 0, 0, 1101, 0, 1857, 2975, 0, 0, 0, 0, 1021, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1192, 0, 0, 0],
           [1000, 1200, 0, 0, 0, 0, 0, 1000, 0, 1950, 2900, 0, 0, 0, 0, 1100, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1200, 0, 0, 0]]

  cost3 = [[600, 600, 600, 600, 600, 600, 600, 600, 600, 600, 600, 600, 600, 600, 600, 600, 600, 600, 600, 600, 600, 600, 600, 600, 600, 600, 600, 600, 600, 600],
           [452, 452, 452, 452, 452, 452, 452, 452, 452, 452, 452, 452, 452, 452, 452, 452, 452, 452, 452, 452, 452, 452, 452, 452, 452, 452, 452, 452, 452, 452],
           [188, 188, 188, 188, 188, 188, 188, 188, 188, 188, 188, 188, 188, 188, 188, 188, 188, 188, 188, 188, 188, 188, 188, 188, 188, 188, 188, 188, 188, 188],
           [400, 400, 400, 400, 400, 400, 400, 400, 400, 400, 400, 400, 400, 400, 400, 400, 400, 400, 400, 400, 400, 400, 400, 400, 400, 400, 400, 400, 400, 400],
           [1200, 1200, 1200, 1200, 1200, 1200, 1200, 1200, 1200, 1200, 1200, 1200, 1200, 1200, 1200, 1200, 1200, 1200, 1200, 1200, 1200, 1200, 1200, 1200, 1200, 1200, 1200, 1200, 1200, 1200]]

  total_demand = [3195, 2539, 15137, 24, 1344, 676, 7020, 679, 7, 604, 4, 7, 474, 17, 0, 1081, 1263, 0, 1420, 2820, 609, 485, 1964, 2, 9, 7, 1268, 0, 4, 1532]
  total_cap = [22148*0.8, 15637*0.8, 24090*0.8, 1440*0.8, 700*0.8]

  # Maximum total of task sizes for any worker
  num_plants = len(total_cap)
  num_cities = len(total_demand)

  print("Plants: ", num_plants)
  print("Cities: ", num_cities)

  # Variables
  x = {}

  for i in range(num_plants):
    for j in range(num_cities):
      x[i, j] = solver.IntVar(0, total_demand[j], 'x[%i,%i]' % (i, j))

# Constraints

# Sum supplies for each plant should less than the cap of the plant
  for i in range(num_plants):
    solver.Add(solver.Sum([x[i, j] for j in range(num_cities)]) <= total_cap[i])

# Sum supplies for each city should larger than the demand of the city
  for j in range(num_cities):
    solver.Add(solver.Sum([x[i, j] for i in range(num_plants)]) >= total_demand[j])

  solver.Minimize(solver.Sum([(cost1[i][j] + cost2[i][j] + cost3[i][j]) * x[i, j] for i in range(num_plants) for j in range(num_cities)]))

  sol = solver.Solve()

  print('Total cost = ', solver.Objective().Value())
  print()
  for i in range(num_plants):
    for j in range(num_cities):
      if x[i, j].solution_value() >= 0:
        print('P', i+1, ' supply C', j+1, ' ', x[i, j].solution_value())
  print()
  print("Time = ", solver.WallTime(), "milliseconds")


if __name__ == '__main__':
  main()
