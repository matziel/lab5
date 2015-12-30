import csv
import random
import math
import numpy

 
def loadCsv(filename):
    """zaimportuj plik .csv jako listę list liczb typu float"""
    lines = csv.reader(open(filename, "r"))
    dataset = list(lines)
    for i in range(len(dataset)):
        for x_i, x in enumerate(dataset[i]):
            dataset[i][x_i] = float(x)
    return dataset

 
def testLoadCsv():
    filename = 'pima-indians-diabetes.data.csv'
    dataset = loadCsv(filename)
    assert(len(dataset))
    print('Loaded data file {0} with {1} rows').format(filename, len(dataset))

    
def splitDataset(dataset, splitRatio):
    """podziel zbiór danych na zbiory: uczący i testowy"""
    trainSet = dataset[:]
    testSet = []
    while len(trainSet)>len(dataset)*splitRatio:
        ind =  random.randint(0,len(trainSet)-1)
        testSet.append(trainSet[ind])
        trainSet.remove(trainSet[ind])
    return [trainSet, testSet]

    
def testSplitDataset():
    dataset = [[1], [2], [3], [4], [5]]
    splitRatio = 0.67
    train, test = splitDataset(dataset, splitRatio)
    assert(train)
    assert(test)
    print('Split {0} rows into train with {1} and test with {2}').format(len(dataset), train, test)

    
def separateByClass(dataset):
    """Rozdziel zbiór uczący według klasy (v[-1]) przypisanej wektorowi cech v"""
    separated = {}
    for v in dataset:
        if v[-1] not in separated:
            separated[v[-1]] = []
    for i in separated:
        separated[i] = [v for v in dataset if v[-1]==i]
    return separated


def testSeparateByClass(): 
    dataset = [[1,20,1], [2,21,0], [3,22,1]]
    separated = separateByClass(dataset)
    assert(separated)
    print('Separated instances: {0}').format(separated)


def mean(numbers):
    """Oblicz średnią arytmetyczną z listy danych"""
    return numpy.mean(numbers)

    
def stdev(numbers):
    """Oblicz odchylenie standardowe z listy danych"""
    avg = mean(numbers)
    variance = sum([pow(x-avg,2) for x in numbers])/float(len(numbers)-1)
    return math.sqrt(variance)

    
def testMeanAndStdev():
    numbers = [1,2,3,4,5]
    assert(mean)
    assert(stdev)
    print('Summary of {0}: mean={1}, stdev={2}').format(numbers, mean(numbers), stdev(numbers))

 
def summarize(dataset):
    summaries = [(mean(attribute), stdev(attribute)) for attribute in zip(*dataset)]
    return summaries

    
def testSummarize(dataset):
    dataset = [[1,20,0], [2,21,1], [3,22,0]]
    summary = summarize(dataset)
    assert(summary)
    print('Attribute summaries: {0}').format(summary)

 
def summarizeByClass(dataset):
    separated = separateByClass(dataset)
    summaries = {}
    for classValue, instances in separated.iteritems():
        summaries[classValue] = summarize(instances)
    return summaries

 
def calculateProbability(x, mean, stdev):
    """Oblicz prawdopodobieństwo"""
    exponent = math.exp(-(math.pow(x-mean,2)/(2*math.pow(stdev,2))))
    return (1 / (math.sqrt(2*math.pi) * stdev)) * exponent

def testCalculateProbability():
    x = 71.5
    mean = 73
    stdev = 6.2
    probability = calculateProbability(x, mean, stdev)
    assert(probability)
    print('Probability of belonging to this class: {0}').format(probability)

def calculateClassProbabilities(summaries, inputVector):
    """Oblicz prawdopodobieństwo występowania klas"""
    probabilities = {}
    for klasa in summaries:
        for nrkol in range(len(inputVector)-1):
            if klasa not in probabilities:
                probabilities[klasa] = []
            (med, stdv) = summaries[klasa][nrkol]
            probabilities[klasa].insert(nrkol, calculateProbability(inputVector[nrkol], med, stdv))
    for klasa in probabilities:
        probabilities[klasa] = numpy.product(probabilities[klasa])
    return probabilities

def testCalculateClassProbabilities():    
    summaries = {0:[(1, 0.5), (2, 0.2)], 1:[(20, 5.0), (70, 3.0)]}
    inputVector = [1.1, 2.1, '?']
    probabilities = calculateClassProbabilities(summaries, inputVector)
    assert(probabilities)
    print('Probabilities for each class: {0}').format(probabilities)
			
def predict(summaries, inputVector):
    """Dokonaj predykcji jednego elementu zbioru danych wg danych prawdopodobieństw"""
    probabilities = calculateClassProbabilities(summaries, inputVector)
    bestLabel, bestProb = None, -1
    bestLabel = max(probabilities, key=probabilities.get)
    return bestLabel
    
def testPredict():
    summaries = {'A':[(1, 0.5)], 'B':[(20, 5.0)]}
    inputVector = [1.1, '?']
    result = predict(summaries, inputVector)
    assert(result == 'A')
    print('Prediction: {0}').format(result)
 
def getPredictions(summaries, testSet):
    """Dokonaj predykcji dla wszystkich elementów w zbiorze danych"""
    predictions = []
    for i in testSet:
        predictions.append(predict(summaries, i))
    return predictions

def testGetPredictions():
    summaries = {'A':[(1, 0.5)], 'B':[(20, 5.0)]}
    testSet = [[1.1, '?'], [19.1, '?']]
    predictions = getPredictions(summaries, testSet)
    print('Predictions: {0}').format(predictions)
    
def getAccuracy(testSet, predictions):
    """Oblicz dokładność przewidywań"""
    correct = 0
    for i in range(len(testSet)):
        if testSet[i][-1] == predictions[i]:
            correct += 1
    return (correct/float(len(testSet))) * 100.0

def testGetAccuracy():
    testSet = [[1,1,1,'a'], [2,2,2,'a'], [3,3,3,'b']]
    predictions = ['a', 'a', 'a']
    accuracy = getAccuracy(testSet, predictions)
    print('Accuracy: {0}').format(accuracy)
    
def main():
    filename = 'pima-indians-diabetes.data.csv'
    splitRatio = 0.67
    dataset = loadCsv(filename)
    trainingSet, testSet = splitDataset(dataset, splitRatio)
    print('Split {0} rows into train={1} and test={2} rows').format(len(dataset), len(trainingSet), len(testSet))
    # prepare model
    summaries = summarizeByClass(trainingSet)
    # test model
    predictions = getPredictions(summaries, testSet)
    accuracy = getAccuracy(testSet, predictions)
    print('Accuracy: {0}%').format(accuracy)

main()
