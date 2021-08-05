from itertools import count
from pprint import pprint


def proporcao(x, X, y):
    # x -- X
    # y -- ?   
    return (y * X) / x


def redimensionar(key, de, para):
    c = count()
    for macro in dieta[key]:
        dieta[key][next(c)] = proporcao(de, macro, para)


def kcal(carboidrato, proteina, gordura):
    return carboidrato*4 + proteina*4 + gordura*9


def total(macro):
    return {
        "carboidratos": sum(dieta[k][0] for k in dieta.keys()),
        "proteinas": sum(dieta[k][1] for k in dieta.keys()),
        "gorduras": sum(dieta[k][2] for k in dieta.keys())
    }.get(macro)


## Durante +/- 28 dias

dieta = {
    "hipercalorico": [128., 15., 2.3],  # R$75.00-80.00 [Ref: 160g de 3Kg] (1 unidade) 20 dias
    "leite_em_po": [9.6, 6.7, 7.1],     # R$11.99 [Ref: 26g de 400g] (3 unidade) 28 dias
    "amido_de_milho": [17., 0., 0.],    # R$3.99 [Ref: 20g de 200g] (4 unidade) 28 dias
    "amendoim": [3., 4., 6.6],          # R$8.99 [Ref: 15g de 500g] (2 unidade) 28 a 29 dias
    "macarrao": [60., 9.2, .5],         # R$4.99 [Ref: 80g de 1kg] (3 unidade) 30 dias
    #"frango": [0., 23, 1.],             # R$13.99 [Ref: 100g de 1kg] (3 unidade) 30 dias
    #"acai": [4., 1., 7.],               # R$10.00 [Ref: 100g de 1kg] (3 unidade) 30 dias
    "arroz": [39., 3.6, 0.],
}

registros = (
    ("hipercalorico", 160, 150),
    ("leite_em_po", 26, 25),
    ("amido_de_milho", 20, 28),
    ("amendoim", 15, 20),
    ("macarrao", 80, 100),
    #("frango", 100, 100),
    #("acai", 100, 100),
    ("arroz", 50, 100),
)

custo = sum([
    75. * 1,
    11.99 * 3,
    3.99 * 4,
    8.99 * 2,
    4.99 * 3,
    #13.99 * 3,
    #10. * 3,
    19.98 * 1,
])

for registro in registros:
    redimensionar(*registro)

dias_com_hipercalorico = sum(kcal(*dieta[k]) for k in dieta.keys())
#dias_sem_hipercalorico = sum(kcal(*dieta[k]) for k in dieta.keys() if k != "hipercalorico")

pprint(list(dieta.keys()))

print(f"\nTotal de Kcal: {dias_com_hipercalorico:.0f} kcal")
#print(f"Sem hipercalórico: {dias_sem_hipercalorico:.0f} kcal")

print(f"Carboidratos: {total('carboidratos'):.0f}g\n"
      f"Proteínas: {total('proteinas'):.0f}g\n"
      f"Gorduras: {total('gorduras'):.0f}g")

print(f"Custo total: {custo}\n"
      f"Custo acumulado: {custo + sum([8.98, 7.99, 3.98, 2.])}")
                                    # Café, óleo, adoçante e sal
