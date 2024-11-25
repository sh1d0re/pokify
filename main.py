USERINPUT = {
    "Calculate Opponent": input("           Calculate for the opponent? [Y/N]: "),
    "Hands": input("  Enter your gaven hands [Split with spaces]: "),
    "River": input("Enter your current river [Split with spaces]: ")
}

from collections import *

deckHands = "23456789TJQKA"
deckSuits = "CDHS"
deckDealer = [i+j for i in deckHands for j in deckSuits]

deckKnownHands = {
    "Hands": USERINPUT["Hands"].split(),
    "River": USERINPUT["River"].split()
}

for i in deckKnownHands["Hands"]: deckDealer.remove(i)
for i in deckKnownHands["River"]: deckDealer.remove(i)

def fixToDigits(length:int, prompt:str, makeUp: str):
    return(prompt+"".join([makeUp for i in range(length-len(prompt))]))

def translateCardNotation(type:str, target:list) -> list:
    if type == 1:
        return([int(str(i[:-1]).replace("A","14").replace("T","10").replace("J","11").replace("Q","12").replace("K","13")) for i in target])
    if type == 2:
        return([str(str(i).replace("14","A").replace("10","T").replace("11","J").replace("12","Q").replace("13","K")) for i in target])
    
ignoreCalculations = []

def checkCurrentHands(givenHands, givenRiver):
    hands = {"Pair": None, "Two Pair": None, "Three Card": None, "Straight": None, "Flush": None, "Full House": None, "Four Of A Kind": None, "Straight Flush": None, "Royal Flush": None}
    givenHandsAndRiver = sorted(givenHands+givenRiver)
    givenHandsAndRiverInteger = sorted(translateCardNotation(1, givenHandsAndRiver))
    givenHandsAndRiverCounted = Counter(givenHandsAndRiverInteger)
    lastPair = 0
    for i in givenHandsAndRiverInteger:
        if 2 <= int(givenHandsAndRiverCounted[int(i)]):
            hands["Pair"] = int(i)
            lastPair += 1
        if 2 <= int(givenHandsAndRiverCounted[int(i)]) and lastPair >= 3:
            hands["Two Pair"] = int(i)
        if 3 <= int(givenHandsAndRiverCounted[int(i)]):
            hands["Three Card"] = int(i)
        if 4 <= int(givenHandsAndRiverCounted[int(i)]):
            hands["Four Of A Kind"] = int(i)
    straightCounter = 0
    for i in range(len(givenHandsAndRiverInteger) - 1):
        if int(givenHandsAndRiverInteger[i])+1 == int(givenHandsAndRiverInteger[i+1]):
            straightCounter += 1
        elif int(givenHandsAndRiverInteger[i])+6 == int(givenHandsAndRiverInteger[i+1]):
            straightCounter += 1
        else:
            straightCounter = 0
        if straightCounter >= 5:
            hands["Straight"] = givenHandsAndRiverInteger[i]
            break
    if any(count >= 5 for count in Counter([i[1] for i in givenHandsAndRiver]).values()):
        hands["Flush"] = str(i)[0]
        if ("10, 11, 12, 13, 14" in str(givenHandsAndRiverInteger)):
            hands["Royal Flush"] = True
    if not(hands["Pair"] == None) and not(hands["Three Card"] == None):
        hands["Full House"] = max([hands["Pair"], hands["Three Card"]])
    if not(hands["Straight"] == None) and not(hands["Flush"] == None):
        hands["Straight Flush"] = int(hands["Flush"])
    return(hands)

selfResults = {"Pair": [], "Two Pair": [], "Three Card": [], "Straight": [], "Flush": [], "Full House": [], "Four Of A Kind": [], "Straight Flush": [], "Royal Flush": []}

oppoResults = {"Pair": [], "Two Pair": [], "Three Card": [], "Straight": [], "Flush": [], "Full House": [], "Four Of A Kind": [], "Straight Flush": [], "Royal Flush": []}

operationsCount=[0.01, 0]
for _ in ((i,j) for i in [deckDealer[a*2] for a in range(len(deckDealer)//2)] for j in [deckDealer[b*2+1] for b in range(len(deckDealer)//2-1)]):
    if USERINPUT["Calculate Opponent"] == "Y":
        for r in ((p,q) for p in [deckDealer[a*2] for a in range(len(deckDealer)//2)] for q in [deckDealer[b*2+1] for b in range(len(deckDealer)//2-1)]):
            if len(set([_[0], _[1], r[0], r[1]])) == 4:
                operationsCount[0]+=1
                oppoPossibility = checkCurrentHands([r[0],r[1]], deckKnownHands["River"]+[_[0],_[1]])
                if oppoPossibility["Pair"] != None: oppoResults["Pair"].append(oppoPossibility["Pair"])
                if oppoPossibility["Two Pair"] != None: oppoResults["Two Pair"].append(oppoPossibility["Two Pair"])
                if oppoPossibility["Three Card"] != None: oppoResults["Three Card"].append(oppoPossibility["Three Card"])
                if oppoPossibility["Straight"] != None: oppoResults["Straight"].append(oppoPossibility["Straight"])
                if oppoPossibility["Flush"] != None: oppoResults["Flush"].append(oppoPossibility["Flush"])
                if oppoPossibility["Full House"] != None: oppoResults["Full House"].append(oppoPossibility["Full House"])
                if oppoPossibility["Four Of A Kind"] != None: oppoResults["Four Of A Kind"].append(oppoPossibility["Four Of A Kind"])
                if oppoPossibility["Straight Flush"] != None: oppoResults["Straight Flush"].append(oppoPossibility["Straight Flush"])
                if oppoPossibility["Royal Flush"] != None: oppoResults["Royal Flush"].append(oppoPossibility["Royal Flush"])
    if not (_[0] == _[1]):
        operationsCount[1]+=1
        selfPossibility = checkCurrentHands(deckKnownHands["Hands"], deckKnownHands["River"]+[_[0],_[1]])
        if selfPossibility["Pair"] != None: selfResults["Pair"].append(selfPossibility["Pair"])
        if selfPossibility["Two Pair"] != None: selfResults["Two Pair"].append(selfPossibility["Two Pair"])
        if selfPossibility["Three Card"] != None: selfResults["Three Card"].append(selfPossibility["Three Card"])
        if selfPossibility["Straight"] != None: selfResults["Straight"].append(selfPossibility["Straight"])
        if selfPossibility["Flush"] != None: selfResults["Flush"].append(selfPossibility["Flush"])
        if selfPossibility["Full House"] != None: selfResults["Full House"].append(selfPossibility["Full House"])
        if selfPossibility["Four Of A Kind"] != None: selfResults["Four Of A Kind"].append(selfPossibility["Four Of A Kind"])
        if selfPossibility["Straight Flush"] != None: selfResults["Straight Flush"].append(selfPossibility["Straight Flush"])
        if selfPossibility["Royal Flush"] != None: selfResults["Royal Flush"].append(selfPossibility["Royal Flush"])

selfTotalExecution = operationsCount[1]
oppoTotalExecution = operationsCount[0]

selfPercentage = {"Pair": "", "Two Pair": "", "Three Card": "", "Straight": "", "Flush": "", "Full House": "", "Four Of A Kind": "", "Straight Flush": "", "Royal Flush": ""}
oppoPercentage = {"Pair": "", "Two Pair": "", "Three Card": "", "Straight": "", "Flush": "", "Full House": "", "Four Of A Kind": "", "Straight Flush": "", "Royal Flush": ""}

for i in selfResults.keys():
    selfResults[str(i)] = Counter(translateCardNotation(2, selfResults[str(i)]))
for i in oppoResults.keys():
    oppoResults[str(i)] = Counter(translateCardNotation(2, oppoResults[str(i)]))
for i in oppoResults.keys():
    oppoPercentage[str(i)] = fixToDigits(6, str((int(sum(list(oppoResults[str(i)].values()))) / oppoTotalExecution)*100)[:6], "0")
for i in selfResults.keys():
    selfPercentage[str(i)] = fixToDigits(6, str((int(sum(list(selfResults[str(i)].values()))) / selfTotalExecution)*100)[:6], "0")

print(f"""
Possibilities of you:
(
              "Pair": {selfPercentage["Pair"]} %   -   {selfResults["Pair"]}
          "Two Pair": {selfPercentage["Two Pair"]} %   -   {selfResults["Two Pair"]}
        "Three Card": {selfPercentage["Three Card"]} %   -   {selfResults["Three Card"]}
          "Straight": {selfPercentage["Straight"]} %   -   {selfResults["Straight"]}
             "Flush": {selfPercentage["Flush"]} %   -   {selfResults["Flush"]}
        "Full House": {selfPercentage["Full House"]} %   -   {selfResults["Full House"]}
    "Four Of A Kind": {selfPercentage["Four Of A Kind"]} %   -   {selfResults["Four Of A Kind"]}
    "Straight Flush": {selfPercentage["Straight Flush"]} %   -   {selfResults["Straight Flush"]}
       "Royal Flush": {selfPercentage["Royal Flush"]} %   -   {selfResults["Royal Flush"]}
""")
if USERINPUT["Calculate Opponent"] == "Y":
     print(f"""
Possibilities of the opponent:
(
              "Pair": {oppoPercentage["Pair"]} %   -   {oppoResults["Pair"]}
          "Two Pair": {oppoPercentage["Two Pair"]} %   -   {oppoResults["Two Pair"]}
        "Three Card": {oppoPercentage["Three Card"]} %   -   {oppoResults["Three Card"]}
          "Straight": {oppoPercentage["Straight"]} %   -   {oppoResults["Straight"]}
             "Flush": {oppoPercentage["Flush"]} %   -   {oppoResults["Flush"]}
        "Full House": {oppoPercentage["Full House"]} %   -   {oppoResults["Full House"]}
    "Four Of A Kind": {oppoPercentage["Four Of A Kind"]} %   -   {oppoResults["Four Of A Kind"]}
    "Straight Flush": {oppoPercentage["Straight Flush"]} %   -   {oppoResults["Straight Flush"]}
       "Royal Flush": {oppoPercentage["Royal Flush"]} %   -   {oppoResults["Royal Flush"]}
)""")
