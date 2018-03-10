from django.shortcuts import render
from django import forms

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
	DAIRY = 'Dairy'
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
		(DAIRY, 'Dairy'),
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
			regimen = form.cleaned_data['regimen']
			allergen = form.cleaned_data['allergens']
			dietary_restrictions = form.cleaned_data['dietary_restrictions']
			return render(request, 'mealrecommender/meals.html', {'name': name, 'regimen': regimen})
	else:
		form = AthleteForm()

	return render(request, 'mealrecommender/athlete_form.html', {'form': form})



