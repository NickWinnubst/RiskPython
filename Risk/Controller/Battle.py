import random


# simulate a single attack with attackers and defenders
# return: [dice lost by attacker, dice lost by defender]
def attack(attackers, defenders):
    if attackers <= 0 or defenders <= 0 or attackers > 3 or defenders > 2:
        return [0,0]

    score = list([0,0])

    attacker_dice = throw_dice(attackers)
    defender_dice = throw_dice(defenders)

    for x in range(0,min(attackers,defenders)):
        score = [a+b for [a,b] in zip(score,compare_dice(attacker_dice[x], defender_dice[x]))]

    return score, attacker_dice, defender_dice


# compare dice to determine a score
# return: [dice lost by attacker, dice lost by defender]
def compare_dice(attacker_die, defender_die):
    if attacker_die > defender_die:
        return list([0,1])
    return list([1,0])


# throw a given amount of dice
def throw_dice(amount):
    dice = []
    for i in range(1,amount+1):
        dice.append(random.randint(1,6))

    return sorted(dice, reverse=True)