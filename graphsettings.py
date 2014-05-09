import matplotlib.pyplot as plt
import pickle
import numpy
import pylab
import glob
import string
import os.path
import os

class SettingsInfo:
    def __init__(self):
        self.approximation = True
        self.ploteRanges = False
        self.plotStandDev = False
        self.fitnessOnYAxis = True
        self.plotGenDiversity = True
        self.plotPhenodiversity = True
        self.comparegp = False
        self.plotBestVals = True
        self.plotAverages = True
        self.title = "Untitled"
        self.size = 1
        self.fontType = 1
        self.color = 0
        self.graphType = 0
        self.xAxis = "Untitled"
        self.yAxis = "Untitled"

    def setConfig(self, title, size, fontType, color, graphType, xAxis, yAxis, approximation, ploteRanges, plotStandDev, fitnessOnYAxis, plotGenDiversity, plotPhenodiversity, comparegp, plotBestVals, plotAverages):
        self.approximation = approximation
        self.ploteRanges = ploteRanges
        self.plotStandDev = plotStandDev
        self.fitnessOnYAxis = fitnessOnYAxis
        self.plotGenDiversity = plotGenDiversity
        self.plotPhenodiversity = plotPhenodiversity
        self.comparegp = comparegp
        self.plotBestVals = plotBestVals
        self.plotAverages = plotAverages
        self.title = title
        self.size = size
        self.fontType = fontType
        self.color = color
        self.graphType = graphType
        self.xAxis = xAxis
        self.yAxis = yAxis


class GraphSettings:
    fontSizeList = ["10", "12", "14", "16", "18", "20", "22", "24",]
    fontTypeList = ["Arial", "Times New Roman", "Calibri", "Sans Serif", "Comic Sans"]
    fontColorList = ["blue", "green", "red", "cyan", "magenta", "yellow", "black", "white"]
    graphTypeList = ["Line", "Scatterplot", "Bar", "Pie Chart"]
    arrayOfPlotCharacters = ['o', 'D','+','*','1','2','3','4','5','>','<','^','|','d']

    def __init__(self, dataFile):
        self.settingsFileName = "lastGraphSettings.pkl"
        self.loadSettings()
        self.dataFilePath = dataFile
        print dataFile
        self.data = pickle.load(open(self.dataFilePath, "rb"))

    def loadSettings(self):
        if(os.path.isfile(self.settingsFileName)):
            self.Settings = pickle.load(open(self.settingsFileName,"rb"))
        else:
            self.Settings = SettingsInfo()

    def saveSettings(self):
        pickle.dump(self.Settings, open(self.settingsFileName, "w+b"), 2)

    def extractLists(self):
        self.data[0]


    def plotter(self, valuesInXAxis, valuesInYAxis, plotsSoFar, generalLabelForLeyend, yAxis):
    #print "the x values are:", valuesInXAxis
        sizeMe=15
        npArrayOfXValues = numpy.array(valuesInXAxis)
        yAxis.plot(valuesInXAxis, valuesInYAxis, 'k'+self.arrayOfPlotCharacters[plotsSoFar], color=self.fontColorList[self.Settings.color], label=generalLabelForLeyend, lw=sizeMe/4, ms=sizeMe)
        yAxis.plot(valuesInXAxis, valuesInYAxis, lw=sizeMe/4, ms=sizeMe)
        if self.Settings.approximation:
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

    def LinesDrawer(self, matrixOfValues, labelForLegend, plotsSoFar, yAxis, beginningXValue = 0):
    #print "the matrix is", matrixOfValues
        Averages, Minimums, Maximums, StandardDeviations = self.LinesGenerator(matrixOfValues)
        arrayOfXValues = range(beginningXValue, beginningXValue + len(Averages))
        ticker = self.arrayOfPlotCharacters[plotsSoFar]
        self.plotter(arrayOfXValues, Averages, plotsSoFar, labelForLegend, yAxis)
        if self.Settings.ploteRanges:
            lowRange  = [a - b for a, b in zip(Averages, Minimums)]
            highRange = [a - b for a, b in zip(Maximums, Averages)]
            pylab.errorbar(arrayOfXValues, Averages, yerr= [lowRange, highRange])
        if self.Settings.plotStandDev:
            lowDev  = [a - b for a, b in zip(Averages, StandardDeviations)]
            highDev = [a + b for a, b in zip(Averages, StandardDeviations)]
            pylab.fill_between(arrayOfXValues, highDev, lowDev, facecolor='grey', alpha=0.5, )
        plotsSoFar = plotsSoFar + 1
        return(plotsSoFar)



    def LinesGenerator(self, matrixOfValues):

        generationsProcessed = 0
        Averages           = []
        Minimums           = []
        Maximums           = []
        StandardDeviations = []
        while generationsProcessed < len(matrixOfValues):
            arrayOfASingleGeneration   = matrixOfValues[generationsProcessed]
            npArrayOfASingleGeneration = numpy.array(arrayOfASingleGeneration)
            Averages.append(numpy.mean(npArrayOfASingleGeneration))
            # Minimums.append(numpy.min(npArrayOfASingleGeneration))
            # Maximums.append(numpy.max(npArrayOfASingleGeneration))
            StandardDeviations.append(numpy.std(npArrayOfASingleGeneration))
            generationsProcessed = generationsProcessed + 1
        return (Averages, Minimums, Maximums, StandardDeviations)
    
    def PutIntoBigMatrixFromFile(self, newArray, newArrayPos, matrixOfAllValues):
        # precondition: the arrays are of the same size
        entriesToProcess = len(newArray)
        processedAlready = 0
        while (processedAlready < entriesToProcess):
            while processedAlready >= len(matrixOfAllValues):
                matrixOfAllValues.append([])
            matrixOfAllValues[processedAlready].append(float(newArray[newArrayPos][processedAlready]))
            processedAlready    = processedAlready + 1
        return(matrixOfAllValues)

    def PutIntoBigMatrix(self, newArray, matrixOfAllValues):
        # precondition: the arrays are of the same size
        entriesToProcess = len(newArray)
        processedAlready = 0
        while (processedAlready < entriesToProcess):
            while processedAlready >= len(matrixOfAllValues):
                matrixOfAllValues.append([])
            matrixOfAllValues[processedAlready].append(float(newArray[processedAlready]))
            # print newArray[processedAlready]
            # print matrixOfAllValues[processedAlready]
            processedAlready    = processedAlready + 1
        return(matrixOfAllValues)

    def SubstractArrays(self, A1, A2):
        A3 = []
        # print A1
        # print A2
        thisIndexNext = 0
        while thisIndexNext < len(A1):
            nextElement = A1[0][thisIndexNext] - A2[0][thisIndexNext]
            A3.append(nextElement)
            thisIndexNext = thisIndexNext + 1
        return (A3)

    def DivideArrays(self, A1, A2):
        A3 = []
        thisIndexNext = 0
        while thisIndexNext < len(A1):
            nextElement = A1[0][thisIndexNext] / A2[0][thisIndexNext]
            A3.append(nextElement)
            thisIndexNext = thisIndexNext + 1
        return (A3)

    def ProcessArrayToMatirx(self, array, intoThisMatrix):
        for currentLine in array:
            if isinstance(currentLine, list):
                print "isList"
                currentValues = currentLine
            else:
                currentValues = [currentLine]
            # divide it into elements, based on spaces
            # currentValues = currentLine.split()
            # we now have the data in an array, but they are in "run first" order.
            # we need to turn it into a "generation first" order.
            # storing them into the matrix will do that work.
            self.PutIntoBigMatrix(currentValues, intoThisMatrix)
        return(intoThisMatrix)

    # def ReadDataFromFile(a, b, c, d):
    #     userAnswer = raw_input("Enter file name:")
    #     fileHandle = open(userAnswer)
    #     fileAsArray = fileHandle.readlines()
    #     fileHandle.close()
    #     ProcessFromHereToHere(fileAsArray, "Bests", "Averages", a)
    #     ProcessFromHereToHere(fileAsArray, "Averages", "Genetic Differences", b)
    #     ProcessFromHereToHere(fileAsArray, "Genetic Differences", "Phenotypic Differences", c)
    #     ProcessFromHereToHere(fileAsArray, "Phenotypic Differences", "End", d)
    #     return(a, b, c, d)
    
    def graph(self):
        # arrayOfPlotCharacters = ['o', 'D','+','*','0','1','2','3','4','5','>','<','^','|','d']
# these are the characters that define how the plot lines will look like.
# if there are more data sets than characters here, add more lines, or modify the code
# so that it loops around.
# these control characters can be found at http://www.loria.fr/~rougier/teaching/matplotlib/#line-styles
        arrayOfPlotCharacters = ['o', 'D','*','+','X','0','1','2','3','4','5','>','<','^','|','d']
        plotsSoFar      = 0 # so that we know which control character to use for the lines.
        fig, ax1 = pylab.subplots()
        ax2 = ax1.twinx()
        if self.Settings.fitnessOnYAxis:
            fitnessAxis   = ax2
            diversityAxis = ax1
        else:
            fitnessAxis   = ax1
            diversityAxis = ax2
        # keepGettingData = True
        for datSet in self.data: # this loop controls how many lines are going to be drawn in the plot.
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
            labelForBests ="_Best"
            labelForAverages ="_Average"
            labelForGeneticDiversities ="_Genetic_Diversity"
            labelForPhenotypicDiversities ="_Phenotypic_Diversity"
            labelForDiversityDifference ="_difference"
            labelForDiversityRatio      ="_ration"
            # for i in self.data:
            self.ProcessArrayToMatirx(datSet[0], bigArrayOfBests)
            # self.PutIntoBigMatrix(i[0], bigArrayOfBests)
            # print "Bests"
            self.ProcessArrayToMatirx(datSet[1], bigArrayOfAverages)
            # print "Averages"
            self.ProcessArrayToMatirx(datSet[2], bigArrayOfGeneticDiversities)
            # print "Genetic"
            self.ProcessArrayToMatirx(datSet[3], bigArrayOfPhenotypicDiversities)
                # print "Phenotypic"
            arrayOfXValues = [x for x in range(len(matrixForBests))]
            arrayOfDiversityDifferences = self.SubstractArrays(bigArrayOfGeneticDiversities, bigArrayOfPhenotypicDiversities)
            arrayOfDiversityRatios      = self.DivideArrays(bigArrayOfGeneticDiversities, bigArrayOfPhenotypicDiversities)
            self.PutIntoBigMatrix(arrayOfDiversityDifferences, matrixForDiversityDifferences)
            self.PutIntoBigMatrix(arrayOfDiversityRatios, matrixForDiversityRatios)
            if self.Settings.plotGenDiversity:
                plotsSoFar = self.LinesDrawer(matrixForGeneticDiversities, labelForGeneticDiversities, plotsSoFar, diversityAxis, arrayOfXValues[0])
            if self.Settings.plotPhenodiversity:
                plotsSoFar = self.LinesDrawer(matrixForPhenotypicDiversities, labelForPhenotypicDiversities, plotsSoFar, diversityAxis, arrayOfXValues[0])
            if self.Settings.comparegp:
                print "Diversity differences..."
                plotsSoFar = self.LinesDrawer(matrixForPhenotypicDiversities, labelForDiversityDifference, plotsSoFar, diversityAxis, arrayOfXValues[0])
                plotsSoFar = plotsSoFar - 1
                print "Diversity ratios..."
                plotsSoFar = self.LinesDrawer(matrixForPhenotypicDiversities, labelForDiversityRatio, plotsSoFar, diversityAxis, arrayOfXValues[0])
                plotsSoFar = plotsSoFar - 1
            if self.Settings.plotBestVals:
                plotsSoFar = self.LinesDrawer(matrixForBests, labelForBests, plotsSoFar, fitnessAxis, arrayOfXValues[0])
            if self.Settings.plotAverages:
               plotsSoFar = self.LinesDrawer(matrixForAverages, labelForAverages, plotsSoFar, fitnessAxis, arrayOfXValues[0])
            # keepGettingData = False
        sizeMe = self.fontSizeList[self.Settings.size]
        fitnessAxis.set_ylabel('fitness score', fontsize=sizeMe)
        ax1.set_xlabel("generation", fontsize=sizeMe)
        diversityAxis.set_ylabel('diversity', fontsize=sizeMe)
        ax2.legend(loc='upper right', fancybox=True, prop={'size':sizeMe})#.get_frame().set_alpha(0.5)
        ax2.tick_params(axis='both', which='major', labelsize=sizeMe)
        ax1.tick_params(axis='both', which='major', labelsize=sizeMe)
        #ax1.legend(loc='upper left' , fancybox=True, prop={'size':sizeMe}).get_frame().set_alpha(0.5)
        pylab.show()
