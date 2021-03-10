## Blaseball Bet Odds Optimizer ##
import math
import numpy
import sys
import sseclient
import json
import requests

# Parameter setup
gameOdds = []
gameOddNumbers = []
coins = 96
currentMaxBet = 60
EVMode = True

# Gather the game odds from the current game state
def get_data():
    url = 'https://www.blaseball.com/events/streamData'
    headers = {'Accept': 'text/event-stream'}
    response = requests.get(url, stream=True, headers=headers)
    client = sseclient.SSEClient(response)
    for event in client.events():
        return json.loads(event.data)

data = get_data()

for day in data["value"]["games"]["tomorrowSchedule"]:

    better_odds = 0.3
    better_team = "Team Name"

    if day["awayOdds"]>day["homeOdds"]:
        better_odds = day["awayOdds"]
        better_team = day["awayTeamNickname"]
    else:
        better_odds = day["homeOdds"]
        better_team = day["homeTeamNickname"]

    better_touple = (round(better_odds * 100), better_team)

    gameOddNumbers.append(round(better_odds * 100))
    gameOdds.append(better_touple)

# total arguments
n = len(sys.argv)

if (n==3):
    coins = int(sys.argv[1])
    currentMaxBet = int(sys.argv[2])
else:
    print("No/improper command line arguments detected. Switching to user input")

    coins = int(input("Enter current coins: "))
    currentMaxBet = int(input("Enter current max bet: "))

# Pre-Allocating Arrays
gameOddsEV = ['0'] * len(gameOdds)
gameBetsSortedBeg = ['0'] * len(gameOdds)
gameBets = ['0'] * len(gameOdds)
totalCoins = coins
minBet = 0 # Used when EV mode set to False

# Determine game-set bet order, so high games get max bid
gameOrder = numpy.argsort(gameOddNumbers)
gameOrder = gameOrder[::-1]
gameSorted = sorted(gameOdds)

if EVMode == False:
    HighRank = 70
    # Determining bet amounts here
    logCoEf = (1 - minBet)/(math.log1p(HighRank-50))
    print("Log Co-Efficient: " + str(logCoEf))
    for index in range(0,len(gameOdds)):
        gameBets[index] = math.floor( currentMaxBet * ((logCoEf*math.log1p(gameOdds[index][0] - 50)) + minBet))
        if gameBets[index] > currentMaxBet:
            gameBets[index] = currentMaxBet
    gameBetsSorted = sorted(gameBets, reverse = True)

if EVMode == True:
    EVmax = (2 - (355*10**-6)*(math.pow((100*(0.77-0.5)), 2.045)))*(0.77) - 1
    EVmin = 0
    EVrange = EVmax - EVmin
    for index in range(0,len(gameOdds)):
        gameOddsEV[index] = (2 - (355*10**-6)*(math.pow((100*(gameOdds[index][0]/100 - 0.5)), 2.045)))*(gameOdds[index][0]/100) - 1
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
print('\nGame\tOdds\t\t\tBet')
print('||||||||||||||||||||||||||||||||||||')
for index in range(0,len(gameOdds)):
    if gameBetsSortedBeg[index] == 'Beg':
        gameBetsSorted[index] = gameBetsSortedBeg[index]

    print("{:<8}{:<24}{}".format(gameOrder[index] + 1, str(gameOdds[gameOrder[index]]), gameBetsSorted[index]))