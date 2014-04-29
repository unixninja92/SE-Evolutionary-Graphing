class ParseError(Exception): pass

class DataParser(object):
	"""Takes settings from GUI, imports data, and parses it accordingly"""
	
	DirectoriesToParse = []
	FileToSave = "defaultOut.txt"
	ConfigLocation = "."
	StartingGeneration = 1
	ComputeGeneticDifference = False
	ComputePhenotypicDifference = False


	def checkPreviousConfig(self):
		# checks if there is a valid previous configuration
		return True

	def getPreviousConfig(self):
		# gets the previous configuration
		self.DirectoriesToParse = DirectoriesToParse
		self.FileToSave = FileToSave
		self.ConfigLocation = ConfigLocation
		self.StartingGeneration = StartingGeneration
		self.ComputeGeneticDifference = ComputeGeneticDifference
		self.ComputePhenotypicDifference = ComputePhenotypicDifference

	def setConfig(self,DirectoriesToParse,FileToSave,ConfigLocation,StartingGeneration,ComputeGeneticDifference,ComputePhenotypicDifference):
		# sets and saves a new configuration
		self.DirectoriesToParse = DirectoriesToParse
		self.FileToSave = FileToSave
		self.ConfigLocation = ConfigLocation
		self.StartingGeneration = StartingGeneration
		self.ComputeGeneticDifference = ComputeGeneticDifference
		self.ComputePhenotypicDifference = ComputePhenotypicDifference

	def getDataToParse(self,*args):
		# gets data from given directories
		if args:
			self.DirectoriesToParse = []
			tempArray = []
			for DirectoryName in args:
				if DirectoryName == "EndOfAverageCharacter":
					self.DirectoriesToParse.append(tempArray)
				else:
					tempArray.append(DirectoryName)
			parseData()
		else:
			ex = NoDirectoryError("No Directories Given")
			raise ex

	def averageData(self,DataArrayToAverage):
		AveragedData = []
		PreviousData = DataArrayToAverage[0]
		for DataTuple in DataArrayToAverage[1:]:
			# average the arrays and reset previous to current
			AveragedData[0] = PreviousData[0] + DataTuple[0]
			AveragedData[1] = PreviousData[1] + DataTuple[1]
			AveragedData[2] = PreviousData[2] + DataTuple[2]
			AveragedData[3] = PreviousData[3] + DataTuple[3]
			AveragedData[4] = PreviousData[4] + DataTuple[4]
			PreviousData = DataTuple
		for Data in AveragedData:
			Data = Data/len(DataArrayToAverage)
		return AveragedData

	def parseData(self):
		# parses the data averaging all the data directories in the column and storing the averages
		ParsedData = []
		FileData = []
		for DirectoriesToAverage in self.DirectoriesToParse:
			###ADAPTED FROM THE FUNCTION GetOneDataRun###
			for DirectoryName in DirectoriesToAverage:
			    candidateFiles = DirectoryName + "/Generation*.txt" 
			    listOfFiles = glob.glob(candidateFiles) # this line looks at the directory and returns anything that matches.
			    numberOfFilesToProcess = len(listOfFiles)
			    print "there are", numberOfFilesToProcess, "files to process." ###OUTPUT TO GUI###
			    thisFileNumberNext = 1
			    aOfBests = []
			    aOfAverages = []
			    aOfXValues = []
			    aOfDiversities = []
			    aOfPhenotypeDiversity = []
			    indexOfFirstFile = self.StartingGeneration
			    if indexOfFirstFile == "":
			        indexOfFirstFile = 1
			    indexOfFirstFile = int(indexOfFirstFile)
			    #for each file...
			    while thisFileNumberNext <= numberOfFilesToProcess:
			        # create the file name, so they are in numeric order
			        # instead of alphabetic order (i.e. 49 > 5)
			        currentFileName = directoryWithDataFiles + "/Generation" + str(thisFileNumberNext + indexOfFirstFile - 1) + ".txt"
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
			    if ComputeGeneticDifference:
			        aOfDiversities = ComputeGeneticDifference(directoryWithDataFiles, indexOfFirstFile)
			    if ComputePhenotypicDifference:
			        aOfPhenotypeDiversity = ComputePhenotypicDifference(directoryWithDataFiles)
			        #print "phenotypic difference array:", aOfPhenotypeDiversity
			    FileData.append([aOfBests, aOfAverages, aOfXValues, aOfDiversities, aOfPhenotypeDiversity])
			ParsedData.append(averageData(FileData))

	def __init__(self):
		if self.checkPreviousConfig(): # if a previous configuration exists
			self.getPreviousConfig()
			print "Woo!"



###THINGS FROM JAIMES CODE###



def DifferenceBetweenTwoArrays(arrayA, arrayB):
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
    
    
def AverageDifferenceInAListsOfLists(matrix):
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
            differenceBetweenTheseTwo = DifferenceBetweenTwoArrays(firstList, secondList)
            #print "difference between these two", differenceBetweenTheseTwo
            accumulatedDifference = accumulatedDifference + differenceBetweenTheseTwo
            indexOfSecondElement = indexOfSecondElement + 1    
        indexOfFirstElement = indexOfFirstElement + 1         
    averageDifference = accumulatedDifference/thingsThatHaveBeenAdded
    return (averageDifference)

def ComputePhenotypicDifference(directory):
    # generate a list of files to process
    #candidateFiles = directory + "/Generation*/Element*/weights.text"
    candidateGenerations = directory + "/Generation*[^.]*"
    #listOfFiles = glob.glob(candidateFiles)
    listOfGenerations = glob.glob(candidateGenerations)
    #print "found this many files:", len(listOfFiles)
    print "found this many generations:", len(listOfGenerations)
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
        print "Generation", thisGenerationNumberNext, "has", numberOfElementsToProcess, "elements"
        thisElementNumberNext = 0
        while thisElementNumberNext < numberOfElementsToProcess:
            nameOfFile = directory + "/Generation" + str(thisGenerationNumberNext) + "/Element" + str(thisElementNumberNext) + "/weights.text"
            print "reading", thisGenerationNumberNext,":", thisElementNumberNext
            # open the file
            fileHandle = open(nameOfFile)
            arrayWithFile = fileHandle.readlines()
            fileHandle.close()
            arrayOfWeights = ExtractWeights(arrayWithFile)
            arrayOfArrayOfWeights.append(arrayOfWeights)
            thisElementNumberNext = thisElementNumberNext + 1
        # at this point we have read all of the elements of a single generation.
        diversityInThisGeneration = AverageDifferenceInAListsOfLists(arrayOfArrayOfWeights)
        arrayOfDiversityValues.append(diversityInThisGeneration)
        thisGenerationNumberNext = thisGenerationNumberNext + 1
    return(arrayOfDiversityValues) 

def ComputeGeneticDifference(directory, indexOfFirst):
    # generate a list of files to process
    candidateFiles = directory + "/Generation*.txt"
    listOfFiles = glob.glob(candidateFiles) # this line looks at the directory and returns anything that matches.
    numberOfFilesToProcess = len(listOfFiles)
    arrayOfDiversity = []
    thisFileNumberNext = 1
    ###THIS PART NEEDS TO BE ASKED THROUGH THE GUI###
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
