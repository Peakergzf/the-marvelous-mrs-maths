"""
Question:
given the number of NBA playoff games a team played in a season,
can we (if yes, how to) determine which rounds(R1, CSF, CF, F) the team advanced to?


"""

N = 8  # the number of rounds (N = 4 in NBA)

# games_cnt[i] = a list of all possible number of games a team plays up to round i
games_cnt = [[j for j in range(4 * i, 7 * i + 1)] for i in range(N)]

for i in range(1, N - 1):
    for j in range(len(games_cnt[i])):
        # only print unique numbers
        if (games_cnt[i][j] in games_cnt[i - 1]) or (games_cnt[i][j] in games_cnt[i + 1]):
            print("-", end="\t")
        else:
            print(games_cnt[i][j], end="\t")
    print()
print()

"""
such number x exists when
max # of games up to the previous round < x < min # of games up to the next round

we also know that x won't exist after round 3 because: let i be the i-th round, 
if 7*(i-1) < 4*(i+1) then i < 11/3 < 4
"""
for i in range(1, N):
    for x in range(4 * i, 7 * i + 1):
        if 7 * (i - 1) < x < 4 * (i + 1):
            print(x, end=", ")
