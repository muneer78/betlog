amount = float(input('How much is at stake?\n'))
odds = int(input('What are the odds?\n'))

cleaned_odds = abs(odds)

winnings = round(((cleaned_odds / 100) * amount) if odds > 0 else ((100 / cleaned_odds) * amount), 2)
win_str = str(winnings)

implied_probability = round((100 / (100 + cleaned_odds)) if odds > 0 else (cleaned_odds / (100 + cleaned_odds)), 2)
implied_probability_100 = implied_probability *100
implied_probability_str = str(implied_probability_100)

ev = round((implied_probability * winnings) - ((1 - implied_probability) * amount), 2)
str_ev = str(ev)

print("If I win, I'll make a profit of $" + win_str + ".")
print("My chances of winning are " + implied_probability_str + "%.")
print("The expected Value of this bet is $" + str_ev +".")
