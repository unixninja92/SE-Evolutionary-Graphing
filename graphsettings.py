import matplotlib.pyplot as plt
import pickle
import pylab
import glob
import string
import os.path
import os

class SettingsInfo:
    def __init__(self):
        self.aproximaion = False
        self.ploteRanges = True
        self.plotStandDev = False
        self.fitnessOnYAxis = True
        self.plotGenDiversity = False
        self.plotPhenodiversity = False
        self.comparegp = False
        self.plotBestVals = False
        self.plotAverages = False

    def setConfig(self, aproximaion, ploteRanges, plotStandDev, fitnessOnYAxis, plotGenDiversity, plotPhenodiversity, comparegp, plotBestVals, plotAverages):
        self.aproximaion = aproximaion
        self.ploteRanges = ploteRanges
        self.plotStandDev = plotStandDev
        self.fitnessOnYAxis = fitnessOnYAxis
        self.plotGenDiversity = plotGenDiversity
        self.plotPhenodiversity = plotPhenodiversity
        self.comparegp = comparegp
        self.plotBestVals = plotBestVals
        self.plotAverages = plotAverages


class GraphSettings:
    def __init__(self):
        self.settingsFileName = "lastGraphSettings.pkl"
        self.loadSettings()

    def loadSettings(self):
        if(os.path.isfile(self.settingsFileName)):
            self.Settings = pickle.load(open(self.settingsFileName),"rb")
        else:
            self.Settings = SettingsInfo()

    def saveSettings(self):
        pickle.dump(self.Settings, open(self.settingsFileName, "w+b"), 2)


    def plotter(self, valuesInXAxis, valuesInYAxis, plotsSoFar, generalLabelForLeyend, yAxis):
    #print "the x values are:", valuesInXAxis
        sizeMe=15
        npArrayOfXValues = numpy.array(valuesInXAxis)
        yAxis.plot(valuesInXAxis, valuesInYAxis, arrayOfPlotCharacters[plotsSoFar], label=generalLabelForLeyend, lw=sizeMe/4, ms=sizeMe)
        yAxis.plot(valuesInXAxis, valuesInYAxis, lw=sizeMe/4, ms=sizeMe)
        if self.aproximaion:
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
        Averages, Minimums, Maximums, StandardDeviations = LinesGenerator(matrixOfValues)
        arrayOfXValues = range(beginningXValue, beginningXValue + len(Averages))
        ticker = arrayOfPlotCharacters[plotsSoFar]
        plotter(arrayOfXValues, Averages, plotsSoFar, labelForLegend, yAxis)
        if self.ploteRanges:
            lowRange  = [a - b for a, b in zip(Averages, Minimums)]
            highRange = [a - b for a, b in zip(Maximums, Averages)]
            pylab.errorbar(arrayOfXValues, Averages, yerr= [lowRange, highRange])
        if self.plotStandDev:
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
            Minimums.append(numpy.min(npArrayOfASingleGeneration))
            Maximums.append(numpy.max(npArrayOfASingleGeneration))
            StandardDeviations.append(numpy.std(npArrayOfASingleGeneration))
            generationsProcessed = generationsProcessed + 1
        return (Averages, Minimums, Maximums, StandardDeviations)

    #def savegraphsettings():

     #   if boolean1:
    
    
    def apply(self):
        # arrayOfPlotCharacters = ['o', 'D','+','*','0','1','2','3','4','5','>','<','^','|','d']
# these are the characters that define how the plot lines will look like.
# if there are more data sets than characters here, add more lines, or modify the code
# so that it loops around.
# these control characters can be found at http://www.loria.fr/~rougier/teaching/matplotlib/#line-styles
        arrayOfPlotCharacters = ['o', 'D','*','+','X','0','1','2','3','4','5','>','<','^','|','d']
        plotsSoFar      = 0 # so that we know which control character to use for the lines.
        fig, ax1 = pylab.subplots()
        ax2 = ax1.twinx()
        if self.fitnessOnYAxis:
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
            labelForBests ="_Best"
            labelForAverages ="_Average"
            labelForGeneticDiversities ="_Genetic_Diversity"
            labelForPhenotypicDiversities ="_Phenotypic_Diversity"
            labelForDiversityDifference ="_difference"
            labelForDiversityRatio      ="ration"
            if self.plotGenDiversity:
                plotsSoFar = LinesDrawer(matrixForGeneticDiversities, labelForGeneticDiversities, plotsSoFar, diversityAxis, arrayOfXValues[0])
            if self.plotPhenodiversity:
                plotsSoFar = LinesDrawer(matrixForPhenotypicDiversities, labelForPhenotypicDiversities, plotsSoFar, diversityAxis, arrayOfXValues[0])
            if self.comparegp:
                plotsSoFar = LinesDrawer(matrixForPhenotypicDiversities, labelForDiversityDifference, plotsSoFar, diversityAxis, arrayOfXValues[0])
                plotsSoFar = plotsSoFar - 1
                plotsSoFar = LinesDrawer(matrixForPhenotypicDiversities, labelForDiversityRatio, plotsSoFar, diversityAxis, arrayOfXValues[0])
                plotsSoFar = plotsSoFar - 1
            if self.plotBestVals:
                plotsSoFar = LinesDrawer(matrixForBests, labelForBests, plotsSoFar, fitnessAxis, arrayOfXValues[0])
            if booleanaverages:
               plotsSoFar = LinesDrawer(matrixForAverages, labelForAverages, plotsSoFar, fitnessAxis, arrayOfXValues[0])
            keepGettingData = False
        sizeMe = 50
        fitnessAxis.set_ylabel('fitness score', fontsize=sizeMe)
        ax1.set_xlabel("generation", fontsize=sizeMe)
        diversityAxis.set_ylabel('diversity', fontsize=sizeMe)
        ax2.legend(loc='upper right', fancybox=True, prop={'size':sizeMe}).get_frame().set_alpha(0.5)
        ax2.tick_params(axis='both', which='major', labelsize=sizeMe)
        ax1.tick_params(axis='both', which='major', labelsize=sizeMe)
        #ax1.legend(loc='upper left' , fancybox=True, prop={'size':sizeMe}).get_frame().set_alpha(0.5)
        pylab.show()






#booleans needed as checkboxs:
#show approximation for this data?
#plot ranges for this data?
#plot standard deviation?
#genetic diversity
#phenotipic diversity
#compare genetic and phenotipic diversity?
#best values?
#averages?
#What do you prefer in the second Y axis, (F)itness values or (d)iversity
