## Blaseball Bet Odds Optimizer ##
import math
import numpy
import sys

# Parameter setup
gameOdds = [] 
coins = 96
currentMaxBet = 60
EVMode = True

# total arguments
n = len(sys.argv)

if (n==13):
    for i in range(1, 11):
        gameOdds.append(int(sys.argv[i]))
    coins = int(sys.argv[11])
    currentMaxBet = int(sys.argv[12])
else:
    print("Needs 10 odds, 1 coins, and 1 currentMaxBet = 12 args. Defaulting to input")

    for i in range(1, 11):
        gameOdds.append(int(input(f"Enter winning odds for game {i}: ")))

    coins = int(input("Enter current coins: "))
    currentMaxBet = int(input("Enter current max bet: "))

# Pre-Allocating Arrays
gameOddsEV = ['0'] * len(gameOdds)
gameBetsSortedBeg = ['0'] * len(gameOdds)
gameBets = ['0'] * len(gameOdds)
totalCoins = coins
minBet = 0 # Used when EV mode set to False

# Determine game-set bet order, so high games get max bid
gameOrder = numpy.argsort(gameOdds)
gameOrder = gameOrder[::-1]
gameSorted = sorted(gameOdds)

if EVMode == False:
    HighRank = 70
    # Determining bet amounts here
    logCoEf = (1 - minBet)/(math.log1p(HighRank-50))
    print("Log Co-Efficient: " + str(logCoEf))
    for index in range(0,len(gameOdds)):
        gameBets[index] = math.floor( currentMaxBet * ((logCoEf*math.log1p(gameOdds[index] - 50)) + minBet))
        if gameBets[index] > currentMaxBet:
            gameBets[index] = currentMaxBet
    gameBetsSorted = sorted(gameBets, reverse = True)

if EVMode == True:
    EVmax = (2 - (355*10**-6)*(math.pow((100*(0.77-0.5)), 2.045)))*(0.77) - 1
    EVmin = 0
    EVrange = EVmax - EVmin
    for index in range(0,len(gameOdds)):
        gameOddsEV[index] = (2 - (355*10**-6)*(math.pow((100*(gameOdds[index]/100 - 0.5)), 2.045)))*(gameOdds[index]/100) - 1
        gameBets[index] = math.floor(currentMaxBet*(gameOddsEV[index]/EVrange))
        if gameBets[index] > currentMaxBet:
            gameBets[index] = currentMaxBet
    gameBetsSorted = sorted(gameBets, reverse = True)

for index in range(0, len(gameOdds)):
    if totalCoins < gameBetsSorted[index]:
        gameBetsSortedBeg[index] = totalCoins
        gameBetsSorted[index] = totalCoins
    if (totalCoins) <= 0:
        gameBetsSortedBeg[index] = 'Beg'
    totalCoins -= gameBetsSorted[index]
    #print('Total coins is now: ' + str(totalCoins))

# Output   
print('\nGame\tOdds\tBet')
print('|||||||||||||||||||')
for index in range(0,len(gameOdds)):
    if gameBetsSortedBeg[index] == 'Beg':
        gameBetsSorted[index] = gameBetsSortedBeg[index]
        print(f"{gameOrder[index] + 1}" +"\t"+ f"{gameOdds[gameOrder[index]]}" + '\t' + f"{gameBetsSorted[index]}")
    else:
        print(f"{gameOrder[index] + 1}" +"\t"+ f"{gameOdds[gameOrder[index]]}" + '\t' + f"{gameBetsSorted[index]}")