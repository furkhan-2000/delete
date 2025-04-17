from flask import Flask, render_template, request, flash, redirect, url_for

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Exercises Data
EXERCISES = {
    "beginner": {
        "Cardio": "Walking, cycling, or low-impact aerobics (e.g., 15–20 mins daily)",
        "Strength": "Bodyweight squats, wall push-ups, and beginner planks",
        "Flexibility": "Easy yoga poses like child's pose, cat-cow stretch",
        "Balance": "Single-leg stands or heel-to-toe walking"
    },
    "intermediate": {
        "Cardio": "Jogging, interval running, or moderate swimming",
        "Strength": "Regular push-ups, lunges, and dumbbell routines",
        "Flexibility": "Sun salutations or deeper stretches",
        "Balance": "Stability ball exercises and one-leg yoga poses like Tree Pose"
    },
    "advanced": {
        "Cardio": "High-intensity interval training (HIIT) or long-distance running",
        "Strength": "Weighted squats, deadlifts, and advanced plyometrics (e.g., jump lunges)",
        "Flexibility": "Dynamic stretches and advanced yoga flows",
        "Balance": "Bosu ball squats or advanced poses like Crow Pose"
    }
}

# Default Diet Plan (fallback if no conditions match)
DEFAULT_DIET_PLAN = {
    "Morning": "Warm lemon water (upon waking)",
    "Breakfast": "Oatmeal with berries and a boiled egg",
    "Mid-Morning Snack": "A piece of fruit or a handful of nuts",
    "Lunch": "Rice (brown/regular) with dal, 205gm boiled chicken curry, buttermilk, spoon of curd",
    "Afternoon Snack": "Roasted chickpeas",
    "Pre-Workout Snack": "Banana shake with dates and peanut butter",
    "Post-Workout Snack": "1 scoop of whey protein, boiled egg",
    "Dinner": "1 chapati with vegetable curry or dal, small side salad"
}

# Diet Plans for Beginner, Intermediate, and Advanced Levels
def get_diet_plan(weight, level):
    diet_plans = {
        "beginner": {
            (40, 60): {
                "Morning": "Warm lemon water (upon waking)",
                "Breakfast": "3 egg whites with whole-wheat toast and a seasonal fruit",
                "Mid-Morning Snack": "A piece of fruit or a handful of nuts",
                "Lunch": "Rice (brown/regular) with dal, 205gm boiled chicken curry, buttermilk, spoon of curd",
                "Afternoon Snack": "Roasted chickpeas",
                "Pre-Workout Snack": "Banana shake with dates and peanut butter",
                "Post-Workout Snack": "1 scoop of whey protein, boiled egg",
                "Dinner": "1 chapati with vegetable curry or dal, small side salad"
            },
            (61, 85): {
                "Hydration (6:30–7:00 AM)": "Warm lemon water",
                "Breakfast (7:30–8:00 AM)": "Oats with fruits and seeds or upma or boiled eggs",
                "Snack (10:00–10:30 AM)": "Fruit and nuts",
                "Lunch (12:30–1:00 PM)": "Carbs (rice/quinoa), protein (paneer/chicken), salad (fresh veggies)",
                "Snack (3:30–4:00 PM)": "Yogurt with berries or sprouts salad",
                "Pre-Workout (5:30–6:00 PM)": "Banana or smoothie (banana, spinach)",
                "Dinner (7:30–8:00 PM)": "Chapatis with curry and dal or grilled fish/chicken, veggies, quinoa/millets",
                "Optional (9:00 PM)": "Herbal tea"
            },
            (86, 120): {
                "Hydration (6:30–7:00 AM)": "Warm lemon water with ginger (optional for added digestive benefits)",
                "Breakfast (7:30–8:00 AM)": "Veggie omelet (eggs, spinach, tomatoes, mushrooms) with avocado slices or unsweetened Greek yogurt with chia seeds",
                "Snack (10:00–10:30 AM)": "Greek yogurt with a sprinkle of flax seeds or a few almonds",
                "Lunch (12:30–1:00 PM)": "Grilled chicken salad (mixed greens, cucumbers, bell peppers, tomatoes, olive oil lemon dressing), side of steamed broccoli",
                "Snack (3:30–4:00 PM)": "Cottage cheese with celery or cucumber sticks",
                "Pre-Workout (5:30–6:00 PM)": "Protein shake (whey protein, almond milk, spinach, ice)",
                "Dinner (7:30–8:00 PM)": "Baked salmon with steamed asparagus and sautéed spinach or grilled turkey breast with cauliflower rice and mixed green salad",
                "Optional (9:00 PM)": "Herbal tea (chamomile or peppermint) for improved digestion and relaxation"
            }
        },
        "intermediate": {
            (40, 60): {
                "Before-Breakfast": "1 glass of warm water with lemon to kickstart metabolism and hydrate",
                "Breakfast": "1 cup oatmeal with mixed berries, 1 scoop whey protein mixed in unsweetened almond milk",
                "Mid-Morning Snack": "Greek yogurt drizzled with a little honey and a small handful of nuts",
                "Lunch": "Grilled chicken (or tofu) salad with mixed greens, cherry tomatoes, and cucumber dressed lightly with vinaigrette, side of quinoa or brown rice",
                "Afternoon Snack": "1 banana and 10–12 almonds",
                "Pre-Workout Snack": "Light protein shake (water or almond milk based) or small piece of fruit",
                "Post-Workout Snack": "Recovery protein shake (optionally blended with a fast-digesting carbohydrate)",
                "Dinner": "Baked salmon (or a hearty lentil stew), steamed broccoli and roasted sweet potato"
            },
            (61, 85): {
                "Before-Breakfast": "1 glass of water with lemon",
                "Breakfast": "2 slices whole-grain toast topped with mashed avocado and 2 eggs, small serving of fruit salad",
                "Mid-Morning Snack": "Cottage cheese with mixed berries",
                "Lunch": "Lean turkey (or grilled paneer), generous serving of brown rice or whole wheat pasta, steamed mixed vegetables (e.g., broccoli, carrots, zucchini)",
                "Afternoon Snack": "Protein bar or small smoothie (banana, spinach, protein powder)",
                "Pre-Workout Snack": "Rice cakes with a spread of almond butter",
                "Post-Workout Snack": "Smoothie combining banana, protein powder, and spinach",
                "Dinner": "Grilled lean beef (or chickpea curry), side of whole-grain roti or quinoa, fresh salad with olive oil dressing"
            },
            (86, 120): {
                "Before-Breakfast": "A glass of warm water with lemon",
                "Breakfast": "3 egg omelette with spinach, mushrooms, and tomatoes, 2 slices of whole-grain bread, 1 piece of fruit (apple or banana)",
                "Mid-Morning Snack": "Protein shake and a handful of walnuts",
                "Lunch": "Larger serving of grilled chicken or tofu, brown rice or quinoa, generous portion of steamed or roasted mixed vegetables",
                "Afternoon Snack": "Greek yogurt mixed with granola and berries",
                "Pre-Workout Snack": "Smoothie with banana, mixed berries, spinach, and protein powder",
                "Post-Workout Snack": "Recovery shake (protein combined with fast-digesting carbs) plus a piece of fruit",
                "Dinner": "Baked fish (or well-spiced legume-based stew), sweet potato or whole-grain pasta, mixed greens salad"
            }
        },
        "advanced": {
            (40, 60): {
                "Before-Breakfast": "1 glass of water with lemon",
                "Breakfast": "Egg white omelette with spinach and bell peppers, 1–2 slices of whole-grain toast, bowl of oatmeal mixed with a scoop of protein powder",
                "Mid-Morning Snack": "Cottage cheese with a handful of berries",
                "Lunch": "Grilled chicken or fish with a large serving of mixed vegetables, moderate portion of sweet potato or brown rice",
                "Afternoon Snack": "Small handful of nuts or an apple",
                "Pre-Workout Snack": "Banana paired with a few almonds",
                "Post-Workout Snack": "Protein shake blended with a small amount of dextrose (or another fast carbohydrate)",
                "Dinner": "Turkey breast or lean fish, steamed broccoli and a serving of quinoa"
            },
            (61, 85): {
                "Before-Breakfast": "1 glass of water with lemon",
                "Breakfast": "Protein smoothie (whey protein, banana, spinach, almond milk), 2 slices of whole-grain toast with natural peanut butter",
                "Mid-Morning Snack": "Greek yogurt with a sprinkle of granola",
                "Lunch": "Grilled lean meat (chicken or turkey) or tofu stir-fry, large serving of quinoa or brown rice with mixed vegetables",
                "Afternoon Snack": "Protein bar or a serving of fruit",
                "Pre-Workout Snack": "Rice cakes topped with almond butter",
                "Post-Workout Snack": "Recovery shake with protein and a carbohydrate source (such as fruit or oats)",
                "Dinner": "Salmon or lean beef, sweet potato and a large green salad (add avocado slices for healthy fats)"
            },
            (86, 120): {
                "Before-Breakfast": "1 glass of water with lemon",
                "Breakfast": "Large bowl of oatmeal mixed with whey protein, topped with nuts and berries, 3 egg omelette with a variety of vegetables",
                "Mid-Morning Snack": "Protein bar and a piece of fruit",
                "Lunch": "Double portion of lean protein (chicken, turkey, or fish), generous serving of brown rice or whole-grain pasta, large mixed vegetable salad dressed with olive oil",
                "Afternoon Snack": "Small fruit serving or another light protein-based snack",
                "Pre-Workout Snack": "Smoothie with banana, mixed berries, spinach, and protein powder",
                "Post-Workout Snack": "Recovery shake containing fast-digesting carbohydrates and protein",
                "Dinner": "Grilled steak or hearty tofu stir-fry, quinoa or whole-grain pasta, steamed vegetables such as broccoli and carrots"
            }
        }
    }

    for min_weight, max_weight in diet_plans.get(level, {}):
        if min_weight <= weight <= max_weight:
            return diet_plans[level][(min_weight, max_weight)]
    return DEFAULT_DIET_PLAN  # Default if no conditions match

@app.route('/workouts', methods=['GET', 'POST'])
def workouts():
    if request.method == 'POST':
        weight_str = request.form.get('weight')
        selected_level = request.form.get('level')

        if weight_str and selected_level:
            try:
                weight = float(weight_str)
                if selected_level in EXERCISES:
                    exercises = EXERCISES[selected_level]
                    diet_plan = get_diet_plan(weight, selected_level)
                    flash(f'Weight {weight} kg recorded successfully!')
                    return redirect(url_for('workouts', weight=weight, level=selected_level))
                else:
                    flash('Please select a valid workout level.')
            except ValueError:
                flash('Please enter a valid number for weight.')
        else:
            flash('Please enter your weight and select a workout level.')

    weight = request.args.get('weight')
    selected_level = request.args.get('level')
    exercises = EXERCISES.get(selected_level) if selected_level else None
    diet_plan = get_diet_plan(float(weight), selected_level) if weight and selected_level else None

    return render_template('index.html', weight=weight, selected_level=selected_level, exercises=exercises, diet_plan=diet_plan)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)