from pprint import pprint
from random import randrange

import numpy
import matplotlib.pyplot as plt

from deap import tools, base, creator
from deap.algorithms import eaSimple

WEIGHT = 60
MAX = 201
DAY = 20


class Product:
    def __init__(self, category, cost, measure, reference, carbohydrate, protein, fat):
        self.category = category
        self.cost = cost
        self.measure = measure
        self.reference = reference
        self._carbohydrate = carbohydrate
        self._protein = protein
        self._fat = fat
        self.carbohydrate = carbohydrate
        self.protein = protein
        self.fat = fat
        
    @property
    def calories(self):
        return 4*self.carbohydrate + 4*self.protein + 9*self.fat
    
    def redefine(self, reference):
        self.carbohydrate = (self._carbohydrate * reference) / self.reference
        self.protein = (self._protein * reference) / self.reference
        self.fat = (self._fat * reference) / self.reference

    def __repr__(self):
        return f'<category="{self.category}" ' \
               f"cost={self.cost} " \
               f"measure={self.measure} " \
               f"reference={self.reference} " \
               f"carbohydrate={self.carbohydrate} " \
               f"protein={self.protein} " \
               f"fat={self.fat}>"


def cost(i, individual):
        factor = 1
        cost_i = products[i].cost

        while (factor * products[i].measure) // individual <= DAY:
            factor += 1
            cost_i = factor * products[i].cost

        return (cost_i, factor,)


def heuristic(individuals):
    score = 0

    for i, individual in enumerate(individuals):
        if individual == 0:
            continue
        cost_i, _ = cost(i, individual)
        score += cost_i
            
    return (score / 100000,)


options = {
    "categories": [
        "hipercalorico",
        "leite_em_po",
        "amido_de_milho",
        "amendoim",
        "macarrao",
        "frango",
        "arroz"
    ],
    "costs": [
        89.90,
        11.99,
        3.99,
        8.99,
        4.99,
        13.99,
        19.98
    ],
    "measures": [
        3000,
        400,
        200,
        500,
        1000,
        1000,
        5000
    ],
    "references": [
        160.,
        26.,
        20.,
        15.,
        80.,
        100.,
        50.
    ],
    "carbohydrates": [
        128.,
        9.6,
        17.,
        3.,
        60.,
        0.,
        39.],
    "proteins": [
        15.,
        6.7,
        0.,
        4.,
        9.2,
        23,
        3.6
    ],
    "fats": [
        2.3,
        7.1,
        0.,
        6.6,
        .5,
        1.,
        0.
    ],
}

products = [
    Product(*product) for product in list(
        zip(*[options[k] for k in options.keys()]))]

toolbox = base.Toolbox()

creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)

toolbox.register("attr_int", randrange, 0, MAX, 10)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_int, n=len(options["categories"]))
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

best_solution = tools.selBest(population, 1)[0]

if __name__ == "__main__":

    best_cost = 0
    factors = []
    costs = []

    for i,_ in enumerate(products):
        if best_solution[i] == 0:
            continue
        aux_cost, aux_factor = cost(i, best_solution[i])
        factors.append(aux_factor)
        costs.append(aux_cost)
        best_cost += aux_cost

    pprint({
        "products": options['categories'],
        "unities": factors,
        "quantities": best_solution,
        "costs": best_cost,
        "score": f"R${best_cost}",
    })

    # plt.plot(info.select("max"))
    # plt.plot(info.select("min"))
    # plt.show()
