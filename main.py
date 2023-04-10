import tkinter as tk
from tkinter import ttk

from athlete import Athlete

# Training plans with corresponding prices in GBP
TRAINING_PLANS = {
    "Beginner (2 sessions per week)": 25.00,
    "Intermediate (3 sessions per week)": 30.00,
    "Elite (5 sessions per week)": 35.00,
}

# Weight categories with upper weight limit in kg
WEIGHT_CATEGORIES = {
    "Heavyweight - Unlimited (Over 100)": float('inf'),
    "Light-Heavyweight - 100": 100,
    "Middleweight - 90": 90,
    "Light-Middleweight - 81": 81,
    "Lightweight - 73": 73,
    "Flyweight - 66": 66
}


def submit():
    athlete = Athlete(
        name=name_entry.get(),
        training_plan=plan_combo.get(),
        current_weight=weight_entry.get(),
        competition_category=category_combo.get(),
        competitions_this_month=competitions_entry.get(),
        private_coaching_hours=coaching_entry.get()
    )

    try:
        if len(athlete.name) == 0:
            raise ValueError("Athlete name can't be empty")

        if len(athlete.training_plan) == 0:
            raise ValueError("Select a training plan")

        if len(athlete.current_weight) == 0:
            raise ValueError("Current weight can't be empty")

        if len(athlete.competition_category) == 0:
            raise ValueError("Select a competition category")

        if len(athlete.competitions_this_month) == 0:
            raise ValueError("Select this month competitions value")

        if int(athlete.competitions_this_month) > 0 and athlete.training_plan == "Beginner (2 sessions per week)":
            raise ValueError("Only Intermediate and Elite athletes can enter competitions")

        if len(athlete.private_coaching_hours) == 0:
            raise ValueError("Private coaching hours can't be empty")

        if int(athlete.private_coaching_hours) > 20:
            raise ValueError("You can receive a maximum of 20 hours’ private coaching a month")

        # Calculate total costs
        total_cost = 0
        costs_list = []
        if athlete.training_plan in TRAINING_PLANS:
            training_cost = TRAINING_PLANS[athlete.training_plan] * 4
            total_cost += training_cost
            costs_list.append(f"Training Plan ({athlete.training_plan}): £{training_cost:.2f}")
        if athlete.competitions_this_month:
            competition_cost = float(athlete.competitions_this_month) * 22.00
            total_cost += competition_cost
            costs_list.append(f"Competitions This Month: £{competition_cost:.2f}")
        if athlete.private_coaching_hours:
            coaching_cost = float(athlete.private_coaching_hours) * 9.50
            total_cost += coaching_cost
            costs_list.append(f"Private Coaching Hours: £{coaching_cost:.2f}")

        # Compare current weight with competition weight category
        weight_comparison = ""
        if float(athlete.current_weight) and athlete.competition_category:
            if athlete.competition_category == "Heavyweight - Unlimited (Over 100)":
                if float(athlete.current_weight) > 100:
                    weight_comparison = "Equal"
                else:
                    weight_comparison = "Below"
            elif float(athlete.current_weight) > WEIGHT_CATEGORIES[athlete.competition_category]:
                weight_comparison = "Above"
            elif float(athlete.current_weight) < WEIGHT_CATEGORIES[athlete.competition_category]:
                weight_comparison = "Below"
            else:
                weight_comparison = "Equal"

        # Display the calculated information in the result_label
        result_label.config(text=f"Athlete's Name: {athlete.name}\n"
                                 f"Cost Breakdown:\n"
                                 f"{', '.join(costs_list)}\n"
                                 f"Total Cost: £{total_cost:.2f}\n"
                                 f"Weight Comparison: {weight_comparison} competition category")
    except ValueError as e:
        # Display error message to the user
        message_label.config(text=f"Error: {str(e)}. Please enter valid input.")


# Validation function for weight entry
def validate_weight(char, value):
    if char.isdigit() or char == ".":
        try:
            float(value + char)
            return True
        except ValueError:
            return False
    else:
        return False


# Validation function for competitions entry
def validate_competitions(char):
    if char.isdigit():
        return True
    else:
        return False


# Validation function for coaching entry
def validate_coaching(char):
    if char.isdigit():
        return True
    else:
        return False


root = tk.Tk()
root.title("North Sussex Judo")
root.geometry("800x600")

# Athlete Name Entry
name_label = tk.Label(root, text="Athlete Name:")
name_label.pack()
name_entry = tk.Entry(root)
name_entry.pack()

# Training Plan Selection
plan_label = tk.Label(root, text="Training Plan:")
plan_label.pack()
plan_combo = ttk.Combobox(root, values=list(TRAINING_PLANS.keys()), state="readonly")  # Set state to readonly
plan_combo.pack()

# Current Weight Entry
weight_label = tk.Label(root, text="Current Weight (kg):")
weight_label.pack()
weight_entry = tk.Entry(root, validate="key", validatecommand=(root.register(validate_weight), "%S", "%P"))
weight_entry.pack()

# Competition Category Selection
category_label = tk.Label(root, text="Competition Category:")
category_label.pack()
category_combo = ttk.Combobox(root, values=list(WEIGHT_CATEGORIES.keys()), state="readonly")  # Set state to readonly
category_combo.pack()

# Competitions This Month Entry
competitions_label = tk.Label(root, text="Competitions This Month:")
competitions_label.pack()
competitions_entry = tk.Entry(root, validate="key", validatecommand=(root.register(validate_competitions), "%S"))
competitions_entry.pack()

# Private Coaching Hours Entry
coaching_label = tk.Label(root, text="Private Coaching Hours:")
coaching_label.pack()
coaching_entry = tk.Entry(root, validate="key", validatecommand=(root.register(validate_coaching), "%S"))
coaching_entry.pack()

# Message Label
message_label = tk.Label(root, text="")
message_label.pack()

# Submit Button
submit_button = tk.Button(root, text="Submit", command=submit)
submit_button.pack()

# Result Label
result_label = tk.Label(root, text="")
result_label.pack()

root.mainloop()
