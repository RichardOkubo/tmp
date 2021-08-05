#! C:\Users\Usuário\Desktop\.venv\Scripts\python.exe

from configparser import ConfigParser
from functools import reduce
from operator import mul

from pulp import LpInteger, LpProblem, LpStatus, LpVariable, lpSum, LpMinimize, value

config = ConfigParser(inline_comment_prefixes=";")
config.read("main.ini")
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


def report(model):
    global sum_carbohydrate, sum_protein, sum_fat, sum_kcal, total_cost  # noqa

    objetive = value(model.objective)
    status = model.status

    print(f"Status: {status}, {LpStatus[status]}\n"
          f"Objective: {objetive}\n"
          f"During {formatter('days', problem)} days\n"
          f"Result: {'success' if value(total_cost) <= formatter('expected_cost', problem) else 'failure'}\n")

    for var in model.variables():
        print(f"{var.name}: {var.varValue}")

    print(f"\nKcal: {value(sum_kcal):.2f}:"
          f"\nCarbohydrate: {value(sum_carbohydrate):.2f}"
          f"\nProtein: {value(sum_protein):.2f}"
          f"\nFat: {value(sum_fat):.2f}")


compress_all([
    parameters["costs"],
    parameters["measures"],
    parameters["references"],
    parameters["carbohydrates"],
    parameters["proteins"],
    parameters["fats"]])

resize_all([costs, carbohydrates, proteins, fats])

# Modelo

model = LpProblem(name=problem["problem_name"], sense=LpMinimize)

# Variáveis

decision_vars = LpVariable.dicts(
    name="n",
    indexs=formatter("products", parameters),
    lowBound=0,
    upBound=None,
    cat=LpInteger
)

decision_vars.update({
    "hipercalorico": LpVariable(
        name="n_hipercalorico",
        lowBound=150,
        upBound=150,
        cat=LpInteger)})

# Restrições

## Objetivo

model += lpSum([costs[i] * decision_vars[i] for i in formatter("products", parameters)]), \
    "TotalCostOfProducsPerCan"

## Custo Totoa

daily_cost = lpSum([costs[i] * decision_vars[i] for i in formatter("products", parameters)])

total_cost = daily_cost * formatter('expected_cost', problem)

model += total_cost <= formatter('expected_cost', problem), "TotalCostLimit"

## Carboidrato

sum_carbohydrate = lpSum([
    carbohydrates[i] * decision_vars[i] for i in formatter("products", parameters)])

model += sum_carbohydrate >= apply("carbohydrate_requirement_min", problem), \
    "CarbohydrateRequirementMin"


model += sum_carbohydrate <= apply("carbohydrate_requirement_max", problem), \
    "CarbohydrateRequirementMax"

## Protein

sum_protein = lpSum([proteins[i] * decision_vars[i] for i in formatter("products", parameters)])

model += sum_protein >= apply("protein_requirement_min", problem), \
    "ProteinRequirementMin"

model += sum_protein <= apply("protein_requirement_max", problem), \
    "ProteinRequirementMax"

## Fat

sum_fat = lpSum([fats[i] * decision_vars[i] for i in formatter("products", parameters)])

model += sum_fat >= apply("fat_requirement_min", problem), \
    "FatRequirementMin"

model += sum_fat <= apply("fat_requirement_max", problem), \
    "FatRequirementMax"

## Kcal

sum_kcal = lpSum([
    kcal(carbohydrates[i], proteins[i], fats[i]) * decision_vars[i]
    for i in formatter("products", parameters)])

model += sum_kcal >= formatter("gcm", problem), \
    "CaloriesRequired"

# Solução

model.solve()

# Relatório final
print(model)
report(model)
