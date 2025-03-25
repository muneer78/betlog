import random
from time import sleep

first = [2048*['Pistons']]
second = [1024*['Magic']]
third = [512*['Thunder']]
fourth = [256*['Pelicans']]
fifth = [128*['Rockets']]
sixth = [64*['Spurs']]
seventh = [32*['Blazers']]
eighth = [16*['Pacers']]
ninth = [8*['Knicks']]
tenth = [4*['Wolves']]
eleventh = [2*['Kings']]
twelfth = [1*['Raptors']]

total = []

for i in first:
    for x in i:
        total.append(x)

for i in second:
    for x in i:
        total.append(x)

for i in third:
    for x in i:
        total.append(x)

for i in fourth:
    for x in i:
        total.append(x)

for i in fifth:
    for x in i:
        total.append(x)

for i in sixth:
    for x in i:
        total.append(x)

for i in seventh:
    for x in i:
        total.append(x)

for i in eighth:
    for x in i:
        total.append(x)

for i in ninth:
    for x in i:
        total.append(x)

for i in tenth:
    for x in i:
        total.append(x)

for i in eleventh:
    for x in i:
        total.append(x)

for i in twelfth:
    for x in i:
        total.append(x)

random.shuffle(total)

order = []
for i in total:
    if i not in order:
        order.append(i)

print('the twelfth pick goes to {}'.format(order[11]))
sleep(1)
print('the eleventh pick goes to {}'.format(order[10]))
sleep(1)
print('the tenth pick goes to {}'.format(order[9]))
sleep(1)
print('the ninth pick goes to {}'.format(order[8]))
sleep(1)
print('the eighth pick goes to {}'.format(order[7]))
sleep(1)
print('the seventh pick goes to {}'.format(order[6]))
sleep(2)
print('the sixth pick goes to {}'.format(order[5]))
sleep(2)
print('the fifth pick goes to {}'.format(order[4]))
sleep(2)
print('the fourth pick goes to {}'.format(order[3]))
sleep(3)
print('the third pick goes to {}'.format(order[2]))
sleep(3)
print('the second pick goes to {}'.format(order[1]))
sleep(3)
print('the first pick goes to {}'.format(order[0]))