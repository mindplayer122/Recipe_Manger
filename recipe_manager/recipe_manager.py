import json
import os

DATA_FILE = "data/recipes.json"


class Recipe:
    def __init__(self, title, ingredients, instructions):
        self.title = title
        self.ingredients = ingredients
        self.instructions = instructions

    # convert object to dictionary for JSON
    def to_dict(self):
        return {
            "title": self.title,
            "ingredients": self.ingredients,
            "instructions": self.instructions
        }

    #rebuilds object from dictionary
    @staticmethod
    def from_dict(data):
        return Recipe(data["title"], data["ingredients"], data["instructions"])
    

#load recipes from JSON file
def load_recipes():
    if not os.path.exists(DATA_FILE):
        return []
    #allow the code to read the JSON file with r
    with open(DATA_FILE, "r") as file:
        data = json.load(file)
        return [Recipe.from_dict(d) for d in data]

#saves recipes to JSON file
def save_recipes(recipes):
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    #allow the code to write the JSON file with w
    with open(DATA_FILE, "w") as file:
        json.dump([r.to_dict() for r in recipes], file, indent=4)

#add a new recipe
def add_recipe(recipes):
    title = input("Recipe title: ").strip()
    ingredients = input("ingredients (comma seperated): ").split(",")
    instructions = input("instructions: ").strip()
    recipe = Recipe(title, [i.strip() for i in ingredients], instructions)
    recipes.append(recipe)
    save_recipes(recipes)
    print(f"Recipe '{title}' added!\n")



#view all recipes
def view_recipes(recipes):
    if not recipes:
        print("No recipes found.\n")
        return
    for i, r in enumerate(recipes, 1):
        print(f"{i}. {r.title}")
    print()


#search by title or ingredient
def search_recipes(recipes):
    keyword = input("Enter title or ingredient to search: ").lower()
    results = [r for r in recipes if keyword in r.title.lower()
               or any(keyword in ing.lower() for ing in r.ingredients)]
    if not results:
        print("No matching recipes found.\n")
        return
    for r in results:
        print(f"- {r.title}")
    print()


def edit_recipe(recipes):
    view_recipes(recipes)
    index = int(input("enter a number of the recipe to edit: ")) - 1
    if 0 <= index < len(recipes):
        r = recipes[index]
        new_title = input(f"New title ({r.title}): ").strip()
        new_ingredients = input(f"New ingredients (comma seperated) ({', '.join(r.ingredients)}): ").strip()
        new_instructions = input(f"New instructions ({r.instructions}): ").strip()

        if new_title: r.title = new_title
        if new_ingredients: r.ingredients = [i.strip() for i in new_ingredients.split(",")]
        if new_instructions: r.instructions = new_instructions

        save_recipes(recipes)
        print("Recipe updated!\n")

    else:
        print("Invalid selection.\n")


def delete_recipe(recipes):
    view_recipes(recipes)
    index = int(input("enter a number of the recipe to delete: ")) - 1
    if 0 <= index < len(recipes):
        deleted = recipes.pop(index)
        save_recipes(recipes)
        print(f"Recipe '{deleted.title}' deleted!\n")
    else:
        print("Invalid selection.\n")

def main(): 
    recipes = load_recipes()

    while True:

        print("=== Recipe Manager ===")
        print("1. Add Recipe")
        print("2. View Recipe")
        print("3. Search Recipe")
        print("4. Edit Recipe")
        print("5. Delete Recipe")
        print("6. Exit")

        choice = input("choose an option: ").strip()

        if choice == "1":
            add_recipe(recipes)
        elif choice == "2":
            view_recipes(recipes)
        elif choice == "3":
            search_recipes(recipes)
        elif choice == "4":
            edit_recipe(recipes)
        elif choice == "5":
            delete_recipe(recipes)
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again\n")
        
if __name__ == "__main__":
    main()