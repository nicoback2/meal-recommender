from django.shortcuts import render
from django import forms
import os
import csv
# Create your views here.

class AthleteForm(forms.Form):
	name = forms.CharField(max_length = 30)
	height = forms.DecimalField(label = "Height (inches)", max_digits=5, decimal_places=1)
	weight = forms.DecimalField(label = "Weight (lbs.)", max_digits=5, decimal_places=1)
	age = forms.IntegerField()
	# Gender
	FEMALE = 'F'
	MALE = 'M'
	GENDER_OPTIONS = (
		(FEMALE, 'Female'),
		(MALE, 'Male')
		)
	gender = forms.ChoiceField(choices = GENDER_OPTIONS, widget=forms.Select())

	SWIMMING = 'Swimming'

	SPORT_OPTIONS = (
		(SWIMMING, 'Swimming'),
		)

	sport = forms.ChoiceField(choices = SPORT_OPTIONS, widget = forms.Select())


    # Regimen type
	OFFDAY = 'Off Day'
	RECOVERY = 'Recovery'
	COMPETITION = 'Competition'
	CONDITIONING = 'Conditioning'

	REGIMEN_TYPES = (
		(OFFDAY, 'Off Day'),
		(RECOVERY, 'Recovery'),
		(COMPETITION, 'Competition'),
		(CONDITIONING, 'Conditioning'),
		)

	regimen = forms.ChoiceField(choices = REGIMEN_TYPES, widget=forms.Select())

	# Allergens
	NONE = 'None'
	SOY = 'Soy'
	MILK = 'Milk'
	TREENUTS = 'Tree Nuts'
	PEANUTS = 'Peanuts'
	FISH = 'Fish'
	SHELLFISH = 'Shellfish'
	GLUTEN = 'Gluten'
	WHEAT = 'Wheat'
	SESAME = 'Sesame'
	EGG = 'Egg'

	ALLERGEN_OPTIONS = (
		(NONE, 'None'),
		(SOY, 'Soy'),
		(MILK, 'Milk'),
		(TREENUTS, 'Tree Nuts'),
		(PEANUTS, 'Peanuts'),
		(FISH, 'Fish'),
		(SHELLFISH, 'Shellfish'),
		(GLUTEN, 'Gluten'),
		(WHEAT, 'Wheat'),
		(SESAME, 'Sesame'),
		(EGG, 'Egg'),
		)

	VEGETARIAN = 'Vegetarian'
	VEGAN = 'Vegan'

	DIETARY_RESTRICTION_OPTIONS = (
		(NONE, 'None'),
		(VEGETARIAN, 'Vegetarian'),
		(VEGAN, 'Vegan'),
		)

	allergens = forms.MultipleChoiceField(choices = ALLERGEN_OPTIONS, widget = forms.CheckboxSelectMultiple())
	dietary_restrictions = forms.MultipleChoiceField(choices = DIETARY_RESTRICTION_OPTIONS, widget = forms.CheckboxSelectMultiple())

def get_foods():
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
    f = open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'mealrecommender/food.csv'), 'r')

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
        return foods

def get_meal_plan(request):
	# If the form has been submitted
	if request.method == 'POST':
		# A form bound to the POST data that has fields for user name and user password
		form = AthleteForm(request.POST)
		# All validation rules pass
		if form.is_valid():
			name = form.cleaned_data['name']
			height = form.cleaned_data['height']
			weight = form.cleaned_data['weight']
			age = form.cleaned_data['age']
			gender = form.cleaned_data['gender']
			sport = form.cleaned_data['sport']
			regimen = form.cleaned_data['regimen']
			allergen = form.cleaned_data['allergens']
			dietary_restrictions = form.cleaned_data['dietary_restrictions']

			# determine meals
			meals = determine_meals(name, height, weight, age, gender, sport, regimen, allergen)


			return render(request, 'mealrecommender/meals.html', {'name': name, 'regimen': regimen, 'meals': meals})
	else:
		form = AthleteForm()

	return render(request, 'mealrecommender/athlete_form.html', {'form': form})

def determine_meals(name, height, weight, age, gender, sport, regimen, allergen):
    foods = get_foods()
    #NOTE: allergens and dietary restrictions are all lower case in the foods list, but capitalized in the form data.
    return ['egg', 'salad', 'chicken']
