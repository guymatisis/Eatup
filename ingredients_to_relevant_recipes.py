import pandas as pd
from fuzzywuzzy import process
import heapq


def ingredients_to_recipe(fridge_items):
	#--------------  SET UP DATABASE  --------------
	#read csv, and split on ";" the line
	df = pd.read_csv('clean_recipes.csv',error_bad_lines=False,sep = ';')
	#clean up data from non-ascii characters
	df.Ingredients.replace({r'[^\x00-\x7F]+':''}, regex=True, inplace=True)
	#Select ingredients column

	#--------------  SET UP INGREDIENTS LIST  --------------
	Ingredients = (df.loc[:,'Ingredients'])
	# Take column 'Ingredients', split it up by ','
	# and put into a dataframe where each ingredient is in a column
	list_of_ingredients =[]
	for recipe in Ingredients:
		result = [x.strip() for x in recipe.split(',')]
		list_of_ingredients.append(result)



	# --------------------COMPARE FRIDGE ITEMS TO RECIPE INGREDIENTS  --------------------
	score_list =[]
	#--------------------ITERATE THROUGH RECIPES--------------------
	for recipe_ingredients in list_of_ingredients:
		matches =0 
		# ITERATE THROUGH FRIDGE ITEMS AND COMPARE THEM TO RECIPE ITEMS
		for fridge_item in fridge_items:
			highest = process.extractOne(fridge_item,recipe_ingredients) #FUZZYWUZZY!! RETURNS ONLY HIGHEST MATCH... NO DUPLICATES
			if(highest[1]>85): #IF RESULTING MATCH IS ABOVE 90 THEN KEEP. (90 IS ARBITRARY...)
				matches = matches +1
		#Number of missing items
		missing_items =len(recipe_ingredients) - matches
		#calculate score. self explanitory.
		score = matches - missing_items
		if matches != 0 :
			score_list.append(score) 
	#--------------------FIND RECIPES WITH BEST SCORES --------------------
	relevant_recipe_indexes = heapq.nlargest(5, range(len(score_list)),score_list.__getitem__) 


	#-------------------- OUTPUT --------------------
	return (df.ix[relevant_recipe_indexes, [u'Recipe Name', u'Directions',u'Recipe Photo']].values.tolist())