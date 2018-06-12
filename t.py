from __future__ import print_function
from ortools.linear_solver import pywraplp


def main():
  # Instantiate a mixed-integer solver
  solver = pywraplp.Solver('SolveTransportationProblem',
                           pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)
  cost = [[90, 76, 75, 70, 50, 74, 12, 68],
          [35, 85, 55, 65, 48, 101, 70, 83],
          [125, 95, 90, 105, 59, 120, 36, 73],
          [45, 110, 95, 115, 104, 83, 37, 71],
          [60, 105, 80, 75, 59, 62, 93, 88]]

  task_sizes = [10, 7, 3, 12, 15, 4, 11, 5]

  # Maximum total of task sizes for any worker
  total_size_max = 15
  num_plants = len(cost)
  num_cities = len(cost[1])

  print("Plants: ", num_plants)
  print("Cities: ", num_cities)

  # Variables
  x = {}

  for i in range(num_plants):
    for j in range(num_cities):
      x[i, j] = solver.IntVar(0, 2, 'x[%i,%i]' % (i, j))

  # Constraints

  # The total size of the tasks each worker takes on is at most total_size_max.

  for i in range(num_plants):
    solver.Add(solver.Sum([task_sizes[j] * x[i, j] for j in range(num_cities)]) <= total_size_max)

  # Each task is assigned to at least one worker.

  for j in range(num_cities):
    solver.Add(solver.Sum([x[i, j] for i in range(num_plants)]) >= 1)

  solver.Minimize(solver.Sum([cost[i][j] * x[i, j] for i in range(num_plants)
                              for j in range(num_cities)]))
  sol = solver.Solve()

  print('Total cost = ', solver.Objective().Value())
  print()
  for i in range(num_plants):
    for j in range(num_cities):
      if x[i, j].solution_value() > 0:
        print('Worker', i, ' assigned to task', j, '  Cost = ', cost[i][j])
  print()
  print("Time = ", solver.WallTime(), "milliseconds")


if __name__ == '__main__':
  main()
