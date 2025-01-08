import math


### Chip breakdown function ###
def chipBreakdown(bigBlind0, noPlayers, buyIn0):
    buyIn = round(buyIn0 * 100)
    bigBlind = round(bigBlind0 * 100)

    ### No. chips ###
    no5c = 100
    no25c = 100
    no1 = 100
    no5 = 100
    no25 = 100
    no100 = 75
    no500 = 25

    ### Max possible chips per player###
    no5cPoss = int(no5c / noPlayers)
    no25cPoss = int(no25c / noPlayers)
    no1Poss = int(no1 / noPlayers)
    no5Poss = int(no5 / noPlayers)
    no25Poss = int(no25 / noPlayers)
    no100Poss = int(no100 / noPlayers)
    no500Poss = int(no500 / noPlayers)

    ### Chip number filter ###
    chipVal = [5, 25, 100, 500, 2500, 10000, 50000]
    chipsNo = [0, 0, 0, 0, 0, 0, 0]
    chipNoPoss = [no5cPoss, no25cPoss, no1Poss, no5Poss, no25Poss, no100Poss, no500Poss]
    sum = buyIn
    for i in range(7):
        if sum > 0:
            if chipVal[i] >= bigBlind / 2:
                while (sum - chipNoPoss[i] * chipVal[i]) < 0:
                    chipNoPoss[i] = chipNoPoss[i] - 1
                chipsNo[i] = chipNoPoss[i]

                if chipVal[i] != 50000 and (sum - chipNoPoss[i] * chipVal[i]) != 0:
                    while (sum - chipNoPoss[i] * chipVal[i]) % chipVal[i + 1] != 0:
                        chipNoPoss[i] = chipNoPoss[i] - 1
                    chipsNo[i] = chipNoPoss[i]

                sum = sum - chipVal[i] * chipsNo[i]
    return chipsNo


### Chip name list ###
chipName = ["5¢", "25¢", "$1", "$5", "$25", "$100", "$500"]

### Game info ###
print("** Poker Chip Breakdown Calculator **")
print()
noPlayers = eval(input("No. players: "))
bigBlind = eval(input("Big blind [$]: "))
print()

### Print chip breakdown ###
while True:
    buyIn = eval(input(("Buy in [$]: ")))
    breakdown = chipBreakdown(bigBlind, noPlayers, buyIn)
    for i in range(len(breakdown)):
        if breakdown[i] != 0:
            print(chipName[i] + ": " + str(breakdown[i]))
    totalChips = sum(breakdown)
    print("Total chips: " + str(totalChips))
    print()