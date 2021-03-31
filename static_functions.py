def calculate_mod(ability_score):
    if ability_score == 1:
        return -5
    elif ability_score in (2, 3):
        return -4
    elif ability_score in (4, 5):
        return -3
    elif ability_score in (6, 7):
        return -2
    elif ability_score in (8, 9):
        return -1
    elif ability_score in (10, 11):
        return 0
    elif ability_score in (12, 13):
        return 1
    elif ability_score in (14, 15):
        return 2
    elif ability_score in (16, 17):
        return 3
    elif ability_score in (18, 19):
        return 4
    elif ability_score in (20, 21):
        return 5
    elif ability_score in (22, 23):
        return 6
    elif ability_score in (24, 25):
        return 7
    elif ability_score in (26, 27):
        return 8
    elif ability_score in (28, 29):
        return 9
    elif ability_score == 30:
        return 10
    else:
        return 0
