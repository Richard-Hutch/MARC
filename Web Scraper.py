from bs4 import BeautifulSoup
import requests
from fractions import Fraction


recipes = [line.rstrip('\n') for line in open('Recipes.txt')]

# cut out blank lines from the file
recipes[:] = [item for item in recipes if item != '']
number_recipes = 0
teaspoons = []
cups = []
total_ingredients = []
temp_string = ''

for t in recipes:

    website = requests.get(recipes[number_recipes])
    page_content = BeautifulSoup(website.text, "html.parser")
    results = page_content.find_all('span', attrs={'class': 'recipe-ingred_txt added'})
    time = page_content.find_all('span', attrs={'class': 'prepTime__item--time'})

    print(time)

    print('WEBSITE: ' + str(recipes[number_recipes]))
    print("INGREDIENTS: ")
    duplicate_check = []

    # i is every ingredient in what every website t is on
    for i in results:

        # groups plural and singular of the same ingredients
        if 'cup ' in i.get_text():
            temp_string = i.get_text()
            temp_string = temp_string.replace('cup ', 'cup(s) ')
            # cups.append(i.get_text())
        elif 'cups' in i.get_text():
            temp_string = i.get_text()
            temp_string = temp_string.replace('cups', 'cup(s) ')

        elif 'teaspoon ' in i.get_text():
            temp_string = i.get_text()
            temp_string = temp_string.replace('teaspoon ', 'teaspoon(s) ')
            # teaspoons.append(i.get_text())

        elif 'teaspoons' in i.get_text():
            temp_string = i.get_text()
            temp_string = temp_string.replace('teaspoons', 'teaspoon(s) ')

        elif 'eggs' in i.get_text():
            temp_string = i.get_text()
            temp_string = temp_string.replace('eggs', 'egg(s) ')
        elif 'egg' in i.get_text():
            temp_string = i.get_text()
            temp_string = temp_string.replace('egg', 'egg(s) ')
        else:
            temp_string = i.get_text()

        # prevents duplicate ingredients from the same website to be added
        # print(i.get_text())
#
        print(temp_string)

        if temp_string not in duplicate_check:
            # print(temp_string)
            total_ingredients.append(temp_string)
            duplicate_check.append(temp_string)
#     # print('CUP(S): ')
#     # print(cups)
#     # print('TEASPOON(S): ')
#     # print(str(teaspoons) + '\n-------------------------------\n-------------------------------\n')
    print('\n-------------------------------\n-------------------------------\n')
#
    number_recipes += 1

# print("TOTAL INGREDIENT LIST: " + str(total_ingredients))
print("Amount of total ingredients " + str(len(total_ingredients)) + '\n')
total_quantity = len(total_ingredients)
final_ing = {}
final_ing2 = {}
final_counter = {}
current_item = 0
quantity_number = 0.0
c_item = ''
# remove quantity and just grab the type of ingredient
while current_item < len(total_ingredients):
    c_item = total_ingredients[current_item]
    c2_item = total_ingredients[current_item]
    quantity_number = c_item
    for characters in '0123456789/':
        # grabs juts the numbers
        if characters in c_item:
            for characters3 in 'abcdefghijklmnopqrstuvwxyz(),-':
                if characters3 in c_item:
                    quantity_number = quantity_number.replace(characters3, '')

        # cuts out numbers and slash
        c_item = c_item.replace(characters, '')
        c2_item = c2_item.replace(characters, '')

        for characters3 in ' ':
            if characters3 in c_item:
                c_item = c_item.replace(characters3, '')
        for characters4 in '/':
            if characters4 in c_item:
                c_item = c_item.replace(characters4, '')

    quantity_number = float(sum(Fraction(s) for s in quantity_number.split()))

    if c_item in final_ing:
        final_ing[c_item] += quantity_number
        final_counter[c_item] += 1

    if c2_item not in final_ing2:
        final_ing[c_item] = quantity_number
        final_counter[c_item] = 1
        final_ing2[c2_item] = 'check'
    # print("ingredient: " + c_item)
    current_item += 1

print('Un-averaged ingredients and quantities: ' + str(final_ing) + '\n')

# divide every key's value by the amount of total of the corresponding ingredient

for element in final_ing:
    hold_int = final_ing[element]
    hold_int2 = final_counter[element]
    final_ing[element] = hold_int / hold_int2


print('Amount of Unique Ingredients: ' + (str(len(final_ing))))
print("FINAL INGREDIENTS AND QUANTITIES " + str(final_ing))
