class Product:
    def __init__(self, product, cost, measure, reference, carbohydrate, protein, fat):
        self.product = product
        self.cost = cost
        self.measure = measure
        self.reference = reference
        self.carbohydrate = carbohydrate
        self.protein = protein
        self.fat = fat
    
    @property
    def calories(self):
        return 4*self.carbohydrate + 4*self.protein + 9*self.fat

    def __repr__(self):
        return f'(product="{self.product}" ' \
               f"cost={self.cost} " \
               f"measure={self.measure} " \
               f"reference={self.reference} " \
               f"carbohydrate={self.carbohydrate} " \
               f"protein={self.protein} " \
               f"fat={self.fat})"
