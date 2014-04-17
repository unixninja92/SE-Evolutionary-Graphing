'''
Created on Apr 5, 2013

@author: jaime
'''
import glob
import pylab
import numpy
import string

def plotter(valuesInXAxis, valuesInYAxis, plotsSoFar, generalLabelForLeyend, yAxis):
    #print "the x values are:", valuesInXAxis
    sizeMe=15
    npArrayOfXValues = numpy.array(valuesInXAxis)
    yAxis.plot(valuesInXAxis, valuesInYAxis, arrayOfPlotCharacters[plotsSoFar], label=generalLabelForLeyend, lw=sizeMe/4, ms=sizeMe)
    yAxis.plot(valuesInXAxis, valuesInYAxis, lw=sizeMe/4, ms=sizeMe)
    userAnswer = raw_input("Do you want to show approximation for this data? [Y/n]")
    if userAnswer == "":
        userAnswer = "y"
    if userAnswer.upper() == "Y": 
        numericArray = []
        for x in valuesInYAxis:
            numericArray.append(float(x))
        npArrayOfYValues = numpy.array(numericArray)
        #print "xvalues:yvalues", len(npArrayOfXValues), len(npArrayOfYValues)
        approximation = numpy.polyfit(npArrayOfXValues, npArrayOfYValues, 5)
        p = numpy.poly1d(approximation)
        pxp=p(valuesInXAxis)
        yAxis.plot(valuesInXAxis, pxp, '-')
        #pxp=p(arrayOfXValues)
        #yAxis.plot(arrayOfXValues, pxp, '-')
    #return (ax)

def LinesDrawer(matrixOfValues, labelForLegend, plotsSoFar, yAxis, beginningXValue = 0):
    #print "the matrix is", matrixOfValues
    Averages, Minimums, Maximums, StandardDeviations = LinesGenerator(matrixOfValues)
    arrayOfXValues = range(beginningXValue, beginningXValue + len(Averages))
    ticker = arrayOfPlotCharacters[plotsSoFar]
    plotter(arrayOfXValues, Averages, plotsSoFar, labelForLegend, yAxis)
    userAnswer = raw_input("Do you want to plot ranges for this data? [y/N]")
    if userAnswer == "":
        userAnswer = "n"        
    if userAnswer.upper() == "Y":
        lowRange  = [a - b for a, b in zip(Averages, Minimums)]
        highRange = [a - b for a, b in zip(Maximums, Averages)]
        pylab.errorbar(arrayOfXValues, Averages, yerr= [lowRange, highRange])
    userAnswer = raw_input("Do you want to plot the standard deviation for this data? [y/N]")
    if userAnswer == "":
        userAnswer = "n"        
    if userAnswer.upper() == "Y":
        lowDev  = [a - b for a, b in zip(Averages, StandardDeviations)]
        highDev = [a + b for a, b in zip(Averages, StandardDeviations)]
        pylab.fill_between(arrayOfXValues, highDev, lowDev, facecolor='grey', alpha=0.5, )
    plotsSoFar = plotsSoFar + 1
    return(plotsSoFar)
        
def is_number(s):
# this function comes from
# http://www.pythoncentral.io/how-to-check-if-a-string-is-a-number-in-python-including-unicode/
    try:
        float(s)
        return True
    except ValueError:
        pass
 
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
 
    return False


def ExtractWeights(array):
    outputArray = []
    for line in array:
        line = line.strip()
        fields = line.split()
        howManyThingsInThisLine = len(fields)
        if (howManyThingsInThisLine == 2):
            if (is_number(fields[0])) and  (is_number(fields[1])):
                # the second number is a weight
                valueToPut = float(fields[1])
                outputArray.append(valueToPut)
    # at this point we have an array of weights
    return(outputArray)
        
        

def ComputeGeneticDifference(directory, indexOfFirst):
    # generate a list of files to process
    candidateFiles = directory + "/Generation*.txt"
    listOfFiles = glob.glob(candidateFiles) # this line looks at the directory and returns anything that matches.
    numberOfFilesToProcess = len(listOfFiles)
    arrayOfDiversity = []
    thisFileNumberNext = 1
    lSystemOrNot = raw_input("Is this an LSystem? [Y/n]")
    if lSystemOrNot == "":
        lSystemOrNot = "Y"
    if lSystemOrNot.upper() == "Y":
        numberOfNonTerminals = int(raw_input("Enter number of non-terminals:"))
        numberOfTerminals    = int(raw_input("Enter number of terminals    :"))
        expansionRate        = int(raw_input("Enter expansion rate         :"))
    #for each file...
    while thisFileNumberNext <= numberOfFilesToProcess:
        listOfGenomes = []
        currentFileName = directory + "/Generation" + str(thisFileNumberNext + indexOfFirst - 1) + ".txt"
        # create a "handle" into the file.
        fileHandle = open(currentFileName)
        # put the file into an array.
        thisFileArray = fileHandle.readlines()
        fileHandle.close()
        # get rid of the last line, which does not have an element.
        # (it has some statistics used elsewhere)
        thisFileArray.pop()
        # now we have an array of genomes.
        for line in thisFileArray:
            # remove all brackets and commas from each genome
            line = line.translate(None, '{},')
            # split the line based on white spaces
            genome = line.split()
            # get rid of the fitness value, which is stored at the end.
            genome.pop()
            #put this genome into a list of genomes.
            listOfGenomes.append(genome)
        # compute the diversity of this list of genomes
        if lSystemOrNot.upper() == "Y":
            #print "generation", thisFileNumberNext
            diversityInThisGeneration = ComputeDiversityOfLSystems(listOfGenomes, numberOfNonTerminals, numberOfTerminals, expansionRate)
        else:
            diversityInThisGeneration = AverageDifferenceInAListsOfLists(listOfGenomes)
        print "genetic diversity in generation", thisFileNumberNext + indexOfFirst - 1, ":", diversityInThisGeneration
        arrayOfDiversity.append(diversityInThisGeneration)
        # done with this file.
        # process the next one
        thisFileNumberNext = thisFileNumberNext + 1
    # now we have an array of diversity with values in it.
    # return it.
    return(arrayOfDiversity)    

def TranslateGenomeToAnLSystem(genome, numberOfNonTerminals, numberOfTerminals, expansionRate):
    numberofGeneToTranslateNext     = 0
    mappedGenome                    = []
    numberOfChunks                  = numberOfNonTerminals + numberOfTerminals
    # first map the non-terminals.
    
    while numberofGeneToTranslateNext < numberOfNonTerminals*expansionRate:
        indexToLetter = int(float(genome[numberofGeneToTranslateNext]) * numberOfChunks)
        letterToUse   = string.ascii_letters[indexToLetter]
        mappedGenome.append(letterToUse)
        numberofGeneToTranslateNext =  numberofGeneToTranslateNext +1
    # then map the terminals.
    while numberofGeneToTranslateNext < numberOfNonTerminals*expansionRate + numberOfTerminals:
        indexToLetter = int(float(genome[numberofGeneToTranslateNext]) * numberOfTerminals) + numberOfNonTerminals
        letterToUse   = string.ascii_letters[indexToLetter]
        mappedGenome.append(letterToUse)
        numberofGeneToTranslateNext =  numberofGeneToTranslateNext +1 
    #print genome
    #print mappedGenome
    return(mappedGenome)
            
        
def ComputeDiversityOfLSystems(listOfGenomes, numberOfNonTerminals, numberOfTerminals, expansionRate):
    # first turn the list of genomes into symbols
    #print "list of genomes:", listOfGenomes
    arrayOfLSystems = []
    debug = 0
    for currentGenome in listOfGenomes:
        #print "list of genomes:", listOfGenomes
        #print "genome before going:", currentGenome
        #print "element", debug
        lSystem = TranslateGenomeToAnLSystem(currentGenome, numberOfNonTerminals, numberOfTerminals, expansionRate)
        arrayOfLSystems.append(lSystem)
        debug = debug + 1
    # now all of the lsystems have been stored.
    average = averageDiversityInAListOfLSystems(arrayOfLSystems) 
    return(average)
    
def DifferenceBetweenTwoLSystems(firstSystem, secondSystem):
    #print "comparing", firstSystem
    #print "with     ", secondSystem
    accumulatedDifference = 0
    indexOfTheElementWeAreLookingAtRightNow = 0
    while indexOfTheElementWeAreLookingAtRightNow < len(firstSystem):
        elementOfA = firstSystem[indexOfTheElementWeAreLookingAtRightNow]
        elementOfB = secondSystem[indexOfTheElementWeAreLookingAtRightNow]
        #print "now comparing these two symbols:", elementOfA, elementOfB
        if elementOfA == elementOfB:
            differenceBetweenTheseTwoslots = 0
        else:
            differenceBetweenTheseTwoslots = 1 
        #print "the answer is", differenceBetweenTheseTwoslots
        accumulatedDifference = accumulatedDifference + differenceBetweenTheseTwoslots
        indexOfTheElementWeAreLookingAtRightNow = indexOfTheElementWeAreLookingAtRightNow + 1
    averageDifference = float(accumulatedDifference)/len(firstSystem)
    #print accumulatedDifference, averageDifference
    return(averageDifference)

def averageDiversityInAListOfLSystems(array):
    accumulatedDifference = 0
    indexOfFirstElement = 0
    thingsThatHaveBeenAdded = 0
    while indexOfFirstElement < len(array):
        indexOfSecondElement = indexOfFirstElement + 1
        while indexOfSecondElement < len(array):
            thingsThatHaveBeenAdded = thingsThatHaveBeenAdded + 1 
            #print firstList, secondList
            firstList = array[indexOfFirstElement]
            secondList = array[indexOfSecondElement]
            differenceBetweenTheseTwo = DifferenceBetweenTwoLSystems(firstList, secondList)
            #print "difference between these two systems", differenceBetweenTheseTwo
            accumulatedDifference = accumulatedDifference + differenceBetweenTheseTwo
            indexOfSecondElement = indexOfSecondElement + 1    
        indexOfFirstElement = indexOfFirstElement + 1         
    averageDifference = accumulatedDifference/thingsThatHaveBeenAdded
    return (averageDifference)


    
    
def LinesGenerator(matrixOfValues):
    
    generationsProcessed = 0
    Averages           = []
    Minimums           = []
    Maximums           = []
    StandardDeviations = []
    while generationsProcessed < len(matrixOfValues):
        arrayOfASingleGeneration   = matrixOfValues[generationsProcessed]
        npArrayOfASingleGeneration = numpy.array(arrayOfASingleGeneration) 
        Averages.append(numpy.mean(npArrayOfASingleGeneration))
        Minimums.append(numpy.min(npArrayOfASingleGeneration))
        Maximums.append(numpy.max(npArrayOfASingleGeneration))
        StandardDeviations.append(numpy.std(npArrayOfASingleGeneration))
        generationsProcessed = generationsProcessed + 1
    return (Averages, Minimums, Maximums, StandardDeviations)

def PutIntoBigMatrix(newArray, matrixOfAllValues):
    # precondition: the arrays are of the same size
    entriesToProcess = len(newArray)
    processedAlready = 0
    while (processedAlready < entriesToProcess):
        while processedAlready >= len(matrixOfAllValues):
            matrixOfAllValues.append([])
        matrixOfAllValues[processedAlready].append(float(newArray[processedAlready]))
        processedAlready    = processedAlready + 1
    return(matrixOfAllValues)

def SaveThisType(label, data, filename):
    filename.write("### ")
    filename.write(label)
    filename.write("\n")
    if len(data) > 0:
        firstGeneration = data[0]
        numberOfRuns    = len(firstGeneration)
        numberOfGenerations = len(data)
        currentRun = 0
        while (currentRun < numberOfRuns):
            currentGeneration = 0
            while currentGeneration < numberOfGenerations:
                filename.write("%s " % data[currentGeneration][currentRun])
                currentGeneration = currentGeneration + 1
            filename.write("\n")
            currentRun = currentRun + 1
        
def SaveDataToFile(a, b, c, d):
    userAnswer = ""
    while userAnswer == "":
        userAnswer = raw_input("Enter file name:")
    fileHandle = open(userAnswer, "w")
    SaveThisType("1 Bests", a, fileHandle)
    SaveThisType("2 Averages", b, fileHandle)
    SaveThisType("3 Genetic Differences", c, fileHandle)
    SaveThisType("4 Phenotypic Differences", d, fileHandle)
    fileHandle.write("### End")
    fileHandle.close()
    
def ProcessFromHereToHere(array, fromHere, toHere, intoThisMatrix):
    # begin by finding the "fromHere" line
    currentLineIndex = 0
    while fromHere not in array[currentLineIndex]:
        currentLineIndex = currentLineIndex + 1
    # found it. now process until we find the "toHere" tag
    currentLineIndex = currentLineIndex + 1
    while toHere not in array[currentLineIndex]:
        #read one line
        currentLine = array[currentLineIndex]
        # divide it into elements, based on spaces
        currentValues = currentLine.split()
        # we now have the data in an array, but they are in "run first" order.
        # we need to turn it into a "generation first" order.
        # storing them into the matrix will do that work.
        PutIntoBigMatrix(currentValues, intoThisMatrix)
        currentLineIndex = currentLineIndex + 1   
    return(intoThisMatrix)

def SubstractArrays(A1, A2):
    A3 = []
    thisIndexNext = 0
    while thisIndexNext < len(A1):
        nextElement = A1[thisIndexNext] - A2[thisIndexNext]
        A3.append(nextElement)
        thisIndexNext = thisIndexNext + 1
    return (A3)

def DivideArrays(A1, A2):
    A3 = []
    thisIndexNext = 0
    while thisIndexNext < len(A1):
        nextElement = A1[thisIndexNext] / A2[thisIndexNext]
        A3.append(nextElement)
        thisIndexNext = thisIndexNext + 1
    return (A3)
   
def ReadDataFromFile(a, b, c, d):
    userAnswer = raw_input("Enter file name:")
    fileHandle = open(userAnswer)
    fileAsArray = fileHandle.readlines()
    fileHandle.close()
    ProcessFromHereToHere(fileAsArray, "Bests", "Averages", a)
    ProcessFromHereToHere(fileAsArray, "Averages", "Genetic Differences", b)
    ProcessFromHereToHere(fileAsArray, "Genetic Differences", "Phenotypic Differences", c)
    ProcessFromHereToHere(fileAsArray, "Phenotypic Differences", "End", d)
    return(a, b, c, d)    


    
arrayOfPlotCharacters = ['o', 'D','+','*','0','1','2','3','4','5','>','<','^','|','d']
if __name__ == '__main__':
    # these are the characters that define how the plot lines will look like.
    # if there are more data sets than characters here, add more lines, or modify the code
    # so that it loops around.
    # these control characters can be found at http://www.loria.fr/~rougier/teaching/matplotlib/#line-styles
    arrayOfPlotCharacters = ['o', 'D','*','+','X','0','1','2','3','4','5','>','<','^','|','d']
    plotsSoFar      = 0 # so that we know which control character to use for the lines.
    fig, ax1 = pylab.subplots()
    ax2 = ax1.twinx()
    userResponse = raw_input("What do you prefer in the second Y axis, (F)itness values or (d)iversity?")
    if userResponse == "":
        userResponse = "F"
    if userResponse.upper() == "F":
        fitnessAxis   = ax2
        diversityAxis = ax1
    else:
        fitnessAxis   = ax1
        diversityAxis = ax2
    keepGettingData = True
    while keepGettingData: # this loop controls how many lines are going to be drawn in the plot.   
        bigArrayOfBests    = []
        bigArrayOfAverages = []  
        bigArrayOfGeneticDiversities = []
        bigArrayOfPhenotypicDiversities = []
        averageWithMoreData = True
        matrixForBests    = [[]] # first index for the generation, second index for the values.
        matrixForAverages = [[]]
        matrixForGeneticDiversities =[[]]
        matrixForPhenotypicDiversities = [[]]
        matrixForDiversityDifferences =[[]]
        matrixForDiversityRatios = [[]]
        userResponse = raw_input("Do you want to read data from a file? [y/N]") 
        if userResponse == "":
            userResponse = "N"
        if userResponse.upper() == "Y":
            readMoreFromFile = True
        else:
            readMoreFromFile = False
        while readMoreFromFile:
            ReadDataFromFile(matrixForBests, matrixForAverages, matrixForGeneticDiversities, matrixForPhenotypicDiversities)
            userResponse = raw_input("Read from more files? [y/N]")
            if userResponse == "":
                userResponse = "N"
            if userResponse.upper() == "Y":
                readMoreFromFile = True
            else:
                readMoreFromFile = False
        arrayOfXValues = [x for x in range(len(matrixForBests))]
        userResponse = raw_input("Do you want to enter new data [y/N]") 
        if userResponse == "":
            userResponse = "N"
        if userResponse.upper() == "Y":
            while averageWithMoreData: # this loop combines data files into a single line for the plot.
                # get one data run.
                arrayOfBests, arrayOfAverages, arrayOfXValues, arrayOfGeneticDiversities, arrayOfPhenotypicDiversities = GetOneDataRun()
                PutIntoBigMatrix(arrayOfBests, matrixForBests)            
                PutIntoBigMatrix(arrayOfAverages, matrixForAverages)
                PutIntoBigMatrix(arrayOfGeneticDiversities, matrixForGeneticDiversities)
                PutIntoBigMatrix(arrayOfPhenotypicDiversities, matrixForPhenotypicDiversities)
                arrayOfDiversityDifferences = SubstractArrays(arrayOfGeneticDiversities, arrayOfPhenotypicDiversities)
                arrayOfDiversityRatios      = DivideArrays(arrayOfGeneticDiversities, arrayOfPhenotypicDiversities)
                PutIntoBigMatrix(arrayOfDiversityDifferences, matrixForDiversityDifferences)
                PutIntoBigMatrix(arrayOfDiversityRatios, matrixForDiversityRatios)
                userResponse = raw_input("Do you want to average this run with some other(s)? [y/N]") 
                if userResponse == "y":
                    averageWithMoreData = True
                else:
                    averageWithMoreData = False
            # plot
        leyendLabel = raw_input("Enter any label you might want for the legend for this line: []")
        if leyendLabel == "":
            leyendLabel = " "
        labelForBests = leyendLabel + "_Best"
        labelForAverages = leyendLabel + "_Average"
        labelForGeneticDiversities = leyendLabel + "_Genetic_Diversity"
        labelForPhenotypicDiversities = leyendLabel + "_Phenotypic_Diversity"
        labelForDiversityDifference = leyendLabel + "_difference"
        labelForDiversityRatio      = leyendLabel + "ration"
        userAnswer = raw_input("Do you want to plot genetic diversity for this data? [Y/n]")
        if userAnswer == "":
            userAnswer = "y"
        if userAnswer.upper() == "Y":
            plotsSoFar = LinesDrawer(matrixForGeneticDiversities, labelForGeneticDiversities, plotsSoFar, diversityAxis, arrayOfXValues[0]) 
        userAnswer = raw_input("Do you want to plot phenotypic diversity for this data? [Y/n]")
        if userAnswer == "":
            userAnswer = "y"
        if userAnswer.upper() == "Y":
            plotsSoFar = LinesDrawer(matrixForPhenotypicDiversities, labelForPhenotypicDiversities, plotsSoFar, diversityAxis, arrayOfXValues[0])
        userAnswer = raw_input("Do you want to compare genetic and phenotipic diversity for this data? [Y/n]")
        if userAnswer == "":
            userAnswer = "y"
        if userAnswer.upper() == "Y":
            print "Diversity differences..."
            plotsSoFar = LinesDrawer(matrixForPhenotypicDiversities, labelForDiversityDifference, plotsSoFar, diversityAxis, arrayOfXValues[0])
            plotsSoFar = plotsSoFar - 1
            print "Diversity ratios..."
            plotsSoFar = LinesDrawer(matrixForPhenotypicDiversities, labelForDiversityRatio, plotsSoFar, diversityAxis, arrayOfXValues[0])
            plotsSoFar = plotsSoFar - 1
        userAnswer = raw_input("Do you want to compute phenotype modularity? [Y/n]")
        if userAnswer == "":
            userAnswer = "y"
        if userAnswer.upper() == "Y":
            print "later"
        userAnswer = raw_input("Do you want to plot best values for this data? [Y/n]")
        if userAnswer == "":
            userAnswer = "y"
        if userAnswer.upper() == "Y":
            plotsSoFar = LinesDrawer(matrixForBests, labelForBests, plotsSoFar, fitnessAxis, arrayOfXValues[0])
        userAnswer = raw_input("Do you want to plot average values for this data? [Y/n]")
        if userAnswer == "":
            userAnswer = "y"
        if userAnswer.upper() == "Y":
            plotsSoFar = LinesDrawer(matrixForAverages, labelForAverages, plotsSoFar, fitnessAxis, arrayOfXValues[0])
        userResponse = raw_input("Want to compare what you entered with additional data? [y/N]") # in case you want to compare several data runs.
        if userResponse == "y":
            keepGettingData = True
        else:
            keepGettingData = False
    userAnswer = raw_input("Save data to file? [Y/n]")
    if userAnswer == "":
        userAnswer = "y"
    if userAnswer.upper() == "Y":
        SaveDataToFile(matrixForBests, matrixForAverages, matrixForGeneticDiversities, matrixForPhenotypicDiversities)
    sizeMe = 50
    fitnessAxis.set_ylabel('fitness score', fontsize=sizeMe)
    ax1.set_xlabel("generation", fontsize=sizeMe)
    diversityAxis.set_ylabel('diversity', fontsize=sizeMe)
    ax2.legend(loc='upper right', fancybox=True, prop={'size':sizeMe}).get_frame().set_alpha(0.5)
    ax2.tick_params(axis='both', which='major', labelsize=sizeMe)
    ax1.tick_params(axis='both', which='major', labelsize=sizeMe)
    #ax1.legend(loc='upper left' , fancybox=True, prop={'size':sizeMe}).get_frame().set_alpha(0.5)
    pylab.show()
    

    

    
