import pandas as pd
import itertools
import numpy as np
from math import comb, perm, factorial
from sympy.utilities.iterables import multiset_permutations, ordered_partitions
from datetime import date
from matplotlib import pyplot as plt

df = pd.read_csv('https://raw.githubusercontent.com/fivethirtyeight/data/master/births/US_births_1994-2003_CDC_NCHS.csv')
df2 = pd.read_csv('https://raw.githubusercontent.com/fivethirtyeight/data/master/births/US_births_2000-2014_SSA.csv')
df = pd.concat([df, df2[df2['year'] > 2003]])

print(df.head())

# print(df['year'].unique())

means = df.groupby(['month', 'date_of_month'])['births'].mean()

# # print(means[2, 29])

means[2, 29] = means[2, 29] / 4

# # print(means[2])

total = np.sum(means)

# print(total)

dates = [date(2020, d[0], d[1]) for d in list(means.index)]

# # plt.plot(dates, means)
# #
# # plt.show()

probs = {}

for d in means.index:
    probs[d] = means[d] / total

# print(probs)
#
# print(len(probs))

# m = 3
# n = 7

# x = [i for i in range(1, n)]
# y = [perm(i, m) / m**i for i in x]
#
# plt.plot(x, y)
# plt.show()

# print(perm(n, m) / m**n)
#
# letters = 'abcdefghijklmnopqrstuvwxyz'
#
# options = list(letters[0:m])
# uniform_dist = 1 / m
# # probs = [uniform_dist for i in range(m)]
# probs = [.5, .4, .1]
# same = 0
# runs = 100000
# for i in range(runs):
#     selection = set(np.random.choice(options, size=n, p=probs))
#     if len(options) == len(selection):
#         same += 1
#
# print(same)
# print(same / runs)


def get_prob_of_perm(permutation, p):
    total_probability = 1
    for element in permutation:
        total_probability *= p[element]

    return total_probability

# print(get_prob_of_perm([1, 2, 3], {1: .5, 2: .25, 3: .25}))

def create_combinations(elements, n):
    num_elm = len(elements)
    num_perm = len(elements)**n

    num_extra = n - len(elements)

    combos = list(itertools.combinations_with_replacement(elements, num_extra))

    return combos

# create_combinations('abc', 7)

def unique_probability(probs):
    print(probs.keys())
    return get_prob_of_perm(probs.keys(), probs)

def get_perm_count(n, perm):
    total_perm = factorial(n)
    for element in set(perm):
        total_perm = total_perm / factorial(perm.count(element) + 1)

    return total_perm

# print(get_perm_count(5, ['a', 'b']))

# print(unique_probability({1: .5, 2: .4, 3: .1}))

def birthday_probability(n, p:dict):
    prob_of_unique = unique_probability(p)
    print(prob_of_unique)

    print(len(p))

    if n - len(p) < 0:
        return 'error: too small n'
    elif n - len(p) == 0:
        return perm(n, n) * prob_of_unique

    combos = create_combinations(p.keys(), n)
    print(len(combos))
    combo_p = np.zeros(len(combos))

    for i in range(len(combos)):
        combo_p[i] = get_perm_count(n, combos[i]) * prob_of_unique * get_prob_of_perm(combos[i], p)

    return np.sum(combo_p)


# p = {1: .5, 2: .4, 3: .1}
# n = 7

print(birthday_probability(367, probs))