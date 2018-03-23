import sys
import getopt
import os
import math
import operator
import collections
import re

class Turney:
  class TrainSplit:
    """Represents a set of training/testing data. self.train is a list of Examples, as is self.test. 
    """
    def __init__(self):
      self.train = []
      self.test = []

  class Example:
    """Represents a document with a label. klass is 'pos' or 'neg' by convention.
       words is a list of strings.
    """
    def __init__(self):
      self.klass = ''
      self.words = []


  def __init__(self):
    self.numFolds = 10
    self.indexes = {}
    self.indexes["great"] = collections.defaultdict(lambda: 0)
    self.indexes["poor"] = collections.defaultdict(lambda: 0)
    self.great_count = 0
    self.poor_count = 0
    self.phrase_count = 0

  

  



  def classify(self, words):
    ''' 
      Calculate semantic orientation of test data
      classify whether pos or neg
    '''

    semantic_orientation = 0.0
    count = 0
    #regular expression for identfying phrases
    reg_exp = "((\w+)_JJ_\S+ (\w+)_(NN|NNS)_\S+)|((\w+)_(RB|RBR|RBS)_\S+ (\w+)_(JJ)_\S+ (\w+)_(?!NN|NNS).*_\S+)|((\w+)_(JJ)_\S+ (\w+)_(JJ)_\S+ (\w+)_(?!NN|NNS).*_\S+)|((\w+)_(NN|NNS)_\S+ (\w+)_(JJ)_\S+ (\w+)_(?!NN|NNS).*_\S+)|((\w+)_(RB|RBR|RBS)_\S+ (\w+)_(VB|VBD|VBG|VBS)_\S+)"
    # calculating semantic orientation. Adding 0.01 for each hit near great and near poor.
    for i in range(len(words)-2):
      string = " ".join([words[i], words[i+1], words[i+2]])
      m = re.match(reg_exp, string)
      if m:
        if self.indexes["great"][(words[i], words[i+1])] == 0 and self.indexes["poor"][(words[i], words[i+1])] == 0:
          continue
        semantic_orientation += math.log(float((self.indexes["great"][(words[i], words[i+1])] + 0.01) * self.poor_count)/float((self.indexes["poor"][(words[i], words[i+1])] + 0.01) * self.great_count))
        count += 1
    if count == 0:
      avg_semantic_orientation = 0.0
    else:
      avg_semantic_orientation = semantic_orientation/count

    # calculating polarity
    if avg_semantic_orientation > 0.0:
      return 'pos'
    else:
      return 'neg'  

  def addExample(self, klass, words):

    ''' Make regexp
    Search patterns that match regexp
    count hits for the matched pattern near great and poor
    count hits for great and poor
    '''

    #regular expression for identifying sentiment phrases
    reg_exp = "((\w+)_JJ_\S+ (\w+)_(NN|NNS)_\S+)|((\w+)_(RB|RBR|RBS)_\S+ (\w+)_(JJ)_\S+ (\w+)_(?!NN|NNS).*_\S+)|((\w+)_(JJ)_\S+ (\w+)_(JJ)_\S+ (\w+)_(?!NN|NNS).*_\S+)|((\w+)_(NN|NNS)_\S+ (\w+)_(JJ)_\S+ (\w+)_(?!NN|NNS).*_\S+)|((\w+)_(RB|RBR|RBS)_\S+ (\w+)_(VB|VBD|VBG|VBS)_\S+)"
    #calculating count of each sentiment phrase near great and poor in self.indexes. Phrases near great
    #are stored in self.indexes['great'] and phrases near poor are stored in self.indexes['poor']
    for i in range(len(words) - 2):
      if "great" in words[i]:
        self.great_count += 1
      if "poor" in words[i]:
        self.poor_count += 1
      string = " ".join([words[i], words[i+1], words[i+2]])
      m = re.match(reg_exp, string)
      length = len(words)
      if m:
        self.phrase_count += 1
        if i < 10:
          list_words = words[0:i+10]
        elif len(words) - 10 < i < len(words):
          list_words = words[i-10:length]
        else:
          list_words = words[i-10:i+10]
        for word in list_words:
          if "great" in word:
            self.indexes["great"][(words[i], words[i+1])] += 1
          if "poor" in word:
            self.indexes["poor"][(words[i], words[i+1])] += 1


  # END TODO (Modify code beyond here with caution)
  #############################################################################
  
  
  def readFile(self, fileName):
    """
     * Code for reading a file.  you probably don't want to modify anything here, 
     * unless you don't like the way we segment files.
    """
    contents = []
    f = open(fileName)
    for line in f:
      contents.append(line)
    f.close()
    result = self.segmentWords('\n'.join(contents)) 
    return result

  
  def segmentWords(self, s):
    """
     * Splits lines on whitespace for file reading
    """
    return s.split()

  
  def trainSplit(self, trainDir):
    """Takes in a trainDir, returns one TrainSplit with train set."""
    split = self.TrainSplit()
    posTrainFileNames = os.listdir('%s/pos_tagged/' % trainDir)
    negTrainFileNames = os.listdir('%s/neg_tagged/' % trainDir)
    for fileName in posTrainFileNames:
      example = self.Example()
      example.words = self.readFile('%s/pos_tagged/%s' % (trainDir, fileName))
      example.klass = 'pos'
      split.train.append(example)
    for fileName in negTrainFileNames:
      example = self.Example()
      example.words = self.readFile('%s/neg_tagged/%s' % (trainDir, fileName))
      example.klass = 'neg'
      split.train.append(example)
    return split

  def train(self, split):
    for example in split.train:
      words = example.words
      if self.FILTER_STOP_WORDS:
        words =  self.filterStopWords(words)
      self.addExample(example.klass, words)


  def crossValidationSplits(self, trainDir):
    """Returns a lsit of TrainSplits corresponding to the cross validation splits."""
    splits = [] 
    posTrainFileNames = os.listdir('%s/pos_tagged/' % trainDir)
    negTrainFileNames = os.listdir('%s/neg_tagged/' % trainDir)
    #for fileName in trainFileNames:
    for fold in range(0, self.numFolds):
      split = self.TrainSplit()
      for fileName in posTrainFileNames:
        example = self.Example()
        example.words = self.readFile('%s/pos_tagged/%s' % (trainDir, fileName))
        example.klass = 'pos'
        if fileName[2] == str(fold):
          split.test.append(example)
        else:
          split.train.append(example)
      for fileName in negTrainFileNames:
        example = self.Example()
        example.words = self.readFile('%s/neg_tagged/%s' % (trainDir, fileName))
        example.klass = 'neg'
        if fileName[2] == str(fold):
          split.test.append(example)
        else:
          split.train.append(example)
      splits.append(split)
    return splits
  
  def filterStopWords(self, words):
    """Filters stop words."""
    filtered = []
    for word in words:
      if not word in self.stopList and word.strip() != '':
        filtered.append(word)
    return filtered

def test10Fold(args, FILTER_STOP_WORDS, BOOLEAN_NB):
  turney = Turney()
  splits = turney.crossValidationSplits(args[0])
  avgAccuracy = 0.0
  fold = 0
  for split in splits:
    classifier = Turney()
    accuracy = 0.0
    for example in split.train:
      words = example.words
      classifier.addExample(example.klass, words)
  
    for example in split.test:
      words = example.words
      guess = classifier.classify(words)
      if example.klass == guess:
        accuracy += 1.0
    accuracy = accuracy / len(split.test)
    avgAccuracy += accuracy
    print '[INFO]\tFold %d Accuracy: %f' % (fold, accuracy) 
    fold += 1
  avgAccuracy = avgAccuracy / fold
  print '[INFO]\tAccuracy: %f' % avgAccuracy
    
    
def classifyDir(FILTER_STOP_WORDS, BOOLEAN_NB, trainDir, testDir):
  classifier = Turney()
  classifier.FILTER_STOP_WORDS = FILTER_STOP_WORDS
  classifier.BOOLEAN_NB = BOOLEAN_NB
  trainSplit = classifier.trainSplit(trainDir)
  classifier.train(trainSplit)
  testSplit = classifier.trainSplit(testDir)
  accuracy = 0.0
  for example in testSplit.train:
    words = example.words
    guess = classifier.classify(words)
    if example.klass == guess:
      accuracy += 1.0
  accuracy = accuracy / len(testSplit.train)
  print '[INFO]\tAccuracy: %f' % accuracy


def main():
  FILTER_STOP_WORDS = False
  BOOLEAN_NB = False
  (options, args) = getopt.getopt(sys.argv[1:], 'fbm')
  if ('-f','') in options:
    FILTER_STOP_WORDS = True
  elif ('-b','') in options:
    BOOLEAN_NB = True
  
  if len(args) == 2:
    classifyDir(FILTER_STOP_WORDS, BOOLEAN_NB,  args[0], args[1])
  elif len(args) == 1:
    test10Fold(args, FILTER_STOP_WORDS, BOOLEAN_NB)

if __name__ == "__main__":
    main()
