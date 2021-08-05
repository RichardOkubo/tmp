from configparser import ConfigParser

from model import Product

config = ConfigParser(inline_comment_prefixes=";")
config.read("config.ini")
parameters = dict(config["parameters"])

product, cost, measure, reference, carbohydrate, protein, fat = [
    eval(parameters[parameter]) for parameter in parameters.keys()]

list_product = [
    Product(*product) for product in [
        list(register) for register in zip(*[
            product, cost, measure, reference, carbohydrate, protein, fat])]]
