class Flavor(object):
    
    def __init__(self, name, base, toppings):
        self.name = name
        self.base = base
        self.toppings = toppings

    def printList(self, list):
        for item in list:
            print(item.name + ', ' + item.base)

    def findFlavor(self, name):
        for flav in self.choices:
            if flav.name == name:
                return flav
        else:
            raise NameError("name not found")

    def createExampleFODList(self):
        f1 = Flavor("Really Resses", ["choc"], ["resses"])
        f2 = Flavor("Red Raspberry", ["ex"], ["raspberry base", "raspberry"])
        f3 = Flavor("Crazy For Cookie Dough", ["van", "choc"], ["cookie dough", "salted caramel", "novelty chocolate"])
        f4 = Flavor("Oreo Overload", ["choc"], ["oreo"])
        f5 = Flavor("Mint Oreo", ["ex"], ["mint base", "oreo"])
        f6 = Flavor("Caramel Pecan", ["van"], ["salted caramel", "pecan"])
        f7 = Flavor("Peach Crisp", ["ex"], ["peach base", "peach"])
        f8 = Flavor("Mint Chip", ["ex"], ["mint base", "dove"])

        FODList = []
        FODList.append(f1)
        FODList.append(f2)
        FODList.append(f3)
        FODList.append(f4)
        FODList.append(f5)
        FODList.append(f6)
        FODList.append(f7)
        FODList.append(f8)

        return FODList

    # this is nasty
    def initFODLists(self):
        certainDayFODs = []
        monthlyFODs = []
        FODChoices = []
        
        with open('FODchoices.txt') as f:
            lines = f.readlines()

            currSection = ""
            name = ""
            day = ""
            base = ""
            toppings = []
            temp = ""

            startIndex = 0
            endIndex = 0
                
            for line in lines:
                line = line.strip()
                if line == "(":
                    currSection = "certainDayFOD"
                    continue
                elif line == "[":
                    currSection = "monthlyFOD"
                    continue
                elif line == "{":
                    currSection = "FODChoice"
                    continue

                if currSection == "certainDayFOD":
                    if line == ")":
                        currSection = ""
                        continue
                    
                    name = line[0:line.index("-") - 1].strip()
                    day = line[line.index("-") + 1: line.index("-") + 4].strip()
                    certainDayFODs.append([name, day])

                if currSection == "monthlyFOD":
                    if line.find(",") == -1:
                        name = line
                        currSection = ""
                    else:
                        name = line[:line.index(",")]

                    monthlyFODs.append(name)
                

                if currSection == "FODChoice":
                    if line == "}":
                        currSection = ""
                        FODChoices.append(Flavor(name, base, toppings))
                    elif line.find("Name:") != -1:
                        name = line[6:]
                    elif line.find("Base:") != -1:
                        base = line[6:]
                    elif line.find("Toppings:") != -1:
                        toppings = []

                        line = line[10:]
                        while line.find(",") != -1:
                            endIndex = line.find(",")
                            toppings.append(line[:endIndex])
                            line = line[endIndex + 2:]

                        toppings.append(line)

        return [certainDayFODs, monthlyFODs, FODChoices] 

    def findFlavor(self, name):
        for flav in self.choices:
            if flav.name == name:
                return flav
        else:
            raise NameError("name not found")

    # Tests if a flavor shares toppings with another flavor
    # Returns True if the flavors share a topping, False if otherwise
    def sharesToppings(self, flav):
        for selfTopping in self.toppings:
            for otherTopping in flav.toppings:
                if selfTopping == otherTopping:
                    return True
        return False

    # Tests if the two previous indexes behind a flavor shares toppings
    # Returns True if one of the previous two indexes share a topping
    def sharesToppingsWithNeighbors(self, currentIndex, flavList):
        spacesToCheck = 2

        if currentIndex < spacesToCheck:
            startIndex = 0
        else:
            startIndex = currentIndex - spacesToCheck
        
        for flavor in flavList[startIndex : currentIndex]:
            if self.sharesToppings(flavor):
                return True
        return False

    def makeFODList(self, days):
        import random

        FODList = []
        choices = self.initFODLists()[2]

        # choose a flavor for the list to start with
        randStart = random.randint(0, len(choices) - 1)
        FODList.append(choices.pop(randStart))

        # define the step order and determine the starting index using the starting flavor
        steps = ['van','ex','choc','ex']
        stepNumber = steps.index(FODList[0].base)

        # create alternating base list
        for i in range(days-1):

            # determine the next base in the list          
            nextBase = steps[(stepNumber + 1) % 4]

            # create a list to pull flavors from without altering the original template
            currentChoices = []
            currentChoices.extend(choices)

            # remove any flavors that do not have the correct base
            removalList = []
            for flavor in currentChoices:
                if flavor.base != nextBase:
                    removalList.append(flavor)

            for flavor in removalList:
                currentChoices.remove(flavor)

            # shuffle the list so the flavor is chosen randomly from the pile
            random.shuffle(currentChoices)
            # iterate through the choices until a flavor with the suitable toppings is found
            for flavor in currentChoices:
                if flavor.sharesToppingsWithNeighbors(len(FODList), FODList) is False:
                    itemPopped = flavor
                    break
            else:
                raise Exception("No suitable flavors found in this instance")
                          

            # after a suitable base is found, remove it from the original choices to prevent reuse,
            # then add it to the FOD list
            choices.remove(itemPopped)
            FODList.append(itemPopped)
            stepNumber += 1

           
        return FODList
