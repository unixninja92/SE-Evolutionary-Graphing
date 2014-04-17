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
    

    

    
