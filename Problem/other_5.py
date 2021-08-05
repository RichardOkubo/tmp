from configparser import ConfigParser
from functools import reduce
from operator import mul
from random import randrange

from deap import base, creator, tools

from handling import product, cost, reference, measure, carbohydrate, protein, fat, list_product

config = ConfigParser(inline_comment_prefixes=";")
config.read("config.ini")
problem = dict(config["problem"])

MAX = 200
DAY = 20


def apply(proper, session):
    values = session[proper].split()
    values.pop(1)
    return reduce(mul, [float(session[value]) for value in values])


def ratio(x, X, y):
    return (y * X) / x


def score_function(cost_i, measure_i, individual_i):
    factor = 1
    cost_total = cost_i

    while ((measure_i * factor) // individual_i) < DAY:
        factor += 1
        cost_total = factor * cost_i

    return cost_total


def heuristic(individual):
    score = sum_carbohydrate = sum_protein = sum_fat = sum_calories = 0

    for i in range(len(individual)):
       if individual[i] > 0:
           score += score_function(cost[i], measure[i], individual[i])
           sum_carbohydrate += ratio(reference[i], carbohydrate[i], individual[i])
           sum_protein += ratio(reference[i], protein[i], individual[i])
           sum_fat += ratio(reference[i], fat[i], individual[i])
           sum_calories += ratio(reference[i], list_product[i].calories, individual[i])

    if (apply("carbohydrate_requirement_min", problem) < sum_carbohydrate < apply("carbohydrate_requirement_max", problem)) and \
       (apply("protein_requirement_min", problem) < sum_protein < apply("protein_requirement_max", problem)) and \
       (apply("fat_requirement_min", problem) < sum_fat < apply("fat_requirement_max", problem)) and \
       (eval(problem["gcm"]) < sum_calories):
        score = 1

    return score / 100000,


toolbox = base.Toolbox()

creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)

toolbox.register("attr_int", randrange, 0, MAX+1, 10)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_int, n=len(product))
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("evaluate", heuristic)
toolbox.register("mate", tools.cxOnePoint)
toolbox.register("mutate", tools.mutFlipBit, indpb=0.01)
toolbox.register("select", tools.selRoulette)
