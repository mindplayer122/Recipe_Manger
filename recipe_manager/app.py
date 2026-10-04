import streamlit as st
from recipe_manager import Recipe, load_recipes, save_recipes

st.title("Recipe Manager")

recipes = load_recipes()


# add recipe

st.header("Add Recipe")

title = st.text_input("Recipe title")

Ingredients = st.text_area(
    "Ingredients",
    placeholder="Enter each ingredient separated by a comma"
)

instructions = st.text_area("Instructions")

if st.button("Add Recipe"):
    if title and Ingredients and instructions:
        Ingredient_list = [i.strip() for i in Ingredients.split(",")]

        recipe = Recipe(
            title,
            Ingredient_list,
            instructions
        )

        recipes.append(recipe)
        save_recipes(recipes)

        st.success(f"Recipe '{title}' added!")
        st.rerun()
    else:
        st.warning("Please fill in all fields.")

#view recipes

st.header("Recipes")

if not recipes:
    st.write("No recipes found.")
else:
    for recipe in recipes:
        with st.expander(recipe.title):
            st.write("**Ingredients**")

            for ingredient in recipe.ingredients:
                st.write(f"- {ingredient}")

            st.write("**Instructions**")
            st.write(recipe.instructions)
#search recipes

st.header("search Recipes")

search = st.text_input("Searchby title or ingredient")

if search: 
    search = search.lower()

    results = [
        recipe for recipe in recipes
        if search in recipe.title.lower()
        or any(search in ingredient.lower()
               for ingredient in recipe.ingredients)
    ]

    if results:
        for recipe in results:
            st.write(f"**{recipe.title}**")
    else:
        st.write("No matching recipes found.")

#Delete recipe

st.header("Delete Recipe")

if recipes:

    recipe_titles = [recipe.title for recipe in recipes]

    selected_recipe = st.selectbox(
        "choose a recipe to delete",
        recipe_titles
    )

    if st.button ("Delete Recipe"):
        recipes = [
            recipe for recipe in recipes
            if recipe.title != selected_recipe
        ]

        save_recipes(recipes)

        st.success(f"'{selected_recipe}' deleted!")
        st.rerun()
