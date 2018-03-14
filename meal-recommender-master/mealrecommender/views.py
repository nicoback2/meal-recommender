from django.shortcuts import render
from django import forms
import os
import csv
import math
from openopt import *
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
		bools = ['is_breakfast', 'is_lunch', 'is_snack','is_dinner']
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
			values, breakfast, lunch, dinner, snack = determine_meals(name, height, weight, age, gender, sport, regimen, allergen, dietary_restrictions)

			return render(request, 'mealrecommender/meals.html', {'name': name, 'regimen': regimen, 'values': values, 'breakfast': breakfast, 'lunch': lunch, 'dinner': dinner, 'snack': snack})
	else:
		form = AthleteForm()

	return render(request, 'mealrecommender/athlete_form.html', {'form': form})

def hasAllergy(allergen, food):
	for allergy in allergen:
		if allergy.lower() in food['has_allergen']:
			return True
	return False

def hasRestriction(restrictions, food):
	for restriction in restrictions:
		if restriction.lower() in food['violates_dietary_restriction']:
			return True
	return False

def createMeal(filtered_foods, TDEE, regimen):
	items = filtered_foods
	protein_pct = .30
	carb_pct = .35
	fat_pct = .35
	if regimen == "Competition" or regimen == "Conditioning":
		carb_pct = 0.50
		protein_pct = 0.30
		fat_pct = 0.20
	constraints = lambda values: (values['calories'] < TDEE, values['protein'] < math.floor((TDEE * protein_pct)/4), values['fat'] < math.floor((TDEE * fat_pct)/9), values['carbs'] < math.floor((TDEE * carb_pct)/4))
	objective = 'calories'
	knapsack = KSP(objective, items, goal = 'max', constraints = constraints)
	solution = knapsack.solve('glpk', iprint = 0)
	print(solution)
	return solution.xf
def extractFoods(names, foods):
	meal = []
	for name in names:
		for food in foods:
			if food['name'] == name:
				meal.append(food)
				break
	return meal

def determine_meals(name, height, weight, age, gender, sport, regimen, allergen, dietary_restrictions):
	foods = get_foods()
	filtered_foods_breakfast = []
	filtered_foods_lunch = []
	filtered_foods_dinner = []
	filtered_foods_snack = []
	for food in foods:
		if not hasAllergy(allergen, food) and not hasRestriction(dietary_restrictions, food) and food['is_breakfast']:
			filtered_foods_breakfast.append(food)
		if not hasAllergy(allergen, food) and not hasRestriction(dietary_restrictions, food) and food['is_lunch']:
			filtered_foods_lunch.append(food)
		if not hasAllergy(allergen, food) and not hasRestriction(dietary_restrictions, food) and food['is_dinner']:
			filtered_foods_dinner.append(food)
		if not hasAllergy(allergen, food) and not hasRestriction(dietary_restrictions, food) and food['is_snack']:
			filtered_foods_snack.append(food)
	print(filtered_foods_snack)
	if gender == 'male':
		BMR = (10 * float(weight)) + (6.25 * float(height)) - (5 * float(age)) + 5
	else:
		BMR = (10 * float(weight)) + (6.25 * float(height)) - (5 * float(age)) - 161
	if regimen == 'Off Day':
		activityFactor = 1.2
	elif regimen == 'Recovery':
		activityFactor = 1.55
	elif regimen == 'Conditioning':
		activityFactor = 1.9
	else:
		activityFactor = 1.725
	TDEE = BMR * activityFactor
	breakfast = createMeal(filtered_foods_breakfast, TDEE//4, regimen)
	breakfast = extractFoods(breakfast, foods)
	lunch = createMeal(filtered_foods_lunch, TDEE//4, regimen)
	print(lunch)
	# Do not repeat foods for dinner and lunch
	for food in filtered_foods_dinner:
		if food['name'] in lunch:
			filtered_foods_dinner.remove(food)
	lunch = extractFoods(lunch, foods)
	# print(str(len(filtered_foods_dinner)))
	# print(str(len(filtered_foods_dinner)))
	dinner = createMeal(filtered_foods_dinner, TDEE//4, regimen)
	dinner = extractFoods(dinner, foods)
	print(filtered_foods_snack)
	snack = createMeal(filtered_foods_snack, TDEE//4, regimen)
	snack = extractFoods(snack, foods)
	protein_pct = .30
	carb_pct = .35
	fat_pct = .35
	if regimen == "Competition" or regimen == "Conditioning":
		carb_pct = 0.50
		protein_pct = 0.30
		fat_pct = 0.20
	values = {}
	values['calories'] = round(TDEE)
	values['protein'] = round(TDEE / 4 * protein_pct)
	values['carbs'] = round(TDEE / 4 * carb_pct)
	values['fat'] = round(TDEE / 9 * fat_pct)

	#NOTE: allergens and dietary restrictions are all lower case in the foods list, but capitalized in the form data.
	return (values, breakfast, lunch, dinner, snack)
