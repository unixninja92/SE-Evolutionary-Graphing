import glob
import string
import pickle
import datetime
import os

class ConfigInfo(object):

    def __init__(self):
        self.StartingGeneration = 1
        self.GeneticDifference = False
        self.GLSystem = [False] #[whetherLSystemOrNot, Enter number of non-terminals, Enter number of terminals, Enter expansion rate]
        self.PhenotypicDifference = False

    def setConfig(self,DirectoriesToParse,StartingGeneration,GeneticDifference,GLSystem,PhenotypicDifference,FileToSave,ConfigLocation):
        # sets and saves a new configuration
        self.StartingGeneration = StartingGeneration
        self.GeneticDifference = GeneticDifference
        self.GLSystem = GLSystem
        self.PhenotypicDifference = PhenotypicDifference
        
class DataParser(object):
    """Takes settings from GUI, imports data, and parses it accordingly"""

    def getPreviousConfig(self,ConfigFile="ParseConfig.pkl"):
        '''gets the previous configuration'''
        self.Config = pickle.load(ConfigFile)

    def setConfig(self,DirectoriesToParse,StartingGeneration,GeneticDifference,GLSystem,PhenotypicDifference,FileToSave = "ParsedData" + datetime.datetime.now().strftime("%y-%m-%d-%H") + ".pkl",ConfigLocation = "ParseConfig.pkl"):
        # sets and saves a new configuration
        self.DirectoriesToParse = DirectoriesToParse
        self.FileToSave = os.path.abspath(FileToSave)
        self.ConfigLocation = ConfigLocation
        self.Config.setConfig(DirectoriesToParse, StartingGeneration, GeneticDifference, GLSystem, PhenotypicDifference, FileToSave, ConfigLocation)
        configLocation = open(self.ConfigLocation,"w+")
        pickle.dump(self.Config,configLocation,2)

    def importPreviousRun(self,FilePath): # This should return the result of previous runs
        self.DataList = pickle.load(FilePath)

    def averageData(self,DataArraysToAverage):
        AveragedData = DataArraysToAverage[0]
        for DataArray in DataArraysToAverage[1:]:
            # average the arrays and reset previous to current
            for i in range(0,len(DataArray)):
                Data = DataArray[i]
                if type(Data) is list:
                    for j in range(0,len(Data)):
                        PrevData = float(AveragedData[i][j])
                        CurrData = float(Data[j])
                        AveragedData[i][j] = (PrevData + CurrData)
                else:
                    AveragedData[i] += Data
        Divisor = len(DataArraysToAverage)
        for i in range(0,len(AveragedData)):
            Data = AveragedData[i]
            if type(Data) is list:
                for j in range(0,len(Data)):
                    currentData = float(AveragedData[i][j])
                    AveragedData[i][j] = currentData / Divisor
            else:
                currentData = float(AveragedData[i])
                AveragedData[i] = currentData / Divisor
        return AveragedData

    def parseData(self):
        # parses the data averaging all the data directories in the column and storing the averages
        ParsedData = self.DataList
        for DirectoryList in self.DirectoriesToParse:
            FileData = []
            if DirectoryList:
                ###ADAPTED FROM THE FUNCTION GetOneDataRun###
                for DirectoryName in DirectoryList:
                    candidateFiles = DirectoryName + "/Generation*.txt" 
                    listOfFiles = glob.glob(candidateFiles) # this line looks at the directory and returns anything that matches.
                    numberOfFilesToProcess = len(listOfFiles)
#                     print "there are", numberOfFilesToProcess, "files to process." ###OUTPUT TO GUI###
                    thisFileNumberNext = 1
                    aOfBests = []
                    aOfAverages = []
                    aOfXValues = []
                    aOfDiversities = []
                    aOfPhenotypeDiversity = []
                    indexOfFirstFile = self.Config.StartingGeneration
                    if indexOfFirstFile == "":
                        indexOfFirstFile = 1
                    indexOfFirstFile = int(indexOfFirstFile)
                    #for each file...
                    while thisFileNumberNext <= numberOfFilesToProcess:
                        # create the file name, so they are in numeric order
                        # instead of alphabetic order (i.e. 49 > 5)
                        currentFileName = DirectoryName + "/Generation" + str(thisFileNumberNext + indexOfFirstFile - 1) + ".txt"
                        # create a "handle" into the file.
                        fileHandle = open(currentFileName)
                        # put the file into an array.
                        thisFileArray = fileHandle.readlines()
                        # close the file. Too many files open can cause a program to crash
                        # but it has to be TOO MANY, like if you fall into an infinite loop.
                        fileHandle.close()
                        #grab the last line
                        lineWithSummary = thisFileArray[-1]
                        #print "the summary line for file", currentFileName, "is", lineWithSummary
                        thisFileNumberNext = thisFileNumberNext + 1
                        # break the line (which is currently one long string) into an array, using white spaces as delimiters.
                        arrayWithSummary = lineWithSummary.split()
                        # the sixth element is the average
                        averageFitness = arrayWithSummary[5]
                        #take the semicolon out
                        #this is called taking a slice. 
                        # it returns a piece of the array. 
                        # in this case the piece being returned goes from the first element,
                        # since I left the first position blank,
                        # up to everything except the last element.
                        # in general A[beginning:end] returns the elements of that array
                        # starting with position beginning and up to (but not including) end.  
                        averageFitness = averageFitness[:-1] 
                        # the ninth element is the best
                        bestFitness = arrayWithSummary[8]
                        #print "generation", thisFileNumberNext, "Average:", averageFitness, "Best:", bestFitness 
                        # put the values into arrays
                        aOfAverages.append(averageFitness)
                        aOfBests.append(bestFitness)
                        aOfXValues.append(thisFileNumberNext + indexOfFirstFile - 1)
                    # we're done reading data from the files
                    if self.Config.GeneticDifference:
                        aOfDiversities = self.ComputeGeneticDifference(DirectoryName, indexOfFirstFile)
                    if self.Config.PhenotypicDifference:
                        aOfPhenotypeDiversity = self.ComputePhenotypicDifference(DirectoryName)
                        #print "phenotypic difference array:", aOfPhenotypeDiversity
                    FileData.append([aOfBests, aOfAverages, aOfXValues, aOfDiversities, aOfPhenotypeDiversity])
                ParsedData.append(self.averageData(FileData))
        DataOut = open(self.FileToSave,"w+")
        DataConfigOut = open(self.FileToSave[:-4] + "Config" + ".pkl","w+")
        pickle.dump(ParsedData,DataOut,2)
        pickle.dump(ParsedData,DataConfigOut,2)
        ###Process the parsed data###

    def __init__(self):
        self.Config = ConfigInfo()
        self.DataList = []
        self.DirectoriesToParse = []
        self.FileToSave = "ParsedData" + datetime.datetime.now().strftime("%y-%m-%d-%H") + ".pkl"
        self.ConfigLocation = "ParseConfig.pkl"



###THINGS FROM JAIMES CODE###



    def DifferenceBetweenTwoArrays(self, arrayA, arrayB):
        accumulatedDifference = 0
        indexOfTheElementWeAreLookingAtRightNow = 0
        while indexOfTheElementWeAreLookingAtRightNow < len(arrayA):
            elementOfA = arrayA[indexOfTheElementWeAreLookingAtRightNow]
            elementOfB = arrayB[indexOfTheElementWeAreLookingAtRightNow]
            differenceBetweenTheseTwoslots = abs(float(elementOfA) - float(elementOfB))
            accumulatedDifference = accumulatedDifference + differenceBetweenTheseTwoslots
            indexOfTheElementWeAreLookingAtRightNow = indexOfTheElementWeAreLookingAtRightNow + 1
        averageDifference = accumulatedDifference/len(arrayA)
        #print accumulatedDifference, averageDifference
        return(averageDifference)
        
    def AverageDifferenceInAListsOfLists(self, matrix):
        accumulatedDifference = 0
        indexOfFirstElement = 0
        thingsThatHaveBeenAdded = 0
        while indexOfFirstElement < len(matrix):
            indexOfSecondElement = indexOfFirstElement + 1
            while indexOfSecondElement < len(matrix):
                thingsThatHaveBeenAdded = thingsThatHaveBeenAdded + 1 
                #print firstList, secondList
                firstList = matrix[indexOfFirstElement]
                secondList = matrix[indexOfSecondElement]
                differenceBetweenTheseTwo = self.DifferenceBetweenTwoArrays(firstList, secondList)
                #print "difference between these two", differenceBetweenTheseTwo
                accumulatedDifference = accumulatedDifference + differenceBetweenTheseTwo
                indexOfSecondElement = indexOfSecondElement + 1    
            indexOfFirstElement = indexOfFirstElement + 1         
        averageDifference = accumulatedDifference/thingsThatHaveBeenAdded
        return (averageDifference)    

    def ComputePhenotypicDifference(self, directory):
        # generate a list of files to process
        #candidateFiles = directory + "/Generation*/Element*/weights.text"
        candidateGenerations = directory + "/Generation*[^.]*"
        #listOfFiles = glob.glob(candidateFiles)
        listOfGenerations = glob.glob(candidateGenerations)
        #print "found this many files:", len(listOfFiles)
#         print "found this many generations:", len(listOfGenerations)
        # for each of those files...
        numberOfGenerationsToProcess = len(listOfGenerations)
        arrayOfDiversityValues = []
        thisGenerationNumberNext = 0
        while thisGenerationNumberNext < numberOfGenerationsToProcess:
            arrayOfArrayOfWeights =[]
            # how many elements are there in this generation?
            candidateElements = directory + "/Generation" + str(thisGenerationNumberNext) + "/*"
            listOfElements = glob.glob(candidateElements)
            numberOfElementsToProcess = len(listOfElements)
#             print "Generation", thisGenerationNumberNext, "has", numberOfElementsToProcess, "elements"
            thisElementNumberNext = 0
            while thisElementNumberNext < numberOfElementsToProcess:
                nameOfFile = directory + "/Generation" + str(thisGenerationNumberNext) + "/Element" + str(thisElementNumberNext) + "/weights.text"
#                 print "reading", thisGenerationNumberNext,":", thisElementNumberNext
                # open the file
                fileHandle = open(nameOfFile)
                arrayWithFile = fileHandle.readlines()
                fileHandle.close()
                arrayOfWeights = self.ExtractWeights(arrayWithFile)
                arrayOfArrayOfWeights.append(arrayOfWeights)
                thisElementNumberNext = thisElementNumberNext + 1
            # at this point we have read all of the elements of a single generation.
            diversityInThisGeneration = self.AverageDifferenceInAListsOfLists(arrayOfArrayOfWeights)
            arrayOfDiversityValues.append(diversityInThisGeneration)
            thisGenerationNumberNext = thisGenerationNumberNext + 1
        return(arrayOfDiversityValues)     

    def ComputeGeneticDifference(self, directory, indexOfFirst):
        # generate a list of files to process
        candidateFiles = directory + "/Generation*.txt"
        listOfFiles = glob.glob(candidateFiles) # this line looks at the directory and returns anything that matches.
        numberOfFilesToProcess = len(listOfFiles)
        arrayOfDiversity = []
        thisFileNumberNext = 1
        if self.Config.GLSystem[0]:
            numberOfNonTerminals = self.Config.GLSystem[1]
            numberOfTerminals    = self.Config.GLSystem[2]
            expansionRate        = self.Config.GLSystem[3]
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
            if self.Config.GLSystem[0]:
                #print "generation", thisFileNumberNext
                diversityInThisGeneration = self.ComputeDiversityOfLSystems(listOfGenomes, numberOfNonTerminals, numberOfTerminals, expansionRate)
            else:
                diversityInThisGeneration = self.AverageDifferenceInAListsOfLists(listOfGenomes)
#             print "genetic diversity in generation", thisFileNumberNext + indexOfFirst - 1, ":", diversityInThisGeneration
            arrayOfDiversity.append(diversityInThisGeneration)
            # done with this file.
            # process the next one
            thisFileNumberNext = thisFileNumberNext + 1
        # now we have an array of diversity with values in it.
        # return it.
        return(arrayOfDiversity)        

    def TranslateGenomeToAnLSystem(self, genome, numberOfNonTerminals, numberOfTerminals, expansionRate):
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
                
            
    def ComputeDiversityOfLSystems(self, listOfGenomes, numberOfNonTerminals, numberOfTerminals, expansionRate):
        # first turn the list of genomes into symbols
        #print "list of genomes:", listOfGenomes
        arrayOfLSystems = []
        debug = 0
        for currentGenome in listOfGenomes:
            #print "list of genomes:", listOfGenomes
            #print "genome before going:", currentGenome
            #print "element", debug
            lSystem = self.TranslateGenomeToAnLSystem(currentGenome, numberOfNonTerminals, numberOfTerminals, expansionRate)
            arrayOfLSystems.append(lSystem)
            debug = debug + 1
        # now all of the lsystems have been stored.
        average = self.averageDiversityInAListOfLSystems(arrayOfLSystems) 
        return(average)
        
    def DifferenceBetweenTwoLSystems(self, firstSystem, secondSystem):
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

    def averageDiversityInAListOfLSystems(self, array):
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
                differenceBetweenTheseTwo = self.DifferenceBetweenTwoLSystems(firstList, secondList)
                #print "difference between these two systems", differenceBetweenTheseTwo
                accumulatedDifference = accumulatedDifference + differenceBetweenTheseTwo
                indexOfSecondElement = indexOfSecondElement + 1    
            indexOfFirstElement = indexOfFirstElement + 1         
        averageDifference = accumulatedDifference/thingsThatHaveBeenAdded
        return (averageDifference)
    
    def ExtractWeights(self, array):
        outputArray = []
        for line in array:
            line = line.strip()
            fields = line.split()
            howManyThingsInThisLine = len(fields)
            if (howManyThingsInThisLine == 2):
                if (self.is_number(fields[0])) and  (self.is_number(fields[1])):
                    # the second number is a weight
                    valueToPut = float(fields[1])
                    outputArray.append(valueToPut)
                    # at this point we have an array of weights
                    return(outputArray)
                
    def is_number(self, s):
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
    

if __name__ == '__main__':
    x = DataParser()
    x.setConfig([["/home/mitchel/Documents/Jaime/runnerup_then_champion","/home/mitchel/Documents/Jaime/runnerup_then_champion"], ["/home/mitchel/Documents/Jaime/champion_then_runnerup"]], 1, False, [False], False, "/home/mitchel/Desktop/thing.pkl")
    x.parseData()
