import pandas as pd

# Data
data = {
    'Point Spread': [1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6, 6.5, 7, 7.5, 8, 8.5, 9, 9.5, 10, 10.5, 11, 11.5, 12, 12.5, 13, 13.5, 14, 14.5, 15, 15.5, 16, 16.5, 17, 17.5, 18, 18.5, 19, 19.5, 20],
    'Moneyline For Favorite': [116, 123, 130, 137, 170, 197, 210, 222, 237, 252, 277, 299, 335, 368, 397, 427, 441, 456, 510, 561, 595, 631, 657, 681, 730, 781, 904, 1024, 1086, 1147, 1223, 1300, 1418, 1520, 1664, 1803, 1985, 2182, 2390],
    'Moneyline For Underdog': [-104, 102, 108, 113, 141, 163, 174, 184, 196, 208, 229, 247, 277, 305, 328, 353, 365, 377, 422, 464, 492, 522, 543, 564, 604, 646, 748, 847, 898, 949, 1012, 1076, 1173, 1257, 1377, 1492, 1642, 1805, 1977]
}

df = pd.DataFrame(data)

# Allow user input of point spread
user_point_spread = float(input("Enter the Point Spread: "))

# Allow user input of bet price
user_bet_price = int(input("Enter the Bet Price: "))

# Allow user to enter F for favorite or U for underdog
user_choice = input("Enter 'F' for Favorite or 'U' for Underdog: ").strip().upper()

# Do closest match for point spread
nearest_point_spread = df.iloc[(df['Point Spread'] - user_point_spread).abs().idxmin()]

# Determine the moneyline value based on user choice
if user_choice == 'F':
    moneyline_value = nearest_point_spread['Moneyline For Favorite']
elif user_choice == 'U':
    moneyline_value = nearest_point_spread['Moneyline For Underdog']
else:
    print("Invalid choice. Please enter 'F' or 'U'.")
    exit()

# Determine if it's a bet or not
if user_bet_price > moneyline_value:
    print("Bet moneyline")
else:
    print("Bet spread")
