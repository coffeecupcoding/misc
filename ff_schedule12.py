#!/usr/bin/env python3

# Calculate a 12 team 2 division head-to-head fantasy schedule
# Each team plays division rivals twice and a random set of
#   three teams in the other division
# The order of division matchups is also randomized

# This is the only section that needs to be changed
# Teams 1-6 should be one division, teams 7-12 should be the other

team_list = [
    'team01',
    'team02',
    'team03',
    'team04',
    'team05',
    'team06',
    'team07',
    'team08',
    'team09',
    'team10',
    'team11',
    'team12'
]



# Program

import random

def swap_matchup_week(matchups):
    # swap 'home' and 'away' by reversing the order of the tuple values
    swapped_matchups = []
    for matchup in matchups:
        swapped_matchups.append((matchup[1], matchup[0]))
    return swapped_matchups

def division_2(matchups):
    # Return a matchup list for division 2 (ie. teams 6-11)
    d2_matchups = []
    for matchup in matchups:
        d2_matchups.append((matchup[0] + 6, matchup[1] + 6))
    return d2_matchups

def print_matchups(title, matchup_list):
    # Print out the matchups for a week
    print(title)
    for matchup in matchup_list:
        print("%30s   at   %-30s" % (team_list[(matchup[0])],
            team_list[(matchup[1])]) )

def print_weeks(matchups, start_week, inter=False):
    # print out the set of matchups for each week in matchups
    # returns the next start_week
    for week in range(len(matchups)):
        print("Week %i\n" % start_week)
        if inter:
           print_matchups("Inter-Division", matchups[week])
        else:
            print_matchups("Division 1", matchups[week])
            print_matchups("\nDivision 2", division_2(matchups[week]))
        print("\n")
        start_week += 1
    return start_week


# All possible intradivision weekly schedules
all_weeks = [
    [ [(0,1), (2,3), (4,5)], [(0,1), (2,4), (3,5)], [(0,1), (2,5), (3,4)] ],
    [ [(0,2), (1,4), (3,5)], [(0,2), (1,3), (4,5)], [(0,2), (1,5), (3,4)] ],
    [ [(0,3), (1,5), (2,4)], [(0,3), (1,2), (4,5)], [(0,3), (1,4), (2,5)] ],
    [ [(0,4), (1,3), (2,5)], [(0,4), (1,2), (3,5)], [(0,4), (1,5), (2,3)] ],
    [ [(0,5), (1,2), (3,4)], [(0,5), (1,3), (2,4)], [(0,5), (1,4), (2,3)] ]
]

# All the consistent combinations of weeks
possible_schedules = [
    [ 0, 0, 0, 0, 0 ],
    [ 0, 2, 2, 1, 1 ],
    [ 1, 1, 2, 2, 0 ],
    [ 1, 2, 1, 0, 2 ],
    [ 2, 0, 1, 2, 1 ],
    [ 2, 1, 0, 1, 2 ]
]

# Select the order of the intra-division matchups

# randomly choose a schedule from the possible schedules
x = random.choice(range(6))

# The actual set of matchup weeks chosen
matchup_list = [
    all_weeks[0][possible_schedules[x][0]],
    all_weeks[1][possible_schedules[x][1]],
    all_weeks[2][possible_schedules[x][2]],
    all_weeks[3][possible_schedules[x][3]],
    all_weeks[4][possible_schedules[x][4]]
]

# Now randomize the weeks themselves
early_intra_matchups = random.sample(matchup_list, k=len(matchup_list))

# swap matchup order for the second and fourth week, in case the league
#   uses some form of home field advantage
early_intra_matchups[1] = swap_matchup_week(early_intra_matchups[1])
early_intra_matchups[3] = swap_matchup_week(early_intra_matchups[3])

# Reverse the order and home/away for the last five weeks
late_intra_matchups = [ swap_matchup_week(week) for week in
    reversed(early_intra_matchups) ]

# Choose the inter-division matchups
inter_matchups = []
coin_flip = random.choice(range(1,3))
matchup_order = list(range(6,12))
random.shuffle(matchup_order)
for x in range(3):
    matchups = []
    for y in range(6):
        matchups.append( (y, matchup_order[y]) )
    # Assign the extra home game by division, this attempts to make
    #   schedules more fair within the division
    if ((x + coin_flip) % 2) == 0:
        matchups = swap_matchup_week(matchups)
    inter_matchups.append(matchups)
    # Rotate twice to make it seem more random ;)
    matchup_order.insert(0, matchup_order.pop())
    matchup_order.insert(0, matchup_order.pop())

# Print the matchups by week
season_week = 1
season_week = print_weeks(early_intra_matchups, season_week)
season_week = print_weeks(inter_matchups, season_week, inter=True)
print_weeks(late_intra_matchups, season_week)

