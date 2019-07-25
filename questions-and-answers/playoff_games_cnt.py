"""
Question:
given the number of NBA playoff games a team played in a season,
can we (if yes, how to) determine which rounds(R1, CSF, CF, F) the team advanced to?
"""

N = 4  # the number of rounds (N = 4 in NBA)

# games_cnt[i] = a list of all possible number of games a team plays up to round i (1 <= i <= N)
games_cnt = [[j for j in range(4 * i, 7 * i + 1)] for i in range(N + 2)]

for i in range(1, N + 1):
    for j in range(len(games_cnt[i])):
        # R1 (no rounds before)
        if i == 1 and (games_cnt[i][j] not in games_cnt[i + 1]):
            print(games_cnt[i][j], end="\t")
        # F (no rounds after)
        elif i == N and (games_cnt[i][j] not in games_cnt[i - 1]):
            print(games_cnt[i][j], end="\t")
        # CSF, CF (have rounds before and after)
        elif (games_cnt[i][j] not in games_cnt[i - 1]) and (games_cnt[i][j] not in games_cnt[i + 1]):
            print(games_cnt[i][j], end="\t")
        else:
            print("-", end="\t")
    print()
print()

"""
such number x exists when
max # of games up to the previous round < x < min # of games up to the next round

we also know that x won't exist after round 3 because: let i be the i-th round, 
if 7*(i-1) < 4*(i+1) then i < 11/3 < 4 (but in NBA there is no such restriction for round 4 (final))
"""
for i in range(1, N + 1):
    for x in range(4 * i, 7 * i + 1):
        # R1 (no rounds before)
        if i == 1 and x < 4 * (i + 1):
            print(x, end=", ")
        # F (no rounds after)
        elif i == N and x > 7 * (i - 1):
            print(x, end=", ")
        # CSF, CF (have rounds before and after)
        elif 7 * (i - 1) < x < 4 * (i + 1):
            print(x, end=", ")
