import csv

# converts food csv into a list of dicts, each dict representing a single food item
# the id of a food item corresponds to its index in the list. the id is also located in the 'id' field of the dict
# the fields of each food item are:

# id: int
# name: string
# calories: int
# carbs: float
# protein: float
# fat: float
# is_breakfast: bool (i.e. can this food item be included in a breakfast meal?)
# is_lunch: bool
# is_dinner: bool
# has_allergen: list of strings where each element is one of: gluten, egg, fish, milk, soy, wheat, peanuts, tree nuts, sesame, shellfish
# violates_dietary_restriction: list of strings, where each element is one of: vegetarian, vegan
def main():

    f = open('food.csv', 'r')

    with f:

        reader = csv.DictReader(f)
        foods = list(reader)
        bools = ['is_breakfast', 'is_lunch', 'is_dinner']
        for i, el in enumerate(foods):
            el['has_allergen'] = (el['has_allergen']).split("@")
            if len(el['has_allergen']) == 1 and el['has_allergen'][0] == '':
                el['has_allergen'] = []
            el['violates_dietary_restriction'] = (el['violates_dietary_restriction']).split()
            el['id'] = i
            el['calories'] = int(el['calories'])
            el['protein'] = float(el['protein'])
            el['carbs'] = float(el['carbs'])
            el['fat'] = float(el['fat'])
            for b in bools:
                if el[b] == 'TRUE':
                    el[b] = True
                else:
                    el[b] = False


if __name__ == "__main__":
    main()
