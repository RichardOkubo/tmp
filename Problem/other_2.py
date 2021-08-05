from configparser import ConfigParser
from random import randrange

import numpy

from deap import tools, base, creator
from deap.algorithms import eaSimple

MAX = 200
DAY = 20

config = ConfigParser(inline_comment_prefixes=";")
config.read("config.ini")
parameters = dict(config["parameters"])
problem = dict(config["problem"])


def compress(key, value):
    return {k : v for k, v in zip(key, value)}


def compress_all(args, parameters=parameters):
    alias = list(parameters.keys())
    alias.remove("products")
    for i, item in enumerate(args):
        exec(f"{alias[i]} = compress(formatter('products', parameters), {item})", globals())


def formatter(proper, session):
    return eval(session[proper])


def ratio(x, X, y):
    return (y * X) / x


def resize(target, references, unity):
    for i, k in enumerate(target.keys()):
        target[k] = ratio(references[k], target[k], unity[i])
    return target


def resize_all(args, individual):
    for item in args:
        resize(item, references, individual)


def heuristic(individual):
    resize_all([carbohydrates, proteins, fats], individual)
    # [fats[k] * individual[i] for i, k in enumerate(formatter("products", parameters))]


compress_all([
    parameters["costs"],
    parameters["measures"],
    parameters["references"],
    parameters["carbohydrates"],
    parameters["proteins"],
    parameters["fats"]])

# toolbox = base.Toolbox()

# creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
# creator.create("Individual", list, fitness=creator.FitnessMin)

# toolbox.register("attr_int", randrange, 0, MAX+1, 10)
# toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_int, n=len(costs.keys()))
# toolbox.register("population", tools.initRepeat, list, toolbox.individual)
# toolbox.register("evaluate", heuristic)
# toolbox.register("mate", tools.cxOnePoint)
# toolbox.register("mutate", tools.mutFlipBit, indpb=0.01)
# toolbox.register("select", tools.selRoulette)

# population = toolbox.population(n=20)
# probability_crossover = 1.0
# probability_mutation = 0.01
# n_generations = 100

# statistics = tools.Statistics(key=lambda individuo: individuo.fitness.values)
# statistics.register("max", numpy.max)
# statistics.register("min", numpy.min)
# statistics.register("med", numpy.mean)
# statistics.register("std", numpy.std)

# population, info = eaSimple(
#     population,
#     toolbox,
#     probability_crossover,
#     probability_mutation,
#     n_generations,
#     statistics)

# best_solution = tools.selBest(population, 1)
