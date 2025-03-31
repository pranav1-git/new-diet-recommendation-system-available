import os
import csv
import pandas as pd
import numpy as np
from flask import Flask, render_template, request, jsonify, session
from flask_session import Session
from flask_cors import CORS
import random

app = Flask(__name__, static_folder="static", template_folder="templates")
app.config["SESSION_TYPE"] = "filesystem"  # Can be "redis", "mongodb", etc.
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_USE_SIGNER"] = True  # Helps prevent session tampering
app.config["SESSION_FILE_DIR"] = "./flask_sessions"  # Directory to store session files
Session(app)
app.secret_key = "diet_recommendation_secret_key"  # For session handling
CORS(app)  # Enable CORS for API access

# Global variable for food data
food_data = None


def load_food_data():
    global food_data
    try:
        # Try to load the included food data
        current_dir = os.path.dirname(os.path.abspath(__file__))
        food_data = pd.read_csv(os.path.join(current_dir, "food_data_3.csv"))
        print("Food database loaded successfully!")
        return True
    except:
        print("Creating sample food database...")
        create_sample_food_data()
        return True


def create_sample_food_data():
    global food_data
    # Create a sample food database
    data = {
        "Food_items": [
            "Chicken Breast",
            "Salmon",
            "Lentils",
            "Brown Rice",
            "Quinoa",
            "Spinach",
            "Broccoli",
            "Sweet Potato",
            "Banana",
            "Oatmeal",
            "Greek Yogurt",
            "Eggs",
            "Tofu",
            "Almonds",
            "Avocado",
            "Whole Wheat Bread",
            "Apple",
            "Cottage Cheese",
            "Black Beans",
            "Blueberries",
        ],
        "Category": [
            "Protein",
            "Protein",
            "Protein",
            "Grain",
            "Grain",
            "Vegetable",
            "Vegetable",
            "Vegetable",
            "Fruit",
            "Grain",
            "Dairy",
            "Protein",
            "Protein",
            "Nuts",
            "Fruit",
            "Grain",
            "Fruit",
            "Dairy",
            "Protein",
            "Fruit",
        ],
        "Calories": [
            165,
            208,
            230,
            215,
            222,
            23,
            55,
            112,
            105,
            150,
            100,
            78,
            94,
            164,
            234,
            75,
            95,
            120,
            227,
            84,
        ],
        "Fats": [
            3.6,
            13.0,
            0.8,
            1.8,
            3.6,
            0.4,
            0.6,
            0.1,
            0.4,
            2.5,
            0.7,
            5.3,
            5.3,
            14.2,
            21.0,
            1.1,
            0.3,
            5.0,
            0.9,
            0.5,
        ],
        "Protein": [
            31.0,
            22.0,
            18.0,
            5.0,
            8.1,
            2.9,
            3.7,
            2.0,
            1.3,
            5.0,
            17.0,
            6.3,
            10.0,
            6.0,
            2.9,
            4.0,
            0.5,
            25.0,
            15.0,
            1.1,
        ],
        "Iron": [
            0.9,
            0.5,
            6.6,
            0.8,
            2.8,
            2.7,
            0.7,
            0.6,
            0.3,
            1.7,
            0.1,
            1.2,
            2.7,
            3.7,
            0.6,
            1.4,
            0.1,
            0.2,
            3.6,
            0.4,
        ],
        "Carbohydrates": [
            0.0,
            0.0,
            40.0,
            45.0,
            39.0,
            3.6,
            11.0,
            26.0,
            27.0,
            27.0,
            6.0,
            0.6,
            2.0,
            6.0,
            12.0,
            13.8,
            25.0,
            3.0,
            41.0,
            21.0,
        ],
        "Fibre": [
            0.0,
            0.0,
            16.0,
            3.5,
            5.2,
            2.2,
            2.6,
            3.0,
            3.1,
            4.0,
            0.0,
            0.0,
            0.5,
            3.5,
            9.8,
            2.7,
            4.4,
            0.0,
            15.0,
            3.6,
        ],
        "Sugar": [
            0.0,
            0.0,
            2.0,
            0.7,
            1.0,
            0.4,
            1.7,
            5.4,
            14.0,
            0.0,
            4.0,
            0.6,
            0.0,
            1.2,
            0.7,
            1.5,
            19.0,
            3.0,
            0.5,
            14.7,
        ],
        "Meal_Type": [
            "Lunch,Dinner",
            "Lunch,Dinner",
            "Lunch,Dinner",
            "All",
            "All",
            "All",
            "Lunch,Dinner",
            "Lunch,Dinner",
            "Breakfast,Snack",
            "Breakfast",
            "Breakfast,Snack",
            "Breakfast",
            "Lunch,Dinner",
            "Snack",
            "All",
            "Breakfast,Snack",
            "Snack",
            "Breakfast,Snack",
            "Lunch,Dinner",
            "Snack",
        ],
        "Sodium": [
            74,
            61,
            4,
            5,
            7,
            79,
            33,
            72,
            1,
            2,
            36,
            62,
            7,
            0,
            7,
            137,
            1,
            457,
            2,
            1,
        ],
        "Vegetarian": [
            False,
            False,
            True,
            True,
            True,
            True,
            True,
            True,
            True,
            True,
            True,
            False,
            True,
            True,
            True,
            True,
            True,
            True,
            True,
            True,
        ],
        "Vegan": [
            False,
            False,
            True,
            True,
            True,
            True,
            True,
            True,
            True,
            True,
            False,
            False,
            True,
            True,
            True,
            True,
            True,
            False,
            True,
            True,
        ],
    }

    food_data = pd.DataFrame(data)

    # Save the sample data to a CSV file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    food_data.to_csv(os.path.join(current_dir, "sample_food_data.csv"), index=False)

    print("Sample food database created successfully!")


def calculate_bmi(weight, height):
    """Calculate BMI from weight (kg) and height (cm)"""
    height_m = height / 100  # convert cm to m
    bmi = weight / (height_m * height_m)
    return round(bmi, 2)


def calculate_calorie_requirements(age, weight, height, gender, activity_level, goal):
    """Calculate calorie and macronutrient requirements"""
    # Calculate Basal Metabolic Rate (BMR) using Mifflin-St Jeor Equation
    if gender == "Male":
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161

    # Apply activity multiplier
    activity_multipliers = {
        "Sedentary": 1.2,
        "Lightly Active": 1.375,
        "Moderately Active": 1.55,
        "Very Active": 1.725,
        "Extremely Active": 1.9,
    }

    tdee = bmr * activity_multipliers.get(activity_level, 1.375)

    # Adjust based on goal
    if goal == "Weight Loss":
        calories = tdee - 500  # 500 calorie deficit
    elif goal == "Muscle Gain":
        calories = tdee + 300  # 300 calorie surplus
    else:  # Maintenance or General Health
        calories = tdee

    # Calculate macronutrient ratios based on goal
    if goal == "Weight Loss":
        protein_pct = 0.35
        fat_pct = 0.30
        carb_pct = 0.35
    elif goal == "Muscle Gain":
        protein_pct = 0.30
        fat_pct = 0.25
        carb_pct = 0.45
    else:  # Maintenance or General Health
        protein_pct = 0.25
        fat_pct = 0.30
        carb_pct = 0.45

    # Calculate grams of each macronutrient
    protein_g = (calories * protein_pct) / 4  # 4 calories per gram of protein
    fat_g = (calories * fat_pct) / 9  # 9 calories per gram of fat
    carb_g = (calories * carb_pct) / 4  # 4 calories per gram of carb

    # Estimate fiber needs (14g per 1000 calories is a common recommendation)
    fiber_g = (calories / 1000) * 14

    return {
        "calories": round(calories),
        "protein": round(protein_g),
        "fat": round(fat_g),
        "carbs": round(carb_g),
        "fiber": round(fiber_g),
    }


def filter_foods_by_preferences(
    foods_df, vegetarian, vegan, low_carb, low_fat, high_protein, allergies
):
    """Filter foods based on dietary preferences and allergies"""
    # Make a copy to avoid changing the original
    filtered_df = foods_df.copy()

    # Apply dietary restrictions
    if vegetarian:
        filtered_df = filtered_df[filtered_df["Vegetarian"] == True]

    if vegan:
        filtered_df = filtered_df[filtered_df["Vegan"] == True]

    # Apply allergies filtering
    if allergies:
        allergies_list = [a.strip().lower() for a in allergies.split(",")]
        for allergy in allergies_list:
            filtered_df = filtered_df[
                ~filtered_df["Food_items"].str.lower().str.contains(allergy)
            ]

    # Apply low carb preference
    if low_carb:
        # Filter for foods where carbs are less than 20% of calories
        filtered_df = filtered_df[
            filtered_df["Carbohydrates"] * 4 / (filtered_df["Calories"] + 0.001) < 0.2
        ]

    # Apply low fat preference
    if low_fat:
        # Filter for foods where fat is less than 25% of calories
        filtered_df = filtered_df[
            filtered_df["Fats"] * 9 / (filtered_df["Calories"] + 0.001) < 0.25
        ]

    # Apply high protein preference
    if high_protein:
        # Filter for foods where protein is more than 25% of calories
        filtered_df = filtered_df[
            filtered_df["Protein"] * 4 / (filtered_df["Calories"] + 0.001) > 0.25
        ]

    return filtered_df


def score_foods(foods_df, nutrition_req, goal):
    """Score foods based on nutritional content and user goals"""
    # Make a copy to avoid changing the original
    scored_df = foods_df.copy()

    # Add a score column
    scored_df["score"] = 0

    # Score based on goal
    if goal == "Weight Loss":
        # For weight loss, prioritize high protein, high fiber, low calorie density
        scored_df["score"] += (
            scored_df["Protein"] / (scored_df["Calories"] + 1) * 20
        )  # Protein per calorie
        scored_df["score"] += (
            scored_df["Fibre"] / (scored_df["Calories"] + 1) * 15
        )  # Fiber per calorie
        scored_df["score"] -= (
            scored_df["Sugar"] / (scored_df["Calories"] + 1) * 10
        )  # Penalize sugar

    elif goal == "Muscle Gain":
        # For muscle gain, prioritize high protein, adequate carbs, nutrient density
        scored_df["score"] += scored_df["Protein"] * 0.3  # Value total protein
        scored_df["score"] += (
            scored_df["Carbohydrates"] * 0.1
        )  # Value carbs but less than protein
        scored_df["score"] += scored_df["Iron"] * 5  # Value iron for recovery

    elif goal == "General Health":
        # For general health, prioritize nutrient density, fiber, balanced macros
        scored_df["score"] += scored_df["Fibre"] * 1.5
        scored_df["score"] += scored_df["Protein"] * 0.3
        scored_df["score"] -= (
            scored_df["Sugar"] * 0.2
        )  # Penalize sugar but less than in weight loss
        scored_df["score"] -= (
            scored_df["Sodium"] * 0.01
        )  # Slightly penalize high sodium

    else:  # Maintenance
        # For maintenance, balanced scoring
        scored_df["score"] += scored_df["Protein"] * 0.2
        scored_df["score"] += scored_df["Fibre"] * 0.8
        scored_df["score"] -= scored_df["Sugar"] * 0.1

    # Normalize the scores (0-100 range)
    min_score = scored_df["score"].min()
    max_score = scored_df["score"].max()

    if max_score > min_score:  # Avoid division by zero
        scored_df["score"] = (
            100 * (scored_df["score"] - min_score) / (max_score - min_score)
        )

    return scored_df


def categorize_foods_by_meal(scored_foods):
    """Categorize foods by meal type"""
    meal_categories = {"breakfast": [], "lunch": [], "dinner": [], "snacks": []}

    # Sort foods by score (descending)
    sorted_foods = scored_foods.sort_values(by="score", ascending=False)

    # Assign foods to meal categories based on Meal_Type
    for _, food in sorted_foods.iterrows():
        food_dict = food.to_dict()
        meal_types = food["Meal_Type"].split(",")

        if "Breakfast" in meal_types:
            meal_categories["breakfast"].append(food_dict)

        if "Lunch" in meal_types:
            meal_categories["lunch"].append(food_dict)

        if "Dinner" in meal_types:
            meal_categories["dinner"].append(food_dict)

        if "Snack" in meal_types:
            meal_categories["snacks"].append(food_dict)

    # In case of missing meal type assignments, add top foods to appropriate meals
    all_foods = sorted_foods.to_dict("records")

    for meal_type in meal_categories:
        if len(meal_categories[meal_type]) < 5:
            for food in all_foods:
                if (
                    food not in meal_categories[meal_type]
                    and len(meal_categories[meal_type]) < 5
                ):
                    meal_categories[meal_type].append(food)

    return meal_categories


def generate_weekly_meal_plan(categorized_foods, nutrition_req):
    """Generate a weekly meal plan from Monday to Sunday"""
    days_of_week = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]
    weekly_plan = {}

    # Create a plan for each day
    for day in days_of_week:
        # Initialize daily structure
        weekly_plan[day] = {"breakfast": [], "lunch": [], "dinner": [], "snacks": []}

        # Fill in each meal with 2-3 items from appropriate category
        # Add some variety by shuffling the foods
        breakfast_options = categorized_foods["breakfast"].copy()
        lunch_options = categorized_foods["lunch"].copy()
        dinner_options = categorized_foods["dinner"].copy()
        snack_options = categorized_foods["snacks"].copy()

        random.shuffle(breakfast_options)
        random.shuffle(lunch_options)
        random.shuffle(dinner_options)
        random.shuffle(snack_options)

        # Take top 3 items for each meal type to ensure variety across the week
        weekly_plan[day]["breakfast"] = breakfast_options[:3]
        weekly_plan[day]["lunch"] = lunch_options[:3]
        weekly_plan[day]["dinner"] = dinner_options[:3]
        weekly_plan[day]["snacks"] = snack_options[:2]

    return weekly_plan


def calculate_weekly_nutritional_totals(weekly_plan):
    """Calculate nutritional totals for the week and for each day"""
    # Initialize daily and weekly totals
    nutritional_totals = {
        "weekly": {"protein": 0, "carbs": 0, "fat": 0, "fiber": 0, "calories": 0},
        "daily": {},
    }

    days_of_week = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]

    # Calculate totals for each day
    for day in days_of_week:
        daily_totals = {
            "protein": 0,
            "carbs": 0,
            "fat": 0,
            "fiber": 0,
            "calories": 0,
            "meal_calories": {"breakfast": 0, "lunch": 0, "dinner": 0, "snacks": 0},
        }

        for meal, foods in weekly_plan[day].items():
            meal_calories = 0
            for food in foods:
                daily_totals["protein"] += food["Protein"]
                daily_totals["carbs"] += food["Carbohydrates"]
                daily_totals["fat"] += food["Fats"]
                daily_totals["fiber"] += food["Fibre"]
                daily_totals["calories"] += food["Calories"]
                meal_calories += food["Calories"]

            daily_totals["meal_calories"][meal] = meal_calories

        # Add to weekly totals
        nutritional_totals["weekly"]["protein"] += daily_totals["protein"]
        nutritional_totals["weekly"]["carbs"] += daily_totals["carbs"]
        nutritional_totals["weekly"]["fat"] += daily_totals["fat"]
        nutritional_totals["weekly"]["fiber"] += daily_totals["fiber"]
        nutritional_totals["weekly"]["calories"] += daily_totals["calories"]

        # Store daily totals
        nutritional_totals["daily"][day] = daily_totals

    # Calculate daily averages
    nutritional_totals["daily_average"] = {
        "protein": round(nutritional_totals["weekly"]["protein"] / 7, 1),
        "carbs": round(nutritional_totals["weekly"]["carbs"] / 7, 1),
        "fat": round(nutritional_totals["weekly"]["fat"] / 7, 1),
        "fiber": round(nutritional_totals["weekly"]["fiber"] / 7, 1),
        "calories": round(nutritional_totals["weekly"]["calories"] / 7),
    }

    return nutritional_totals


@app.route("/")
def index():
    session.clear()
    return render_template("index.html")


@app.route("/calculate_bmi", methods=["POST"])
def calculate_bmi_route():
    data = request.get_json()
    weight = float(data.get("weight", 0))
    height = float(data.get("height", 0))

    if weight <= 0 or height <= 0:
        return jsonify({"error": "Weight and height must be positive values"}), 400

    bmi = calculate_bmi(weight, height)
    return jsonify({"bmi": bmi})


@app.route("/generate_weekly_plan", methods=["POST"])
def generate_weekly_plan_route():
    try:
        data = request.get_json()

        # Extract user data
        age = int(data.get("age", 0))
        weight = float(data.get("weight", 0))
        height = float(data.get("height", 0))
        gender = data.get("gender", "Male")
        activity_level = data.get("activity_level", "Lightly Active")
        goal = data.get("goal", "Weight Loss")

        # Extract preferences
        vegetarian = data.get("vegetarian", False)
        vegan = data.get("vegan", False)
        low_carb = data.get("low_carb", False)
        low_fat = data.get("low_fat", False)
        high_protein = data.get("high_protein", False)
        allergies = data.get("allergies", "")

        # Validate inputs
        if age <= 0 or weight <= 0 or height <= 0:
            return (
                jsonify({"error": "Age, weight, and height must be positive values"}),
                400,
            )

        # Calculate nutrition requirements
        nutrition_req = calculate_calorie_requirements(
            age, weight, height, gender, activity_level, goal
        )

        # Make sure food data is loaded
        global food_data
        if food_data is None:
            load_food_data()

        # Filter foods based on user preferences
        filtered_foods = filter_foods_by_preferences(
            food_data, vegetarian, vegan, low_carb, low_fat, high_protein, allergies
        )

        if filtered_foods.empty:
            return (
                jsonify(
                    {
                        "error": "No foods match your dietary preferences and restrictions. Please adjust your preferences."
                    }
                ),
                400,
            )

        # Score foods
        scored_foods = score_foods(filtered_foods, nutrition_req, goal)

        # Categorize foods by meal type
        categorized_foods = categorize_foods_by_meal(scored_foods)

        # Generate weekly meal plan
        weekly_plan = generate_weekly_meal_plan(categorized_foods, nutrition_req)

        # Calculate nutritional totals
        nutritional_totals = calculate_weekly_nutritional_totals(weekly_plan)

        # Store results in session
        session["nutrition_req"] = nutrition_req
        session["weekly_plan"] = weekly_plan
        session["nutritional_totals"] = nutritional_totals

        # Return the recommendations
        return jsonify(
            {
                "success": True,
                "nutrition_req": nutrition_req,
                "weekly_plan": weekly_plan,
                "nutritional_totals": nutritional_totals,
            }
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/get_visualizations_data")
def get_visualizations_data():
    nutrition_req = session.get("nutrition_req")
    weekly_plan = session.get("weekly_plan")
    nutritional_totals = session.get("nutritional_totals")

    if not nutrition_req or not weekly_plan or not nutritional_totals:
        return (
            jsonify(
                {
                    "error": "No recommendation data available. Generate recommendations first."
                }
            ),
            400,
        )

    # Prepare data for visualizations
    visualization_data = {
        "macros": {
            "labels": ["Protein", "Carbs", "Fat"],
            "values": [
                nutrition_req["protein"] * 4,  # Convert to calories
                nutrition_req["carbs"] * 4,
                nutrition_req["fat"] * 9,
            ],
        },
        "daily_calories": {
            "labels": list(nutritional_totals["daily"].keys()),
            "values": [
                nutritional_totals["daily"][day]["calories"]
                for day in nutritional_totals["daily"]
            ],
        },
        "nutrient_comparison": {
            "nutrients": ["Protein (g)", "Carbs (g)", "Fat (g)", "Fiber (g)"],
            "recommended": [
                nutrition_req["protein"] * 7,  # Weekly recommendations
                nutrition_req["carbs"] * 7,
                nutrition_req["fat"] * 7,
                nutrition_req["fiber"] * 7,
            ],
            "actual": [
                nutritional_totals["weekly"]["protein"],
                nutritional_totals["weekly"]["carbs"],
                nutritional_totals["weekly"]["fat"],
                nutritional_totals["weekly"]["fiber"],
            ],
        },
        "daily_distribution": {
            "days": list(nutritional_totals["daily"].keys()),
            "meal_types": ["breakfast", "lunch", "dinner", "snacks"],
            "values": [
                [
                    nutritional_totals["daily"][day]["meal_calories"]["breakfast"]
                    for day in nutritional_totals["daily"]
                ],
                [
                    nutritional_totals["daily"][day]["meal_calories"]["lunch"]
                    for day in nutritional_totals["daily"]
                ],
                [
                    nutritional_totals["daily"][day]["meal_calories"]["dinner"]
                    for day in nutritional_totals["daily"]
                ],
                [
                    nutritional_totals["daily"][day]["meal_calories"]["snacks"]
                    for day in nutritional_totals["daily"]
                ],
            ],
        },
    }

    return jsonify(visualization_data)


if __name__ == "__main__":
    load_food_data()
    app.run(debug=True)
