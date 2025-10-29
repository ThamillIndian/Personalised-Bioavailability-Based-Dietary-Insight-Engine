"""
Seed Recipe Database
30 diverse recipes across different cuisines and dietary preferences
"""

from app.models.recipe import Recipe, Ingredient, RecipeInstruction, NutritionInfo
from uuid import uuid4

SEED_RECIPES = [
    # Recipe 1: Classic Spaghetti Carbonara
    Recipe(
        id=uuid4(),
        title="Classic Spaghetti Carbonara",
        description="Authentic Italian pasta with creamy egg sauce and crispy pancetta",
        cuisine_type="Italian",
        difficulty="medium",
        prep_time=10,
        cook_time=20,
        servings=4,
        image_url="https://images.unsplash.com/photo-1588013273468-315fd88ea51c",
        ingredients=[
            Ingredient(name="spaghetti", quantity=400, unit="g", is_critical=True, category="grain"),
            Ingredient(name="eggs", quantity=4, unit="whole", is_critical=True, category="protein"),
            Ingredient(name="pancetta", quantity=200, unit="g", is_critical=True, category="protein"),
            Ingredient(name="parmesan cheese", quantity=100, unit="g", category="dairy"),
            Ingredient(name="black pepper", quantity=1, unit="tsp", category="spice"),
            Ingredient(name="salt", quantity=1, unit="tsp", category="spice"),
        ],
        instructions=[
            RecipeInstruction(step_number=1, instruction="Cook spaghetti in salted boiling water until al dente"),
            RecipeInstruction(step_number=2, instruction="Fry pancetta until crispy in a large pan"),
            RecipeInstruction(step_number=3, instruction="Beat eggs with grated parmesan and black pepper"),
            RecipeInstruction(step_number=4, instruction="Drain pasta and add to pancetta pan, remove from heat"),
            RecipeInstruction(step_number=5, instruction="Quickly mix in egg mixture, tossing continuously until creamy"),
        ],
        dietary_tags=[],
        nutrition=NutritionInfo(calories=520, protein=22, carbs=58, fat=21, fiber=3, sodium=850)
    ),
    
    # Recipe 2: Chicken Tikka Masala
    Recipe(
        id=uuid4(),
        title="Chicken Tikka Masala",
        description="Creamy Indian curry with tender chicken in spiced tomato sauce",
        cuisine_type="Indian",
        difficulty="medium",
        prep_time=30,
        cook_time=40,
        servings=6,
        image_url="https://images.unsplash.com/photo-1565557623262-b51c2513a641",
        ingredients=[
            Ingredient(name="chicken breast", quantity=800, unit="g", is_critical=True, category="protein"),
            Ingredient(name="yogurt", quantity=200, unit="ml", category="dairy"),
            Ingredient(name="onion", quantity=2, unit="whole", category="vegetable"),
            Ingredient(name="tomato", quantity=400, unit="g", category="vegetable"),
            Ingredient(name="cream", quantity=200, unit="ml", category="dairy"),
            Ingredient(name="garam masala", quantity=2, unit="tbsp", category="spice"),
            Ingredient(name="ginger", quantity=2, unit="tbsp", category="spice"),
            Ingredient(name="garlic", quantity=4, unit="cloves", category="spice"),
        ],
        instructions=[
            RecipeInstruction(step_number=1, instruction="Marinate chicken in yogurt and spices for 30 minutes"),
            RecipeInstruction(step_number=2, instruction="Grill or bake marinated chicken until cooked"),
            RecipeInstruction(step_number=3, instruction="Sauté onions, ginger, and garlic until fragrant"),
            RecipeInstruction(step_number=4, instruction="Add tomatoes and spices, simmer for 15 minutes"),
            RecipeInstruction(step_number=5, instruction="Add cream and grilled chicken, cook for 10 more minutes"),
        ],
        dietary_tags=["gluten-free"],
        nutrition=NutritionInfo(calories=380, protein=35, carbs=18, fat=20, fiber=3, sodium=620)
    ),
    
    # Recipe 3: Vegetarian Buddha Bowl
    Recipe(
        id=uuid4(),
        title="Vegetarian Buddha Bowl",
        description="Nutritious bowl with quinoa, roasted vegetables, and tahini dressing",
        cuisine_type="Mediterranean",
        difficulty="easy",
        prep_time=15,
        cook_time=30,
        servings=4,
        image_url="https://images.unsplash.com/photo-1546069901-ba9599a7e63c",
        ingredients=[
            Ingredient(name="quinoa", quantity=200, unit="g", is_critical=True, category="grain"),
            Ingredient(name="chickpeas", quantity=400, unit="g", category="protein"),
            Ingredient(name="sweet potato", quantity=2, unit="whole", category="vegetable"),
            Ingredient(name="kale", quantity=200, unit="g", category="vegetable"),
            Ingredient(name="avocado", quantity=1, unit="whole", category="vegetable"),
            Ingredient(name="tahini", quantity=3, unit="tbsp", category="other"),
            Ingredient(name="lemon juice", quantity=2, unit="tbsp", category="other"),
        ],
        instructions=[
            RecipeInstruction(step_number=1, instruction="Cook quinoa according to package instructions"),
            RecipeInstruction(step_number=2, instruction="Roast sweet potato and chickpeas at 200°C for 25 minutes"),
            RecipeInstruction(step_number=3, instruction="Massage kale with a bit of olive oil and salt"),
            RecipeInstruction(step_number=4, instruction="Make tahini dressing with lemon juice and water"),
            RecipeInstruction(step_number=5, instruction="Assemble bowl with quinoa, vegetables, and dressing"),
        ],
        dietary_tags=["vegetarian", "vegan", "gluten-free"],
        nutrition=NutritionInfo(calories=420, protein=15, carbs=55, fat=18, fiber=12, sodium=320)
    ),
    
    # Recipe 4: Beef Tacos
    Recipe(
        id=uuid4(),
        title="Beef Tacos",
        description="Mexican-style tacos with seasoned ground beef and fresh toppings",
        cuisine_type="Mexican",
        difficulty="easy",
        prep_time=10,
        cook_time=15,
        servings=4,
        image_url="https://images.unsplash.com/photo-1551504734-5ee1c4a1479b",
        ingredients=[
            Ingredient(name="ground beef", quantity=500, unit="g", is_critical=True, category="protein"),
            Ingredient(name="taco shells", quantity=8, unit="whole", is_critical=True, category="grain"),
            Ingredient(name="lettuce", quantity=1, unit="head", category="vegetable"),
            Ingredient(name="tomato", quantity=2, unit="whole", category="vegetable"),
            Ingredient(name="cheese", quantity=150, unit="g", category="dairy"),
            Ingredient(name="sour cream", quantity=100, unit="ml", category="dairy"),
            Ingredient(name="taco seasoning", quantity=2, unit="tbsp", category="spice"),
        ],
        instructions=[
            RecipeInstruction(step_number=1, instruction="Brown ground beef in a large skillet"),
            RecipeInstruction(step_number=2, instruction="Add taco seasoning and water, simmer for 5 minutes"),
            RecipeInstruction(step_number=3, instruction="Warm taco shells in oven"),
            RecipeInstruction(step_number=4, instruction="Chop lettuce and tomatoes"),
            RecipeInstruction(step_number=5, instruction="Fill shells with beef and top with vegetables and cheese"),
        ],
        dietary_tags=[],
        nutrition=NutritionInfo(calories=450, protein=28, carbs=35, fat=22, fiber=4, sodium=780)
    ),
    
    # Recipe 5: Salmon Teriyaki
    Recipe(
        id=uuid4(),
        title="Salmon Teriyaki",
        description="Glazed salmon with sweet and savory Japanese teriyaki sauce",
        cuisine_type="Japanese",
        difficulty="easy",
        prep_time=10,
        cook_time=15,
        servings=4,
        image_url="https://images.unsplash.com/photo-1580959375944-58b0b5e1e8ed",
        ingredients=[
            Ingredient(name="salmon fillets", quantity=4, unit="pieces", is_critical=True, category="protein"),
            Ingredient(name="soy sauce", quantity=60, unit="ml", category="other"),
            Ingredient(name="honey", quantity=3, unit="tbsp", category="other"),
            Ingredient(name="ginger", quantity=1, unit="tbsp", category="spice"),
            Ingredient(name="garlic", quantity=2, unit="cloves", category="spice"),
            Ingredient(name="sesame seeds", quantity=1, unit="tbsp", category="other"),
        ],
        instructions=[
            RecipeInstruction(step_number=1, instruction="Mix soy sauce, honey, ginger, and garlic for teriyaki sauce"),
            RecipeInstruction(step_number=2, instruction="Marinate salmon in half the sauce for 15 minutes"),
            RecipeInstruction(step_number=3, instruction="Pan-sear salmon skin-side down for 4-5 minutes"),
            RecipeInstruction(step_number=4, instruction="Flip and cook for 3-4 more minutes"),
            RecipeInstruction(step_number=5, instruction="Brush with remaining sauce and garnish with sesame seeds"),
        ],
        dietary_tags=["gluten-free", "dairy-free"],
        nutrition=NutritionInfo(calories=320, protein=32, carbs=18, fat=14, fiber=0, sodium=920)
    ),
    
    # Recipe 6: Mushroom Risotto
    Recipe(
        id=uuid4(),
        title="Mushroom Risotto",
        description="Creamy Italian rice dish with wild mushrooms and parmesan",
        cuisine_type="Italian",
        difficulty="medium",
        prep_time=10,
        cook_time=30,
        servings=4,
        image_url="https://images.unsplash.com/photo-1476124369491-b79d6792cca2",
        ingredients=[
            Ingredient(name="arborio rice", quantity=300, unit="g", is_critical=True, category="grain"),
            Ingredient(name="mushrooms", quantity=400, unit="g", is_critical=True, category="vegetable"),
            Ingredient(name="vegetable broth", quantity=1000, unit="ml", category="other"),
            Ingredient(name="white wine", quantity=150, unit="ml", category="other"),
            Ingredient(name="parmesan cheese", quantity=100, unit="g", category="dairy"),
            Ingredient(name="butter", quantity=50, unit="g", category="dairy"),
            Ingredient(name="onion", quantity=1, unit="whole", category="vegetable"),
        ],
        instructions=[
            RecipeInstruction(step_number=1, instruction="Sauté mushrooms in butter until golden, set aside"),
            RecipeInstruction(step_number=2, instruction="Sauté onions in same pan until soft"),
            RecipeInstruction(step_number=3, instruction="Add rice, toast for 2 minutes"),
            RecipeInstruction(step_number=4, instruction="Add wine, stir until absorbed"),
            RecipeInstruction(step_number=5, instruction="Add broth one ladle at a time, stirring constantly until creamy"),
            RecipeInstruction(step_number=6, instruction="Stir in mushrooms and parmesan before serving"),
        ],
        dietary_tags=["vegetarian", "gluten-free"],
        nutrition=NutritionInfo(calories=440, protein=14, carbs=62, fat=15, fiber=3, sodium=720)
    ),
    
    # Recipe 7: Greek Salad
    Recipe(
        id=uuid4(),
        title="Traditional Greek Salad",
        description="Fresh Mediterranean salad with feta cheese and olives",
        cuisine_type="Greek",
        difficulty="easy",
        prep_time=15,
        cook_time=0,
        servings=4,
        image_url="https://images.unsplash.com/photo-1540189549336-e6e99c3679fe",
        ingredients=[
            Ingredient(name="cucumber", quantity=2, unit="whole", category="vegetable"),
            Ingredient(name="tomato", quantity=4, unit="whole", category="vegetable"),
            Ingredient(name="red onion", quantity=1, unit="whole", category="vegetable"),
            Ingredient(name="bell pepper", quantity=1, unit="whole", category="vegetable"),
            Ingredient(name="feta cheese", quantity=200, unit="g", category="dairy"),
            Ingredient(name="kalamata olives", quantity=100, unit="g", category="other"),
            Ingredient(name="olive oil", quantity=60, unit="ml", category="oil"),
            Ingredient(name="lemon juice", quantity=2, unit="tbsp", category="other"),
        ],
        instructions=[
            RecipeInstruction(step_number=1, instruction="Chop cucumbers, tomatoes, onion, and bell pepper into chunks"),
            RecipeInstruction(step_number=2, instruction="Combine vegetables in a large bowl"),
            RecipeInstruction(step_number=3, instruction="Add olives and crumbled feta cheese"),
            RecipeInstruction(step_number=4, instruction="Drizzle with olive oil and lemon juice"),
            RecipeInstruction(step_number=5, instruction="Toss gently and season with oregano, salt, and pepper"),
        ],
        dietary_tags=["vegetarian", "gluten-free", "low-carb"],
        nutrition=NutritionInfo(calories=220, protein=8, carbs=12, fat=17, fiber=3, sodium=620)
    ),
    
    # Recipe 8: Thai Green Curry
    Recipe(
        id=uuid4(),
        title="Thai Green Curry",
        description="Aromatic curry with coconut milk and fresh vegetables",
        cuisine_type="Thai",
        difficulty="medium",
        prep_time=15,
        cook_time=25,
        servings=4,
        image_url="https://images.unsplash.com/photo-1455619452474-d2be8b1e70cd",
        ingredients=[
            Ingredient(name="chicken breast", quantity=500, unit="g", is_critical=True, category="protein"),
            Ingredient(name="coconut milk", quantity=400, unit="ml", is_critical=True, category="other"),
            Ingredient(name="green curry paste", quantity=3, unit="tbsp", is_critical=True, category="spice"),
            Ingredient(name="bell pepper", quantity=2, unit="whole", category="vegetable"),
            Ingredient(name="bamboo shoots", quantity=200, unit="g", category="vegetable"),
            Ingredient(name="thai basil", quantity=1, unit="handful", category="vegetable"),
            Ingredient(name="fish sauce", quantity=2, unit="tbsp", category="other"),
        ],
        instructions=[
            RecipeInstruction(step_number=1, instruction="Heat curry paste in a pan until fragrant"),
            RecipeInstruction(step_number=2, instruction="Add chicken and cook until seared"),
            RecipeInstruction(step_number=3, instruction="Pour in coconut milk and bring to simmer"),
            RecipeInstruction(step_number=4, instruction="Add vegetables and cook for 15 minutes"),
            RecipeInstruction(step_number=5, instruction="Stir in fish sauce and Thai basil before serving"),
        ],
        dietary_tags=["gluten-free", "dairy-free"],
        nutrition=NutritionInfo(calories=380, protein=28, carbs=15, fat=25, fiber=3, sodium=890)
    ),
    
    # Recipe 9: Quinoa Stuffed Bell Peppers
    Recipe(
        id=uuid4(),
        title="Quinoa Stuffed Bell Peppers",
        description="Colorful peppers filled with quinoa, black beans, and vegetables",
        cuisine_type="American",
        difficulty="easy",
        prep_time=20,
        cook_time=35,
        servings=4,
        image_url="https://images.unsplash.com/photo-1518133683791-0b9de5a055f0",
        ingredients=[
            Ingredient(name="bell peppers", quantity=4, unit="whole", is_critical=True, category="vegetable"),
            Ingredient(name="quinoa", quantity=200, unit="g", is_critical=True, category="grain"),
            Ingredient(name="black beans", quantity=400, unit="g", category="protein"),
            Ingredient(name="corn", quantity=200, unit="g", category="vegetable"),
            Ingredient(name="tomato", quantity=2, unit="whole", category="vegetable"),
            Ingredient(name="cheese", quantity=100, unit="g", category="dairy"),
            Ingredient(name="cumin", quantity=1, unit="tsp", category="spice"),
        ],
        instructions=[
            RecipeInstruction(step_number=1, instruction="Cook quinoa according to package directions"),
            RecipeInstruction(step_number=2, instruction="Cut tops off bell peppers and remove seeds"),
            RecipeInstruction(step_number=3, instruction="Mix cooked quinoa with beans, corn, tomatoes, and spices"),
            RecipeInstruction(step_number=4, instruction="Stuff peppers with quinoa mixture"),
            RecipeInstruction(step_number=5, instruction="Top with cheese and bake at 180°C for 25-30 minutes"),
        ],
        dietary_tags=["vegetarian", "gluten-free"],
        nutrition=NutritionInfo(calories=340, protein=16, carbs=52, fat=8, fiber=11, sodium=420)
    ),
    
    # Recipe 10: Pad Thai
    Recipe(
        id=uuid4(),
        title="Pad Thai",
        description="Classic Thai stir-fried noodles with shrimp and peanuts",
        cuisine_type="Thai",
        difficulty="medium",
        prep_time=20,
        cook_time=15,
        servings=4,
        image_url="https://images.unsplash.com/photo-1559314809-0d155014e29e",
        ingredients=[
            Ingredient(name="rice noodles", quantity=400, unit="g", is_critical=True, category="grain"),
            Ingredient(name="shrimp", quantity=300, unit="g", is_critical=True, category="protein"),
            Ingredient(name="eggs", quantity=2, unit="whole", category="protein"),
            Ingredient(name="bean sprouts", quantity=200, unit="g", category="vegetable"),
            Ingredient(name="peanuts", quantity=100, unit="g", category="other"),
            Ingredient(name="tamarind paste", quantity=2, unit="tbsp", category="other"),
            Ingredient(name="fish sauce", quantity=3, unit="tbsp", category="other"),
        ],
        instructions=[
            RecipeInstruction(step_number=1, instruction="Soak rice noodles in warm water until soft"),
            RecipeInstruction(step_number=2, instruction="Stir-fry shrimp until pink, set aside"),
            RecipeInstruction(step_number=3, instruction="Scramble eggs in the same pan, set aside"),
            RecipeInstruction(step_number=4, instruction="Stir-fry noodles with tamarind and fish sauce"),
            RecipeInstruction(step_number=5, instruction="Add shrimp, eggs, bean sprouts, and peanuts, toss well"),
        ],
        dietary_tags=["gluten-free", "dairy-free"],
        nutrition=NutritionInfo(calories=480, protein=25, carbs=64, fat=15, fiber=4, sodium=950)
    ),
    
    # Recipe 11: Lentil Soup
    Recipe(
        id=uuid4(),
        title="Hearty Lentil Soup",
        description="Nutritious vegetarian soup with red lentils and vegetables",
        cuisine_type="Mediterranean",
        difficulty="easy",
        prep_time=10,
        cook_time=35,
        servings=6,
        image_url="https://images.unsplash.com/photo-1547592166-23ac45744acd",
        ingredients=[
            Ingredient(name="red lentils", quantity=300, unit="g", is_critical=True, category="protein"),
            Ingredient(name="carrot", quantity=2, unit="whole", category="vegetable"),
            Ingredient(name="celery", quantity=2, unit="stalks", category="vegetable"),
            Ingredient(name="onion", quantity=1, unit="whole", category="vegetable"),
            Ingredient(name="vegetable broth", quantity=1500, unit="ml", category="other"),
            Ingredient(name="cumin", quantity=1, unit="tsp", category="spice"),
            Ingredient(name="turmeric", quantity=1, unit="tsp", category="spice"),
        ],
        instructions=[
            RecipeInstruction(step_number=1, instruction="Chop carrots, celery, and onion"),
            RecipeInstruction(step_number=2, instruction="Sauté vegetables in olive oil until soft"),
            RecipeInstruction(step_number=3, instruction="Add lentils and spices, stir for 1 minute"),
            RecipeInstruction(step_number=4, instruction="Pour in broth and simmer for 30 minutes"),
            RecipeInstruction(step_number=5, instruction="Blend partially for creamy texture, season to taste"),
        ],
        dietary_tags=["vegetarian", "vegan", "gluten-free", "dairy-free"],
        nutrition=NutritionInfo(calories=220, protein=14, carbs=38, fat=2, fiber=15, sodium=520)
    ),
    
    # Recipe 12: Margherita Pizza
    Recipe(
        id=uuid4(),
        title="Margherita Pizza",
        description="Classic Italian pizza with tomato, mozzarella, and basil",
        cuisine_type="Italian",
        difficulty="medium",
        prep_time=90,
        cook_time=15,
        servings=4,
        image_url="https://images.unsplash.com/photo-1574071318508-1cdbab80d002",
        ingredients=[
            Ingredient(name="pizza dough", quantity=500, unit="g", is_critical=True, category="grain"),
            Ingredient(name="tomato sauce", quantity=200, unit="ml", is_critical=True, category="other"),
            Ingredient(name="mozzarella cheese", quantity=300, unit="g", is_critical=True, category="dairy"),
            Ingredient(name="fresh basil", quantity=1, unit="handful", category="vegetable"),
            Ingredient(name="olive oil", quantity=2, unit="tbsp", category="oil"),
            Ingredient(name="garlic", quantity=2, unit="cloves", category="spice"),
        ],
        instructions=[
            RecipeInstruction(step_number=1, instruction="Let pizza dough rise for 1 hour"),
            RecipeInstruction(step_number=2, instruction="Roll out dough into round pizza base"),
            RecipeInstruction(step_number=3, instruction="Spread tomato sauce evenly"),
            RecipeInstruction(step_number=4, instruction="Top with torn mozzarella and drizzle olive oil"),
            RecipeInstruction(step_number=5, instruction="Bake at 250°C for 12-15 minutes until crust is golden"),
            RecipeInstruction(step_number=6, instruction="Garnish with fresh basil leaves"),
        ],
        dietary_tags=["vegetarian"],
        nutrition=NutritionInfo(calories=520, protein=22, carbs=62, fat=20, fiber=3, sodium=890)
    ),
    
    # Recipe 13: Chicken Caesar Salad
    Recipe(
        id=uuid4(),
        title="Chicken Caesar Salad",
        description="Classic salad with grilled chicken, romaine, and creamy dressing",
        cuisine_type="American",
        difficulty="easy",
        prep_time=15,
        cook_time=15,
        servings=4,
        image_url="https://images.unsplash.com/photo-1546793665-c74683f339c1",
        ingredients=[
            Ingredient(name="chicken breast", quantity=400, unit="g", is_critical=True, category="protein"),
            Ingredient(name="romaine lettuce", quantity=2, unit="heads", is_critical=True, category="vegetable"),
            Ingredient(name="parmesan cheese", quantity=100, unit="g", category="dairy"),
            Ingredient(name="croutons", quantity=150, unit="g", category="grain"),
            Ingredient(name="caesar dressing", quantity=100, unit="ml", category="other"),
            Ingredient(name="lemon juice", quantity=2, unit="tbsp", category="other"),
        ],
        instructions=[
            RecipeInstruction(step_number=1, instruction="Season and grill chicken breast until cooked through"),
            RecipeInstruction(step_number=2, instruction="Slice chicken into strips"),
            RecipeInstruction(step_number=3, instruction="Chop romaine lettuce into bite-sized pieces"),
            RecipeInstruction(step_number=4, instruction="Toss lettuce with Caesar dressing"),
            RecipeInstruction(step_number=5, instruction="Top with chicken, croutons, and shaved parmesan"),
        ],
        dietary_tags=[],
        nutrition=NutritionInfo(calories=380, protein=32, carbs=22, fat=20, fiber=3, sodium=720)
    ),
    
    # Recipe 14: Vegetable Stir Fry
    Recipe(
        id=uuid4(),
        title="Vegetable Stir Fry",
        description="Quick and healthy stir-fried mixed vegetables with soy sauce",
        cuisine_type="Chinese",
        difficulty="easy",
        prep_time=15,
        cook_time=10,
        servings=4,
        image_url="https://images.unsplash.com/photo-1512058564366-18510be2db19",
        ingredients=[
            Ingredient(name="broccoli", quantity=300, unit="g", category="vegetable"),
            Ingredient(name="bell pepper", quantity=2, unit="whole", category="vegetable"),
            Ingredient(name="carrot", quantity=2, unit="whole", category="vegetable"),
            Ingredient(name="snow peas", quantity=200, unit="g", category="vegetable"),
            Ingredient(name="soy sauce", quantity=3, unit="tbsp", category="other"),
            Ingredient(name="ginger", quantity=1, unit="tbsp", category="spice"),
            Ingredient(name="garlic", quantity=3, unit="cloves", category="spice"),
            Ingredient(name="sesame oil", quantity=2, unit="tbsp", category="oil"),
        ],
        instructions=[
            RecipeInstruction(step_number=1, instruction="Cut all vegetables into similar-sized pieces"),
            RecipeInstruction(step_number=2, instruction="Heat sesame oil in a wok over high heat"),
            RecipeInstruction(step_number=3, instruction="Stir-fry ginger and garlic for 30 seconds"),
            RecipeInstruction(step_number=4, instruction="Add vegetables in order of cooking time, stir constantly"),
            RecipeInstruction(step_number=5, instruction="Add soy sauce and toss well, cook for 2 more minutes"),
        ],
        dietary_tags=["vegetarian", "vegan", "dairy-free"],
        nutrition=NutritionInfo(calories=150, protein=5, carbs=20, fat=7, fiber=6, sodium=680)
    ),
    
    # Recipe 15: Baked Cod with Lemon
    Recipe(
        id=uuid4(),
        title="Baked Cod with Lemon",
        description="Light and flaky cod fillet with fresh lemon and herbs",
        cuisine_type="Mediterranean",
        difficulty="easy",
        prep_time=10,
        cook_time=20,
        servings=4,
        image_url="https://images.unsplash.com/photo-1580959375944-58b0b5e1e8ed",
        ingredients=[
            Ingredient(name="cod fillets", quantity=4, unit="pieces", is_critical=True, category="protein"),
            Ingredient(name="lemon", quantity=2, unit="whole", category="other"),
            Ingredient(name="garlic", quantity=3, unit="cloves", category="spice"),
            Ingredient(name="parsley", quantity=1, unit="handful", category="vegetable"),
            Ingredient(name="olive oil", quantity=3, unit="tbsp", category="oil"),
            Ingredient(name="white wine", quantity=100, unit="ml", category="other"),
        ],
        instructions=[
            RecipeInstruction(step_number=1, instruction="Preheat oven to 200°C"),
            RecipeInstruction(step_number=2, instruction="Place cod fillets in a baking dish"),
            RecipeInstruction(step_number=3, instruction="Drizzle with olive oil, lemon juice, and white wine"),
            RecipeInstruction(step_number=4, instruction="Top with minced garlic and parsley"),
            RecipeInstruction(step_number=5, instruction="Bake for 15-20 minutes until fish flakes easily"),
        ],
        dietary_tags=["gluten-free", "dairy-free", "low-carb"],
        nutrition=NutritionInfo(calories=220, protein=30, carbs=3, fat=10, fiber=0, sodium=380)
    ),
    
    # Recipe 16: Black Bean Burgers
    Recipe(
        id=uuid4(),
        title="Black Bean Burgers",
        description="Hearty vegetarian burgers made with black beans and spices",
        cuisine_type="American",
        difficulty="medium",
        prep_time=20,
        cook_time=15,
        servings=4,
        image_url="https://images.unsplash.com/photo-1550547660-d9450f859349",
        ingredients=[
            Ingredient(name="black beans", quantity=400, unit="g", is_critical=True, category="protein"),
            Ingredient(name="breadcrumbs", quantity=100, unit="g", category="grain"),
            Ingredient(name="onion", quantity=1, unit="whole", category="vegetable"),
            Ingredient(name="egg", quantity=1, unit="whole", category="protein"),
            Ingredient(name="cumin", quantity=1, unit="tsp", category="spice"),
            Ingredient(name="paprika", quantity=1, unit="tsp", category="spice"),
            Ingredient(name="burger buns", quantity=4, unit="whole", is_critical=True, category="grain"),
        ],
        instructions=[
            RecipeInstruction(step_number=1, instruction="Mash black beans in a large bowl"),
            RecipeInstruction(step_number=2, instruction="Mix in breadcrumbs, diced onion, egg, and spices"),
            RecipeInstruction(step_number=3, instruction="Form mixture into 4 burger patties"),
            RecipeInstruction(step_number=4, instruction="Pan-fry or grill patties for 6-7 minutes per side"),
            RecipeInstruction(step_number=5, instruction="Serve on toasted buns with your favorite toppings"),
        ],
        dietary_tags=["vegetarian"],
        nutrition=NutritionInfo(calories=320, protein=15, carbs=52, fat=6, fiber=12, sodium=520)
    ),
    
    # Recipe 17: Shrimp Scampi
    Recipe(
        id=uuid4(),
        title="Shrimp Scampi",
        description="Garlicky shrimp in white wine butter sauce over pasta",
        cuisine_type="Italian",
        difficulty="easy",
        prep_time=10,
        cook_time=15,
        servings=4,
        image_url="https://images.unsplash.com/photo-1633504581786-316c8002c1e8",
        ingredients=[
            Ingredient(name="shrimp", quantity=500, unit="g", is_critical=True, category="protein"),
            Ingredient(name="linguine", quantity=400, unit="g", is_critical=True, category="grain"),
            Ingredient(name="garlic", quantity=6, unit="cloves", category="spice"),
            Ingredient(name="white wine", quantity=150, unit="ml", category="other"),
            Ingredient(name="butter", quantity=60, unit="g", category="dairy"),
            Ingredient(name="lemon", quantity=1, unit="whole", category="other"),
            Ingredient(name="parsley", quantity=1, unit="handful", category="vegetable"),
        ],
        instructions=[
            RecipeInstruction(step_number=1, instruction="Cook linguine according to package directions"),
            RecipeInstruction(step_number=2, instruction="Sauté garlic in butter until fragrant"),
            RecipeInstruction(step_number=3, instruction="Add shrimp and cook until pink"),
            RecipeInstruction(step_number=4, instruction="Add white wine and lemon juice, simmer for 3 minutes"),
            RecipeInstruction(step_number=5, instruction="Toss with cooked pasta and fresh parsley"),
        ],
        dietary_tags=[],
        nutrition=NutritionInfo(calories=480, protein=32, carbs=52, fat=16, fiber=3, sodium=620)
    ),
    
    # Recipe 18: Chickpea Curry
    Recipe(
        id=uuid4(),
        title="Chickpea Curry",
        description="Flavorful vegan curry with chickpeas in tomato-coconut sauce",
        cuisine_type="Indian",
        difficulty="easy",
        prep_time=10,
        cook_time=25,
        servings=4,
        image_url="https://images.unsplash.com/photo-1585937421612-70a008356fbe",
        ingredients=[
            Ingredient(name="chickpeas", quantity=800, unit="g", is_critical=True, category="protein"),
            Ingredient(name="coconut milk", quantity=400, unit="ml", is_critical=True, category="other"),
            Ingredient(name="tomato", quantity=400, unit="g", category="vegetable"),
            Ingredient(name="onion", quantity=1, unit="whole", category="vegetable"),
            Ingredient(name="curry powder", quantity=2, unit="tbsp", category="spice"),
            Ingredient(name="ginger", quantity=1, unit="tbsp", category="spice"),
            Ingredient(name="garlic", quantity=3, unit="cloves", category="spice"),
            Ingredient(name="spinach", quantity=200, unit="g", category="vegetable"),
        ],
        instructions=[
            RecipeInstruction(step_number=1, instruction="Sauté onion, ginger, and garlic until soft"),
            RecipeInstruction(step_number=2, instruction="Add curry powder and cook for 1 minute"),
            RecipeInstruction(step_number=3, instruction="Add tomatoes and simmer for 10 minutes"),
            RecipeInstruction(step_number=4, instruction="Stir in chickpeas and coconut milk"),
            RecipeInstruction(step_number=5, instruction="Add spinach and cook until wilted, season to taste"),
        ],
        dietary_tags=["vegetarian", "vegan", "gluten-free", "dairy-free"],
        nutrition=NutritionInfo(calories=380, protein=14, carbs=42, fat=18, fiber=12, sodium=420)
    ),
    
    # Recipe 19: Beef Stir Fry
    Recipe(
        id=uuid4(),
        title="Beef and Broccoli Stir Fry",
        description="Tender beef with crisp broccoli in savory Asian sauce",
        cuisine_type="Chinese",
        difficulty="easy",
        prep_time=20,
        cook_time=15,
        servings=4,
        image_url="https://images.unsplash.com/photo-1603360946369-dc9bb6258143",
        ingredients=[
            Ingredient(name="beef sirloin", quantity=500, unit="g", is_critical=True, category="protein"),
            Ingredient(name="broccoli", quantity=400, unit="g", category="vegetable"),
            Ingredient(name="soy sauce", quantity=4, unit="tbsp", category="other"),
            Ingredient(name="oyster sauce", quantity=2, unit="tbsp", category="other"),
            Ingredient(name="ginger", quantity=1, unit="tbsp", category="spice"),
            Ingredient(name="garlic", quantity=3, unit="cloves", category="spice"),
            Ingredient(name="cornstarch", quantity=1, unit="tbsp", category="other"),
        ],
        instructions=[
            RecipeInstruction(step_number=1, instruction="Slice beef thinly against the grain"),
            RecipeInstruction(step_number=2, instruction="Marinate beef in soy sauce and cornstarch for 15 minutes"),
            RecipeInstruction(step_number=3, instruction="Stir-fry beef in hot oil until browned, remove from pan"),
            RecipeInstruction(step_number=4, instruction="Stir-fry broccoli with ginger and garlic"),
            RecipeInstruction(step_number=5, instruction="Return beef to pan, add oyster sauce, toss well"),
        ],
        dietary_tags=["dairy-free"],
        nutrition=NutritionInfo(calories=320, protein=35, carbs=15, fat=14, fiber=4, sodium=980)
    ),
    
    # Recipe 20: Caprese Salad
    Recipe(
        id=uuid4(),
        title="Caprese Salad",
        description="Simple Italian salad with tomatoes, mozzarella, and basil",
        cuisine_type="Italian",
        difficulty="easy",
        prep_time=10,
        cook_time=0,
        servings=4,
        image_url="https://images.unsplash.com/photo-1592417817038-d13bb0b50e33",
        ingredients=[
            Ingredient(name="tomatoes", quantity=4, unit="whole", is_critical=True, category="vegetable"),
            Ingredient(name="fresh mozzarella", quantity=300, unit="g", is_critical=True, category="dairy"),
            Ingredient(name="fresh basil", quantity=1, unit="handful", category="vegetable"),
            Ingredient(name="olive oil", quantity=3, unit="tbsp", category="oil"),
            Ingredient(name="balsamic vinegar", quantity=2, unit="tbsp", category="other"),
            Ingredient(name="salt", quantity=1, unit="tsp", category="spice"),
        ],
        instructions=[
            RecipeInstruction(step_number=1, instruction="Slice tomatoes and mozzarella into 1/4 inch rounds"),
            RecipeInstruction(step_number=2, instruction="Arrange alternating slices on a platter"),
            RecipeInstruction(step_number=3, instruction="Tuck fresh basil leaves between slices"),
            RecipeInstruction(step_number=4, instruction="Drizzle with olive oil and balsamic vinegar"),
            RecipeInstruction(step_number=5, instruction="Season with salt and pepper to taste"),
        ],
        dietary_tags=["vegetarian", "gluten-free", "low-carb"],
        nutrition=NutritionInfo(calories=250, protein=14, carbs=8, fat=20, fiber=2, sodium=420)
    ),
    
    # Recipe 21: Pork Chops with Apples
    Recipe(
        id=uuid4(),
        title="Pork Chops with Apples",
        description="Pan-seared pork chops with caramelized apples and onions",
        cuisine_type="American",
        difficulty="medium",
        prep_time=15,
        cook_time=25,
        servings=4,
        image_url="https://images.unsplash.com/photo-1432139555190-58524dae6a55",
        ingredients=[
            Ingredient(name="pork chops", quantity=4, unit="pieces", is_critical=True, category="protein"),
            Ingredient(name="apples", quantity=2, unit="whole", category="vegetable"),
            Ingredient(name="onion", quantity=1, unit="whole", category="vegetable"),
            Ingredient(name="butter", quantity=30, unit="g", category="dairy"),
            Ingredient(name="thyme", quantity=1, unit="tsp", category="spice"),
            Ingredient(name="apple cider", quantity=100, unit="ml", category="other"),
        ],
        instructions=[
            RecipeInstruction(step_number=1, instruction="Season pork chops with salt, pepper, and thyme"),
            RecipeInstruction(step_number=2, instruction="Sear pork chops in butter until golden on both sides"),
            RecipeInstruction(step_number=3, instruction="Remove chops and sauté sliced apples and onions"),
            RecipeInstruction(step_number=4, instruction="Add apple cider and simmer until reduced"),
            RecipeInstruction(step_number=5, instruction="Return pork chops, cook until internal temp reaches 63°C"),
        ],
        dietary_tags=["gluten-free"],
        nutrition=NutritionInfo(calories=380, protein=36, carbs=22, fat=18, fiber=3, sodium=420)
    ),
    
    # Recipe 22: Veggie Fajitas
    Recipe(
        id=uuid4(),
        title="Vegetable Fajitas",
        description="Sizzling bell peppers and onions with warm tortillas",
        cuisine_type="Mexican",
        difficulty="easy",
        prep_time=15,
        cook_time=15,
        servings=4,
        image_url="https://images.unsplash.com/photo-1599974875801-0dc473993d11",
        ingredients=[
            Ingredient(name="bell peppers", quantity=3, unit="whole", is_critical=True, category="vegetable"),
            Ingredient(name="onion", quantity=2, unit="whole", category="vegetable"),
            Ingredient(name="flour tortillas", quantity=8, unit="whole", is_critical=True, category="grain"),
            Ingredient(name="lime", quantity=1, unit="whole", category="other"),
            Ingredient(name="cumin", quantity=1, unit="tsp", category="spice"),
            Ingredient(name="chili powder", quantity=1, unit="tsp", category="spice"),
            Ingredient(name="sour cream", quantity=100, unit="ml", category="dairy"),
        ],
        instructions=[
            RecipeInstruction(step_number=1, instruction="Slice bell peppers and onions into strips"),
            RecipeInstruction(step_number=2, instruction="Heat oil in a large skillet over high heat"),
            RecipeInstruction(step_number=3, instruction="Stir-fry vegetables with cumin and chili powder"),
            RecipeInstruction(step_number=4, instruction="Squeeze lime juice over vegetables"),
            RecipeInstruction(step_number=5, instruction="Warm tortillas and serve with vegetables and toppings"),
        ],
        dietary_tags=["vegetarian"],
        nutrition=NutritionInfo(calories=320, protein=8, carbs=54, fat=9, fiber=6, sodium=420)
    ),
    
    # Recipe 23: Tuna Poke Bowl
    Recipe(
        id=uuid4(),
        title="Tuna Poke Bowl",
        description="Hawaiian-style fresh tuna bowl with rice and vegetables",
        cuisine_type="Hawaiian",
        difficulty="easy",
        prep_time=20,
        cook_time=15,
        servings=4,
        image_url="https://images.unsplash.com/photo-1546069901-ba9599a7e63c",
        ingredients=[
            Ingredient(name="sushi-grade tuna", quantity=400, unit="g", is_critical=True, category="protein"),
            Ingredient(name="sushi rice", quantity=300, unit="g", is_critical=True, category="grain"),
            Ingredient(name="edamame", quantity=200, unit="g", category="protein"),
            Ingredient(name="avocado", quantity=2, unit="whole", category="vegetable"),
            Ingredient(name="cucumber", quantity=1, unit="whole", category="vegetable"),
            Ingredient(name="soy sauce", quantity=3, unit="tbsp", category="other"),
            Ingredient(name="sesame oil", quantity=1, unit="tbsp", category="oil"),
        ],
        instructions=[
            RecipeInstruction(step_number=1, instruction="Cook sushi rice according to package directions"),
            RecipeInstruction(step_number=2, instruction="Dice tuna into cubes and marinate in soy sauce and sesame oil"),
            RecipeInstruction(step_number=3, instruction="Prepare vegetables: slice avocado and cucumber"),
            RecipeInstruction(step_number=4, instruction="Cook edamame in boiling water"),
            RecipeInstruction(step_number=5, instruction="Assemble bowls with rice, tuna, and vegetables"),
        ],
        dietary_tags=["gluten-free", "dairy-free"],
        nutrition=NutritionInfo(calories=420, protein=28, carbs=48, fat=14, fiber=6, sodium=820)
    ),
    
    # Recipe 24: Eggplant Parmesan
    Recipe(
        id=uuid4(),
        title="Eggplant Parmesan",
        description="Breaded eggplant slices baked with marinara and cheese",
        cuisine_type="Italian",
        difficulty="medium",
        prep_time=30,
        cook_time=40,
        servings=6,
        image_url="https://images.unsplash.com/photo-1515516969601-9eef52c3e42f",
        ingredients=[
            Ingredient(name="eggplant", quantity=2, unit="whole", is_critical=True, category="vegetable"),
            Ingredient(name="marinara sauce", quantity=500, unit="ml", is_critical=True, category="other"),
            Ingredient(name="mozzarella cheese", quantity=300, unit="g", category="dairy"),
            Ingredient(name="parmesan cheese", quantity=100, unit="g", category="dairy"),
            Ingredient(name="breadcrumbs", quantity=200, unit="g", category="grain"),
            Ingredient(name="eggs", quantity=2, unit="whole", category="protein"),
        ],
        instructions=[
            RecipeInstruction(step_number=1, instruction="Slice eggplant into 1/2 inch rounds and salt to remove moisture"),
            RecipeInstruction(step_number=2, instruction="Dip eggplant in beaten eggs, then coat in breadcrumbs"),
            RecipeInstruction(step_number=3, instruction="Fry breaded eggplant until golden on both sides"),
            RecipeInstruction(step_number=4, instruction="Layer eggplant, marinara, and cheeses in baking dish"),
            RecipeInstruction(step_number=5, instruction="Bake at 180°C for 30 minutes until cheese is bubbly"),
        ],
        dietary_tags=["vegetarian"],
        nutrition=NutritionInfo(calories=420, protein=20, carbs=42, fat=20, fiber=8, sodium=920)
    ),
    
    # Recipe 25: Chicken Quesadillas
    Recipe(
        id=uuid4(),
        title="Chicken Quesadillas",
        description="Crispy tortillas filled with chicken and melted cheese",
        cuisine_type="Mexican",
        difficulty="easy",
        prep_time=15,
        cook_time=15,
        servings=4,
        image_url="https://images.unsplash.com/photo-1618040996337-56904b7850b9",
        ingredients=[
            Ingredient(name="chicken breast", quantity=400, unit="g", is_critical=True, category="protein"),
            Ingredient(name="flour tortillas", quantity=8, unit="whole", is_critical=True, category="grain"),
            Ingredient(name="cheese", quantity=300, unit="g", is_critical=True, category="dairy"),
            Ingredient(name="bell pepper", quantity=1, unit="whole", category="vegetable"),
            Ingredient(name="onion", quantity=1, unit="whole", category="vegetable"),
            Ingredient(name="cumin", quantity=1, unit="tsp", category="spice"),
        ],
        instructions=[
            RecipeInstruction(step_number=1, instruction="Cook chicken with cumin and seasonings, then dice"),
            RecipeInstruction(step_number=2, instruction="Sauté bell pepper and onion until soft"),
            RecipeInstruction(step_number=3, instruction="Place cheese, chicken, and vegetables on half of tortilla"),
            RecipeInstruction(step_number=4, instruction="Fold tortilla in half and cook in pan until crispy"),
            RecipeInstruction(step_number=5, instruction="Flip and cook other side, cut into wedges"),
        ],
        dietary_tags=[],
        nutrition=NutritionInfo(calories=480, protein=32, carbs=42, fat=22, fiber=3, sodium=720)
    ),
    
    # Recipe 26: Minestrone Soup
    Recipe(
        id=uuid4(),
        title="Minestrone Soup",
        description="Hearty Italian vegetable soup with pasta and beans",
        cuisine_type="Italian",
        difficulty="easy",
        prep_time=15,
        cook_time=35,
        servings=6,
        image_url="https://images.unsplash.com/photo-1547592166-23ac45744acd",
        ingredients=[
            Ingredient(name="kidney beans", quantity=400, unit="g", category="protein"),
            Ingredient(name="tomato", quantity=400, unit="g", category="vegetable"),
            Ingredient(name="carrot", quantity=2, unit="whole", category="vegetable"),
            Ingredient(name="celery", quantity=2, unit="stalks", category="vegetable"),
            Ingredient(name="zucchini", quantity=1, unit="whole", category="vegetable"),
            Ingredient(name="pasta", quantity=150, unit="g", category="grain"),
            Ingredient(name="vegetable broth", quantity=1500, unit="ml", category="other"),
        ],
        instructions=[
            RecipeInstruction(step_number=1, instruction="Chop all vegetables into small pieces"),
            RecipeInstruction(step_number=2, instruction="Sauté carrots, celery, and onion in olive oil"),
            RecipeInstruction(step_number=3, instruction="Add broth, tomatoes, and beans, bring to boil"),
            RecipeInstruction(step_number=4, instruction="Add zucchini and pasta, simmer for 15 minutes"),
            RecipeInstruction(step_number=5, instruction="Season with Italian herbs and serve"),
        ],
        dietary_tags=["vegetarian", "vegan", "dairy-free"],
        nutrition=NutritionInfo(calories=240, protein=11, carbs=45, fat=3, fiber=10, sodium=620)
    ),
    
    # Recipe 27: Honey Garlic Chicken
    Recipe(
        id=uuid4(),
        title="Honey Garlic Chicken",
        description="Sweet and savory chicken thighs with sticky honey garlic glaze",
        cuisine_type="American",
        difficulty="easy",
        prep_time=10,
        cook_time=25,
        servings=4,
        image_url="https://images.unsplash.com/photo-1598103442097-8b74394b95c6",
        ingredients=[
            Ingredient(name="chicken thighs", quantity=800, unit="g", is_critical=True, category="protein"),
            Ingredient(name="honey", quantity=80, unit="ml", is_critical=True, category="other"),
            Ingredient(name="soy sauce", quantity=60, unit="ml", category="other"),
            Ingredient(name="garlic", quantity=6, unit="cloves", category="spice"),
            Ingredient(name="ginger", quantity=1, unit="tbsp", category="spice"),
            Ingredient(name="cornstarch", quantity=1, unit="tbsp", category="other"),
        ],
        instructions=[
            RecipeInstruction(step_number=1, instruction="Season chicken thighs with salt and pepper"),
            RecipeInstruction(step_number=2, instruction="Sear chicken in hot pan until golden, set aside"),
            RecipeInstruction(step_number=3, instruction="Sauté garlic and ginger in same pan"),
            RecipeInstruction(step_number=4, instruction="Mix honey, soy sauce, and cornstarch, add to pan"),
            RecipeInstruction(step_number=5, instruction="Return chicken, simmer until sauce thickens and chicken is cooked"),
        ],
        dietary_tags=["gluten-free", "dairy-free"],
        nutrition=NutritionInfo(calories=380, protein=34, carbs=28, fat=16, fiber=0, sodium=920)
    ),
    
    # Recipe 28: Ratatouille
    Recipe(
        id=uuid4(),
        title="Ratatouille",
        description="Classic French vegetable stew with eggplant, zucchini, and tomatoes",
        cuisine_type="French",
        difficulty="medium",
        prep_time=20,
        cook_time=45,
        servings=6,
        image_url="https://images.unsplash.com/photo-1572453800999-e8d2d1589b7c",
        ingredients=[
            Ingredient(name="eggplant", quantity=1, unit="whole", is_critical=True, category="vegetable"),
            Ingredient(name="zucchini", quantity=2, unit="whole", is_critical=True, category="vegetable"),
            Ingredient(name="tomato", quantity=4, unit="whole", is_critical=True, category="vegetable"),
            Ingredient(name="bell pepper", quantity=2, unit="whole", category="vegetable"),
            Ingredient(name="onion", quantity=1, unit="whole", category="vegetable"),
            Ingredient(name="garlic", quantity=4, unit="cloves", category="spice"),
            Ingredient(name="thyme", quantity=2, unit="tsp", category="spice"),
            Ingredient(name="olive oil", quantity=60, unit="ml", category="oil"),
        ],
        instructions=[
            RecipeInstruction(step_number=1, instruction="Slice all vegetables into thin rounds"),
            RecipeInstruction(step_number=2, instruction="Sauté onion and garlic in olive oil"),
            RecipeInstruction(step_number=3, instruction="Add bell pepper and cook until soft"),
            RecipeInstruction(step_number=4, instruction="Layer vegetables in a baking dish in alternating pattern"),
            RecipeInstruction(step_number=5, instruction="Drizzle with olive oil, sprinkle with thyme, bake at 190°C for 40 minutes"),
        ],
        dietary_tags=["vegetarian", "vegan", "gluten-free", "dairy-free", "low-carb"],
        nutrition=NutritionInfo(calories=180, protein=4, carbs=22, fat=10, fiber=7, sodium=220)
    ),
    
    # Recipe 29: Sushi Rolls
    Recipe(
        id=uuid4(),
        title="California Sushi Rolls",
        description="Fresh sushi rolls with crab, avocado, and cucumber",
        cuisine_type="Japanese",
        difficulty="hard",
        prep_time=40,
        cook_time=20,
        servings=4,
        image_url="https://images.unsplash.com/photo-1579584425555-c3ce17fd4351",
        ingredients=[
            Ingredient(name="sushi rice", quantity=400, unit="g", is_critical=True, category="grain"),
            Ingredient(name="nori sheets", quantity=8, unit="whole", is_critical=True, category="other"),
            Ingredient(name="imitation crab", quantity=200, unit="g", is_critical=True, category="protein"),
            Ingredient(name="avocado", quantity=2, unit="whole", category="vegetable"),
            Ingredient(name="cucumber", quantity=1, unit="whole", category="vegetable"),
            Ingredient(name="rice vinegar", quantity=3, unit="tbsp", category="other"),
            Ingredient(name="sesame seeds", quantity=2, unit="tbsp", category="other"),
        ],
        instructions=[
            RecipeInstruction(step_number=1, instruction="Cook sushi rice and season with rice vinegar"),
            RecipeInstruction(step_number=2, instruction="Slice avocado and cucumber into thin strips"),
            RecipeInstruction(step_number=3, instruction="Place nori on bamboo mat, spread rice evenly"),
            RecipeInstruction(step_number=4, instruction="Add crab, avocado, and cucumber in a line"),
            RecipeInstruction(step_number=5, instruction="Roll tightly using mat, slice into 8 pieces, garnish with sesame seeds"),
        ],
        dietary_tags=["dairy-free"],
        nutrition=NutritionInfo(calories=320, protein=12, carbs=52, fat=8, fiber=4, sodium=520)
    ),
    
    # Recipe 30: Shakshuka
    Recipe(
        id=uuid4(),
        title="Shakshuka",
        description="Middle Eastern poached eggs in spicy tomato sauce",
        cuisine_type="Middle Eastern",
        difficulty="easy",
        prep_time=10,
        cook_time=25,
        servings=4,
        image_url="https://images.unsplash.com/photo-1595777216528-071e0127ccf4",
        ingredients=[
            Ingredient(name="eggs", quantity=6, unit="whole", is_critical=True, category="protein"),
            Ingredient(name="tomato", quantity=800, unit="g", is_critical=True, category="vegetable"),
            Ingredient(name="bell pepper", quantity=2, unit="whole", category="vegetable"),
            Ingredient(name="onion", quantity=1, unit="whole", category="vegetable"),
            Ingredient(name="garlic", quantity=4, unit="cloves", category="spice"),
            Ingredient(name="cumin", quantity=1, unit="tsp", category="spice"),
            Ingredient(name="paprika", quantity=1, unit="tsp", category="spice"),
            Ingredient(name="feta cheese", quantity=100, unit="g", category="dairy"),
        ],
        instructions=[
            RecipeInstruction(step_number=1, instruction="Sauté onion, bell pepper, and garlic until soft"),
            RecipeInstruction(step_number=2, instruction="Add tomatoes, cumin, and paprika, simmer for 15 minutes"),
            RecipeInstruction(step_number=3, instruction="Make small wells in sauce and crack eggs into them"),
            RecipeInstruction(step_number=4, instruction="Cover and cook until egg whites are set"),
            RecipeInstruction(step_number=5, instruction="Top with crumbled feta and fresh herbs"),
        ],
        dietary_tags=["vegetarian", "gluten-free", "low-carb"],
        nutrition=NutritionInfo(calories=240, protein=14, carbs=18, fat=14, fiber=5, sodium=520)
    ),
    
    # Recipe 31: Paneer Butter Masala
    Recipe(
        id=uuid4(),
        title="Paneer Butter Masala",
        description="Creamy tomato-based curry with soft paneer cubes finished with butter",
        cuisine_type="Indian",
        difficulty="medium",
        prep_time=15,
        cook_time=25,
        servings=4,
        image_url="https://images.unsplash.com/photo-1604908176997-4310a94d860b",
        ingredients=[
            Ingredient(name="paneer", quantity=300, unit="g", is_critical=True, category="protein"),
            Ingredient(name="tomato", quantity=400, unit="g", is_critical=True, category="vegetable"),
            Ingredient(name="onion", quantity=1, unit="whole", category="vegetable"),
            Ingredient(name="cream", quantity=100, unit="ml", category="dairy"),
            Ingredient(name="butter", quantity=30, unit="g", category="dairy"),
            Ingredient(name="garam masala", quantity=1, unit="tsp", category="spice"),
            Ingredient(name="ginger", quantity=1, unit="tbsp", category="spice"),
            Ingredient(name="garlic", quantity=3, unit="cloves", category="spice"),
        ],
        instructions=[
            RecipeInstruction(step_number=1, instruction="Sauté onions in butter; add ginger-garlic"),
            RecipeInstruction(step_number=2, instruction="Add tomatoes and spices; cook until thick"),
            RecipeInstruction(step_number=3, instruction="Blend to a smooth sauce and return to pan"),
            RecipeInstruction(step_number=4, instruction="Add cream and paneer; simmer 5 minutes"),
            RecipeInstruction(step_number=5, instruction="Finish with butter and garam masala"),
        ],
        dietary_tags=["vegetarian", "gluten-free"],
        nutrition=NutritionInfo(calories=430, protein=18, carbs=20, fat=30, fiber=4, sodium=780)
    ),

    # Recipe 32: Dal Makhani
    Recipe(
        id=uuid4(),
        title="Dal Makhani",
        description="Slow-cooked black lentils and kidney beans finished with butter and cream",
        cuisine_type="Indian",
        difficulty="medium",
        prep_time=10,
        cook_time=60,
        servings=6,
        image_url="https://images.unsplash.com/photo-1640434913931-2d24d90228e1",
        ingredients=[
            Ingredient(name="black lentils (urad)", quantity=300, unit="g", is_critical=True, category="protein"),
            Ingredient(name="kidney beans", quantity=50, unit="g", category="protein"),
            Ingredient(name="tomato", quantity=300, unit="g", category="vegetable"),
            Ingredient(name="butter", quantity=40, unit="g", category="dairy"),
            Ingredient(name="cream", quantity=80, unit="ml", category="dairy"),
            Ingredient(name="ginger", quantity=1, unit="tbsp", category="spice"),
            Ingredient(name="garam masala", quantity=1, unit="tsp", category="spice"),
        ],
        instructions=[
            RecipeInstruction(step_number=1, instruction="Pressure cook lentils and beans until soft"),
            RecipeInstruction(step_number=2, instruction="Cook tomato and spices in butter"),
            RecipeInstruction(step_number=3, instruction="Combine with lentils and simmer 30 minutes"),
            RecipeInstruction(step_number=4, instruction="Stir in cream and garam masala"),
            RecipeInstruction(step_number=5, instruction="Simmer low until rich and creamy"),
        ],
        dietary_tags=["vegetarian", "gluten-free"],
        nutrition=NutritionInfo(calories=360, protein=17, carbs=38, fat=14, fiber=12, sodium=620)
    ),

    # Recipe 33: Palak Paneer
    Recipe(
        id=uuid4(),
        title="Palak Paneer",
        description="Paneer simmered in a smooth spinach gravy with spices",
        cuisine_type="Indian",
        difficulty="easy",
        prep_time=15,
        cook_time=20,
        servings=4,
        image_url="https://images.unsplash.com/photo-1604908554027-183eb89c6bb7",
        ingredients=[
            Ingredient(name="spinach", quantity=400, unit="g", is_critical=True, category="vegetable"),
            Ingredient(name="paneer", quantity=250, unit="g", is_critical=True, category="protein"),
            Ingredient(name="onion", quantity=1, unit="whole", category="vegetable"),
            Ingredient(name="tomato", quantity=1, unit="whole", category="vegetable"),
            Ingredient(name="cream", quantity=50, unit="ml", category="dairy"),
            Ingredient(name="garam masala", quantity=1, unit="tsp", category="spice"),
        ],
        instructions=[
            RecipeInstruction(step_number=1, instruction="Blanch spinach and blend to purée"),
            RecipeInstruction(step_number=2, instruction="Sauté onion and tomato with spices"),
            RecipeInstruction(step_number=3, instruction="Add spinach purée and simmer"),
            RecipeInstruction(step_number=4, instruction="Add paneer cubes and cream; cook briefly"),
            RecipeInstruction(step_number=5, instruction="Adjust seasoning and serve"),
        ],
        dietary_tags=["vegetarian", "gluten-free"],
        nutrition=NutritionInfo(calories=320, protein=18, carbs=16, fat=22, fiber=6, sodium=560)
    ),

    # Recipe 34: Chole Masala
    Recipe(
        id=uuid4(),
        title="Chole Masala",
        description="Punjabi-style spicy chickpea curry",
        cuisine_type="Indian",
        difficulty="easy",
        prep_time=10,
        cook_time=30,
        servings=4,
        image_url="https://images.unsplash.com/photo-1589308078059-be1415eab4c3",
        ingredients=[
            Ingredient(name="chickpeas", quantity=500, unit="g", is_critical=True, category="protein"),
            Ingredient(name="onion", quantity=2, unit="whole", category="vegetable"),
            Ingredient(name="tomato", quantity=300, unit="g", category="vegetable"),
            Ingredient(name="chole masala", quantity=2, unit="tbsp", category="spice"),
            Ingredient(name="ginger", quantity=1, unit="tbsp", category="spice"),
            Ingredient(name="garlic", quantity=4, unit="cloves", category="spice"),
        ],
        instructions=[
            RecipeInstruction(step_number=1, instruction="Sauté onions with ginger-garlic"),
            RecipeInstruction(step_number=2, instruction="Add tomatoes and spice blend; cook down"),
            RecipeInstruction(step_number=3, instruction="Add cooked chickpeas and simmer 15 minutes"),
            RecipeInstruction(step_number=4, instruction="Crush a few chickpeas to thicken"),
            RecipeInstruction(step_number=5, instruction="Finish with cilantro and lemon"),
        ],
        dietary_tags=["vegetarian", "vegan", "gluten-free"],
        nutrition=NutritionInfo(calories=310, protein=14, carbs=46, fat=7, fiber=11, sodium=520)
    ),

    # Recipe 35: Aloo Gobi
    Recipe(
        id=uuid4(),
        title="Aloo Gobi",
        description="Dry stir-fry of cauliflower and potatoes with spices",
        cuisine_type="Indian",
        difficulty="easy",
        prep_time=10,
        cook_time=20,
        servings=4,
        image_url="https://images.unsplash.com/photo-1604908553868-5a7c233d6a94",
        ingredients=[
            Ingredient(name="cauliflower", quantity=500, unit="g", is_critical=True, category="vegetable"),
            Ingredient(name="potato", quantity=300, unit="g", is_critical=True, category="vegetable"),
            Ingredient(name="turmeric", quantity=0.5, unit="tsp", category="spice"),
            Ingredient(name="cumin seeds", quantity=1, unit="tsp", category="spice"),
            Ingredient(name="ginger", quantity=1, unit="tsp", category="spice"),
        ],
        instructions=[
            RecipeInstruction(step_number=1, instruction="Heat oil; splutter cumin and sauté ginger"),
            RecipeInstruction(step_number=2, instruction="Add potatoes and cauliflower with spices"),
            RecipeInstruction(step_number=3, instruction="Cover and cook until tender"),
            RecipeInstruction(step_number=4, instruction="Uncover to crisp edges"),
            RecipeInstruction(step_number=5, instruction="Finish with cilantro and lemon"),
        ],
        dietary_tags=["vegetarian", "vegan", "gluten-free", "low-carb"],
        nutrition=NutritionInfo(calories=220, protein=7, carbs=30, fat=8, fiber=8, sodium=420)
    ),

    # Recipe 36: Bhindi Masala
    Recipe(
        id=uuid4(),
        title="Bhindi Masala",
        description="Okra stir-fried with onions, tomatoes, and spices",
        cuisine_type="Indian",
        difficulty="easy",
        prep_time=10,
        cook_time=15,
        servings=4,
        image_url="https://images.unsplash.com/photo-1624359136355-e1c5a7da5b1c",
        ingredients=[
            Ingredient(name="okra", quantity=400, unit="g", is_critical=True, category="vegetable"),
            Ingredient(name="onion", quantity=1, unit="whole", category="vegetable"),
            Ingredient(name="tomato", quantity=1, unit="whole", category="vegetable"),
            Ingredient(name="coriander powder", quantity=1, unit="tsp", category="spice"),
            Ingredient(name="turmeric", quantity=0.5, unit="tsp", category="spice"),
        ],
        instructions=[
            RecipeInstruction(step_number=1, instruction="Sauté okra separately until non-sticky"),
            RecipeInstruction(step_number=2, instruction="Sauté onions and tomatoes with spices"),
            RecipeInstruction(step_number=3, instruction="Combine okra and cook a few minutes"),
            RecipeInstruction(step_number=4, instruction="Adjust seasoning"),
            RecipeInstruction(step_number=5, instruction="Serve hot with roti"),
        ],
        dietary_tags=["vegetarian", "vegan", "gluten-free", "low-carb"],
        nutrition=NutritionInfo(calories=190, protein=5, carbs=18, fat=9, fiber=6, sodium=380)
    ),

    # Recipe 37: Baingan Bharta
    Recipe(
        id=uuid4(),
        title="Baingan Bharta",
        description="Smoky roasted eggplant mash cooked with onions and tomatoes",
        cuisine_type="Indian",
        difficulty="easy",
        prep_time=15,
        cook_time=25,
        servings=4,
        image_url="https://images.unsplash.com/photo-1544025162-d76694265947",
        ingredients=[
            Ingredient(name="eggplant", quantity=600, unit="g", is_critical=True, category="vegetable"),
            Ingredient(name="onion", quantity=1, unit="whole", category="vegetable"),
            Ingredient(name="tomato", quantity=2, unit="whole", category="vegetable"),
            Ingredient(name="garlic", quantity=4, unit="cloves", category="spice"),
            Ingredient(name="cumin seeds", quantity=1, unit="tsp", category="spice"),
        ],
        instructions=[
            RecipeInstruction(step_number=1, instruction="Roast eggplant until charred; peel and mash"),
            RecipeInstruction(step_number=2, instruction="Sauté onions, garlic, and cumin"),
            RecipeInstruction(step_number=3, instruction="Add tomatoes and cook down"),
            RecipeInstruction(step_number=4, instruction="Stir in mashed eggplant and cook 10 minutes"),
            RecipeInstruction(step_number=5, instruction="Finish with cilantro"),
        ],
        dietary_tags=["vegetarian", "vegan", "gluten-free"],
        nutrition=NutritionInfo(calories=210, protein=5, carbs=22, fat=12, fiber=7, sodium=360)
    ),

    # Recipe 38: Rogan Josh
    Recipe(
        id=uuid4(),
        title="Rogan Josh",
        description="Kashmiri-style aromatic lamb curry with yogurt and spices",
        cuisine_type="Indian",
        difficulty="medium",
        prep_time=15,
        cook_time=45,
        servings=6,
        image_url="https://images.unsplash.com/photo-1625943543163-3a7f1f2b5751",
        ingredients=[
            Ingredient(name="lamb", quantity=800, unit="g", is_critical=True, category="protein"),
            Ingredient(name="yogurt", quantity=150, unit="ml", category="dairy"),
            Ingredient(name="onion", quantity=2, unit="whole", category="vegetable"),
            Ingredient(name="rogan josh masala", quantity=2, unit="tbsp", category="spice"),
            Ingredient(name="ginger garlic paste", quantity=1, unit="tbsp", category="spice"),
        ],
        instructions=[
            RecipeInstruction(step_number=1, instruction="Brown lamb pieces in oil"),
            RecipeInstruction(step_number=2, instruction="Add onions and sauté"),
            RecipeInstruction(step_number=3, instruction="Stir in masala and yogurt; cook covered"),
            RecipeInstruction(step_number=4, instruction="Simmer until tender and gravy thick"),
            RecipeInstruction(step_number=5, instruction="Rest and serve"),
        ],
        dietary_tags=["gluten-free"],
        nutrition=NutritionInfo(calories=420, protein=35, carbs=10, fat=26, fiber=2, sodium=740)
    ),

    # Recipe 39: Chicken Chettinad
    Recipe(
        id=uuid4(),
        title="Chicken Chettinad",
        description="Spicy South Indian chicken curry with roasted spices",
        cuisine_type="Indian",
        difficulty="medium",
        prep_time=15,
        cook_time=30,
        servings=5,
        image_url="https://images.unsplash.com/photo-1589302168068-964664d93dc0",
        ingredients=[
            Ingredient(name="chicken", quantity=800, unit="g", is_critical=True, category="protein"),
            Ingredient(name="onion", quantity=2, unit="whole", category="vegetable"),
            Ingredient(name="tomato", quantity=2, unit="whole", category="vegetable"),
            Ingredient(name="chettinad masala", quantity=2, unit="tbsp", category="spice"),
            Ingredient(name="curry leaves", quantity=1, unit="sprig", category="vegetable"),
        ],
        instructions=[
            RecipeInstruction(step_number=1, instruction="Roast and grind chettinad spices (if using whole)"),
            RecipeInstruction(step_number=2, instruction="Sauté onions and curry leaves; add masala"),
            RecipeInstruction(step_number=3, instruction="Add chicken and tomatoes; cook covered"),
            RecipeInstruction(step_number=4, instruction="Simmer until chicken is tender"),
            RecipeInstruction(step_number=5, instruction="Adjust seasoning and serve"),
        ],
        dietary_tags=["gluten-free", "dairy-free"],
        nutrition=NutritionInfo(calories=360, protein=32, carbs=8, fat=22, fiber=2, sodium=640)
    ),

    # Recipe 40: Goan Fish Curry
    Recipe(
        id=uuid4(),
        title="Goan Fish Curry",
        description="Tangy coconut-based fish curry with tamarind and spices",
        cuisine_type="Indian",
        difficulty="easy",
        prep_time=10,
        cook_time=20,
        servings=4,
        image_url="https://images.unsplash.com/photo-1583336663277-620dc1996580",
        ingredients=[
            Ingredient(name="fish fillets", quantity=600, unit="g", is_critical=True, category="protein"),
            Ingredient(name="coconut milk", quantity=300, unit="ml", is_critical=True, category="other"),
            Ingredient(name="tamarind", quantity=1, unit="tbsp", category="other"),
            Ingredient(name="onion", quantity=1, unit="whole", category="vegetable"),
            Ingredient(name="red chili powder", quantity=1, unit="tsp", category="spice"),
        ],
        instructions=[
            RecipeInstruction(step_number=1, instruction="Sauté onions with spice powders"),
            RecipeInstruction(step_number=2, instruction="Add coconut milk and tamarind; bring to simmer"),
            RecipeInstruction(step_number=3, instruction="Slide in fish; cook until just done"),
            RecipeInstruction(step_number=4, instruction="Rest 5 minutes for flavors to meld"),
            RecipeInstruction(step_number=5, instruction="Serve with steamed rice"),
        ],
        dietary_tags=["gluten-free", "dairy-free"],
        nutrition=NutritionInfo(calories=310, protein=28, carbs=8, fat=18, fiber=1, sodium=520)
    ),

    # Recipe 41: Vegetable Biryani
    Recipe(
        id=uuid4(),
        title="Vegetable Biryani",
        description="Layered basmati rice with spiced mixed vegetables and fried onions",
        cuisine_type="Indian",
        difficulty="medium",
        prep_time=20,
        cook_time=35,
        servings=6,
        image_url="https://images.unsplash.com/photo-1625943537649-b4b38183b081",
        ingredients=[
            Ingredient(name="basmati rice", quantity=500, unit="g", is_critical=True, category="grain"),
            Ingredient(name="mixed vegetables", quantity=400, unit="g", is_critical=True, category="vegetable"),
            Ingredient(name="yogurt", quantity=150, unit="ml", category="dairy"),
            Ingredient(name="biryani masala", quantity=2, unit="tbsp", category="spice"),
            Ingredient(name="onion", quantity=2, unit="whole", category="vegetable"),
        ],
        instructions=[
            RecipeInstruction(step_number=1, instruction="Parboil rice with whole spices"),
            RecipeInstruction(step_number=2, instruction="Cook vegetables with biryani masala and yogurt"),
            RecipeInstruction(step_number=3, instruction="Layer rice and veggies; top with fried onions"),
            RecipeInstruction(step_number=4, instruction="Dum cook 15 minutes"),
            RecipeInstruction(step_number=5, instruction="Fluff and serve"),
        ],
        dietary_tags=["vegetarian"],
        nutrition=NutritionInfo(calories=420, protein=10, carbs=78, fat=8, fiber=5, sodium=680)
    ),

    # Recipe 42: Rajma Masala
    Recipe(
        id=uuid4(),
        title="Rajma Masala",
        description="North Indian kidney bean curry with onion-tomato gravy",
        cuisine_type="Indian",
        difficulty="easy",
        prep_time=10,
        cook_time=35,
        servings=4,
        image_url="https://images.unsplash.com/photo-1595433562696-cc7f2f9b5f17",
        ingredients=[
            Ingredient(name="kidney beans", quantity=500, unit="g", is_critical=True, category="protein"),
            Ingredient(name="onion", quantity=2, unit="whole", category="vegetable"),
            Ingredient(name="tomato", quantity=300, unit="g", category="vegetable"),
            Ingredient(name="rajma masala", quantity=2, unit="tbsp", category="spice"),
        ],
        instructions=[
            RecipeInstruction(step_number=1, instruction="Cook soaked beans until soft"),
            RecipeInstruction(step_number=2, instruction="Make onion-tomato masala with spices"),
            RecipeInstruction(step_number=3, instruction="Combine and simmer 15 minutes"),
            RecipeInstruction(step_number=4, instruction="Mash a few beans to thicken"),
            RecipeInstruction(step_number=5, instruction="Serve with steamed rice"),
        ],
        dietary_tags=["vegetarian", "vegan", "gluten-free"],
        nutrition=NutritionInfo(calories=330, protein=15, carbs=55, fat=4, fiber=13, sodium=540)
    ),

    # Recipe 43: Kadai Paneer
    Recipe(
        id=uuid4(),
        title="Kadai Paneer",
        description="Stir-fried paneer with bell peppers in a roasted spice gravy",
        cuisine_type="Indian",
        difficulty="easy",
        prep_time=10,
        cook_time=20,
        servings=4,
        image_url="https://images.unsplash.com/photo-1625943538989-5a9b2bcb8ecf",
        ingredients=[
            Ingredient(name="paneer", quantity=300, unit="g", is_critical=True, category="protein"),
            Ingredient(name="bell pepper", quantity=2, unit="whole", category="vegetable"),
            Ingredient(name="onion", quantity=1, unit="whole", category="vegetable"),
            Ingredient(name="tomato", quantity=2, unit="whole", category="vegetable"),
            Ingredient(name="kadai masala", quantity=2, unit="tsp", category="spice"),
        ],
        instructions=[
            RecipeInstruction(step_number=1, instruction="Roast and grind kadai masala (or use ready)"),
            RecipeInstruction(step_number=2, instruction="Sauté onions and peppers; add tomatoes"),
            RecipeInstruction(step_number=3, instruction="Stir in masala and paneer; cook briefly"),
            RecipeInstruction(step_number=4, instruction="Finish with kasuri methi"),
            RecipeInstruction(step_number=5, instruction="Serve with roti or naan"),
        ],
        dietary_tags=["vegetarian", "gluten-free"],
        nutrition=NutritionInfo(calories=340, protein=17, carbs=18, fat=22, fiber=5, sodium=560)
    ),

    # Recipe 44: Malai Kofta
    Recipe(
        id=uuid4(),
        title="Malai Kofta",
        description="Fried paneer-potato dumplings in a rich creamy gravy",
        cuisine_type="Indian",
        difficulty="hard",
        prep_time=25,
        cook_time=30,
        servings=4,
        image_url="https://images.unsplash.com/photo-1625943541911-4d9c1f2e1a41",
        ingredients=[
            Ingredient(name="paneer", quantity=200, unit="g", is_critical=True, category="protein"),
            Ingredient(name="potato", quantity=200, unit="g", is_critical=True, category="vegetable"),
            Ingredient(name="cream", quantity=100, unit="ml", category="dairy"),
            Ingredient(name="cashew", quantity=40, unit="g", category="other"),
            Ingredient(name="tomato", quantity=300, unit="g", category="vegetable"),
        ],
        instructions=[
            RecipeInstruction(step_number=1, instruction="Make kofta mixture from paneer and potato; fry"),
            RecipeInstruction(step_number=2, instruction="Prepare cashew-tomato cream gravy"),
            RecipeInstruction(step_number=3, instruction="Add koftas to gravy just before serving"),
            RecipeInstruction(step_number=4, instruction="Simmer 2 minutes to absorb flavors"),
            RecipeInstruction(step_number=5, instruction="Garnish with cream"),
        ],
        dietary_tags=["vegetarian", "gluten-free"],
        nutrition=NutritionInfo(calories=480, protein=16, carbs=28, fat=34, fiber=3, sodium=700)
    ),

    # Recipe 45: Laal Maas
    Recipe(
        id=uuid4(),
        title="Laal Maas",
        description="Rajasthani hot mutton curry with mathania chilies",
        cuisine_type="Indian",
        difficulty="medium",
        prep_time=15,
        cook_time=40,
        servings=5,
        image_url="https://images.unsplash.com/photo-1617191519400-9db6466b7403",
        ingredients=[
            Ingredient(name="mutton", quantity=800, unit="g", is_critical=True, category="protein"),
            Ingredient(name="yogurt", quantity=120, unit="ml", category="dairy"),
            Ingredient(name="red chili paste", quantity=2, unit="tbsp", category="spice"),
            Ingredient(name="garlic", quantity=6, unit="cloves", category="spice"),
        ],
        instructions=[
            RecipeInstruction(step_number=1, instruction="Marinate mutton with yogurt and chili"),
            RecipeInstruction(step_number=2, instruction="Sear meat; add garlic and spices"),
            RecipeInstruction(step_number=3, instruction="Add water and simmer till tender"),
            RecipeInstruction(step_number=4, instruction="Reduce to thick gravy"),
            RecipeInstruction(step_number=5, instruction="Rest before serving"),
        ],
        dietary_tags=["gluten-free", "dairy"],
        nutrition=NutritionInfo(calories=450, protein=36, carbs=6, fat=30, fiber=1, sodium=780)
    ),

    # Recipe 46: Kerala Fish Moilee
    Recipe(
        id=uuid4(),
        title="Kerala Fish Moilee",
        description="Mild coconut milk fish stew with ginger and green chilies",
        cuisine_type="Indian",
        difficulty="easy",
        prep_time=10,
        cook_time=20,
        servings=4,
        image_url="https://images.unsplash.com/photo-1553163147-622ab57be1c7",
        ingredients=[
            Ingredient(name="fish fillets", quantity=600, unit="g", is_critical=True, category="protein"),
            Ingredient(name="coconut milk", quantity=350, unit="ml", is_critical=True, category="other"),
            Ingredient(name="ginger", quantity=1, unit="tbsp", category="spice"),
            Ingredient(name="green chili", quantity=2, unit="whole", category="spice"),
            Ingredient(name="curry leaves", quantity=1, unit="sprig", category="vegetable"),
        ],
        instructions=[
            RecipeInstruction(step_number=1, instruction="Temper curry leaves, ginger, and chili"),
            RecipeInstruction(step_number=2, instruction="Add coconut milk; bring to gentle simmer"),
            RecipeInstruction(step_number=3, instruction="Add fish; cook until flaky"),
            RecipeInstruction(step_number=4, instruction="Season and serve"),
            RecipeInstruction(step_number=5, instruction="Optional: finish with coconut oil"),
        ],
        dietary_tags=["gluten-free", "dairy-free"],
        nutrition=NutritionInfo(calories=300, protein=27, carbs=6, fat=18, fiber=1, sodium=480)
    ),

    # Recipe 47: Paneer Tikka
    Recipe(
        id=uuid4(),
        title="Paneer Tikka",
        description="Marinated paneer and peppers skewered and roasted",
        cuisine_type="Indian",
        difficulty="easy",
        prep_time=20,
        cook_time=15,
        servings=4,
        image_url="https://images.unsplash.com/photo-1617196034796-5f3c2aaca5fa",
        ingredients=[
            Ingredient(name="paneer", quantity=350, unit="g", is_critical=True, category="protein"),
            Ingredient(name="yogurt", quantity=120, unit="ml", category="dairy"),
            Ingredient(name="tikka masala", quantity=2, unit="tbsp", category="spice"),
            Ingredient(name="bell pepper", quantity=2, unit="whole", category="vegetable"),
            Ingredient(name="onion", quantity=1, unit="whole", category="vegetable"),
        ],
        instructions=[
            RecipeInstruction(step_number=1, instruction="Marinate paneer and veggies in yogurt-masala"),
            RecipeInstruction(step_number=2, instruction="Skewer and roast/grill until charred"),
            RecipeInstruction(step_number=3, instruction="Baste with butter or oil midway"),
            RecipeInstruction(step_number=4, instruction="Sprinkle chaat masala"),
            RecipeInstruction(step_number=5, instruction="Serve with mint chutney"),
        ],
        dietary_tags=["vegetarian", "gluten-free"],
        nutrition=NutritionInfo(calories=340, protein=20, carbs=12, fat=24, fiber=3, sodium=520)
    ),

    # Recipe 48: Egg Curry
    Recipe(
        id=uuid4(),
        title="Egg Curry",
        description="Boiled eggs simmered in onion-tomato gravy",
        cuisine_type="Indian",
        difficulty="easy",
        prep_time=10,
        cook_time=20,
        servings=4,
        image_url="https://images.unsplash.com/photo-1615485929964-0f9e66d5645e",
        ingredients=[
            Ingredient(name="eggs", quantity=6, unit="whole", is_critical=True, category="protein"),
            Ingredient(name="onion", quantity=2, unit="whole", category="vegetable"),
            Ingredient(name="tomato", quantity=2, unit="whole", category="vegetable"),
            Ingredient(name="garam masala", quantity=1, unit="tsp", category="spice"),
            Ingredient(name="ginger garlic paste", quantity=1, unit="tbsp", category="spice"),
        ],
        instructions=[
            RecipeInstruction(step_number=1, instruction="Prepare onion-tomato masala with spices"),
            RecipeInstruction(step_number=2, instruction="Add water to make gravy; simmer"),
            RecipeInstruction(step_number=3, instruction="Add halved boiled eggs and simmer 5 minutes"),
            RecipeInstruction(step_number=4, instruction="Finish with cilantro"),
            RecipeInstruction(step_number=5, instruction="Serve with rice or roti"),
        ],
        dietary_tags=["gluten-free"],
        nutrition=NutritionInfo(calories=280, protein=18, carbs=10, fat=18, fiber=2, sodium=520)
    ),

    # Recipe 49: Pindi Chole
    Recipe(
        id=uuid4(),
        title="Pindi Chole",
        description="Dry-style chickpea curry from Rawalpindi with robust spices",
        cuisine_type="Indian",
        difficulty="easy",
        prep_time=10,
        cook_time=30,
        servings=4,
        image_url="https://images.unsplash.com/photo-1626076594271-0f6c4af64a63",
        ingredients=[
            Ingredient(name="chickpeas", quantity=500, unit="g", is_critical=True, category="protein"),
            Ingredient(name="pindi chole masala", quantity=2, unit="tbsp", category="spice"),
            Ingredient(name="onion", quantity=1, unit="whole", category="vegetable"),
            Ingredient(name="ginger", quantity=1, unit="tbsp", category="spice"),
        ],
        instructions=[
            RecipeInstruction(step_number=1, instruction="Cook chickpeas until soft"),
            RecipeInstruction(step_number=2, instruction="Sauté aromatics; add masala"),
            RecipeInstruction(step_number=3, instruction="Add chickpeas; cook until dry and coated"),
            RecipeInstruction(step_number=4, instruction="Finish with slit chilies and ginger juliennes"),
            RecipeInstruction(step_number=5, instruction="Serve with bhature or puri"),
        ],
        dietary_tags=["vegetarian", "vegan", "gluten-free"],
        nutrition=NutritionInfo(calories=320, protein=14, carbs=46, fat=7, fiber=11, sodium=540)
    ),

    # Recipe 50: Veg Pulao
    Recipe(
        id=uuid4(),
        title="Veg Pulao",
        description="Fragrant basmati rice cooked with mixed vegetables and whole spices",
        cuisine_type="Indian",
        difficulty="easy",
        prep_time=10,
        cook_time=20,
        servings=4,
        image_url="https://images.unsplash.com/photo-1605475127380-0f7f3a1d9d4d",
        ingredients=[
            Ingredient(name="basmati rice", quantity=300, unit="g", is_critical=True, category="grain"),
            Ingredient(name="mixed vegetables", quantity=250, unit="g", is_critical=True, category="vegetable"),
            Ingredient(name="whole spices (bay, cinnamon, cloves)", quantity=1, unit="tbsp", category="spice"),
            Ingredient(name="ghee", quantity=1, unit="tbsp", category="other"),
            Ingredient(name="onion", quantity=1, unit="whole", category="vegetable"),
        ],
        instructions=[
            RecipeInstruction(step_number=1, instruction="Sauté whole spices and onions in ghee"),
            RecipeInstruction(step_number=2, instruction="Add vegetables and rinsed rice; sauté briefly"),
            RecipeInstruction(step_number=3, instruction="Add water; cook until rice is fluffy"),
            RecipeInstruction(step_number=4, instruction="Rest 5 minutes before fluffing"),
            RecipeInstruction(step_number=5, instruction="Garnish with fried onions or nuts"),
        ],
        dietary_tags=["vegetarian"],
        nutrition=NutritionInfo(calories=360, protein=7, carbs=68, fat=7, fiber=4, sodium=420)
    ),
]

