from pulp import LpProblem, LpMaximize, LpVariable, LpStatus

# Create a linear programming problem
prob = LpProblem("Maximize_Size", LpMaximize)

# Define variables: number of items of each type to buy
item_1 = LpVariable("Smallest Bet", lowBound=9, cat="Integer")
item_2 = LpVariable("Medium Bet", lowBound=10, cat="Integer")
item_3 = LpVariable(
    "Largest Bet",
    lowBound=11,
    cat="Integer")  # No lower bound for item_3

# Define prices and budget
prices = [1, 1, 1]
budget = 50  # Increase the budget to make it feasible

# Define the individual objectives for each item
objective_item_1 = item_1
objective_item_2 = item_2
objective_item_3 = item_3

# Define the constraint: total cost should equal the budget
prob += prices[0] * item_1 + prices[1] * item_2 + \
    prices[2] * item_3 == budget, "Budget_Constraint"

# Ensure that the remaining budget is non-negative
remaining_budget = budget - (
    (prices[0] * item_1 if item_1.varValue is not None else 0) +
    (prices[1] * item_2 if item_2.varValue is not None else 0) +
    (prices[2] * item_3 if item_3.varValue is not None else 0)
)
prob += remaining_budget >= 0, "Non_Negative_Budget"

# Solve the problem
prob.solve()

# Calculate the total cost of the purchased items
total_cost = (
    (prices[0] * item_1.varValue if item_1.varValue is not None else 0) +
    (prices[1] * item_2.varValue if item_2.varValue is not None else 0) +
    (prices[2] * item_3.varValue if item_3.varValue is not None else 0)
)

# Calculate the remaining budget
remaining_budget = budget - total_cost
remaining_budget_rounded = round(remaining_budget, 2)

# Print the results
print("Status:", LpStatus[prob.status])
print("Smallest Bet:", item_1.varValue)
print("Medium Bet:", item_2.varValue)
print("Largest Bet:", item_3.varValue)
print("Remaining budget:", remaining_budget_rounded)
