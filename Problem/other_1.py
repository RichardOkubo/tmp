from configparser import ConfigParser
from functools import reduce
from operator import mul
from random import randrange

import matplotlib.pyplot as plt
import numpy

from deap import tools, base, creator
from deap.algorithms import eaSimple

MAX = 200
DAY = 20

config = ConfigParser(inline_comment_prefixes=";")
config.read("config.ini")
parameters = dict(config["parameters"])
problem = dict(config["problem"])


def apply(proper, session):
    values = session[proper].split()
    values.pop(1)
    return reduce(mul, [float(session[value]) for value in values])


def formatter(proper, session):
    return eval(session[proper])


def compress(key, value):
    return {k : v for k, v in zip(key, value)}


def compress_all(args, parameters=parameters):
    alias = list(parameters.keys())
    alias.remove("products")
    for i, item in enumerate(args):
        exec(f"{alias[i]} = compress(formatter('products', parameters), {item})", globals())


def ratio(x, X, y):
    return (y * X) / x


def resize(target, reference, unity):
    for k in target.keys():
        target[k] = ratio(reference[k], target[k], unity)
    return target


def resize_all(args):
    try:
        for item in args:
            resize(item, measures, 1)
    except Exception as e:
        raise e


def kcal(carbohydrate, protein, fat):
    return carbohydrate * formatter("carbohydrate_factor", problem) + \
           protein * formatter("protein_factor", problem) + \
           fat * formatter("fat_factor", problem)


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


compress_all([
    parameters["costs"],
    parameters["measures"],
    parameters["references"],
    parameters["carbohydrates"],
    parameters["proteins"],
    parameters["fats"]])

resize_all([costs, carbohydrates, proteins, fats])
breakpoint()

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

population = toolbox.population(n=20)
probability_crossover = 1.0
probability_mutation = 0.01
n_generations = 100

statistics = tools.Statistics(key=lambda individuo: individuo.fitness.values)
statistics.register("max", numpy.max)
statistics.register("min", numpy.min)
statistics.register("med", numpy.mean)
statistics.register("std", numpy.std)

population, info = eaSimple(
    population,
    toolbox,
    probability_crossover,
    probability_mutation,
    n_generations,
    statistics)

best_solution = tools.selBest(population, 1)

for individuo in best_solution:
    print(individuo)
    #print(individuo.fitness)

    summation_cost = summation_calories = 0
    for i in range(len(list_product)):
        if individuo[i] > 0:
            summation_cost += cost[i] * individuo[i]
            summation_calories += list_product[i].calories
            print(f"{list_product[i].product} | "
                  f"R${list_product[i].cost} | "
                  f"carbohydrate: {list_product[i].carbohydrate} | "
                  f"protein: {list_product[i].protein} | "
                  f"fat: {list_product[i].fat} | "
                  f"calories: {list_product[i].calories}")
    print(f"Best solution: R${summation_cost} | {summation_calories}kcal")
    
graphic_values = info.select("max")

plt.plot(graphic_values)
plt.show()
