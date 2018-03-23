import sys
import getopt
import os
import math
import operator
import collections
import random

class Perceptron:
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
    """Perceptron initialization"""
    #in case you found removing stop words helps.
    self.stopList = set(self.readFile('../data/english.stop'))
    self.numFolds = 10
    self.vocabulary = collections.defaultdict(lambda:0)
    self.final_weight = collections.defaultdict(lambda:0)
    self.final_bias = 0
    self.w_0 = collections.defaultdict(lambda:0)
    self.w_1 = collections.defaultdict(lambda:0)



  #############################################################################
  # TODO TODO TODO TODO TODO 
  # Implement the Perceptron classifier with
  # the best set of features you found through your experiments with Naive Bayes.

  def classify(self, words):
    """ TODO
      'words' is a list of words to classify. Return 'pos' or 'neg' classification.
    """
    # for word in words:


    # Write code here
    self.weight_test = 0.0
    self.words_collection = collections.defaultdict(lambda:0)
    for word in words:
      self.words_collection[word] += 1.0
    # for key,value in self.vocabulary.iteritems():
    #   if key in words:
    #     self.words[key] += 1.0
    #   else:
    #     self.words[key] = 0.0
    for key, value in self.words_collection.iteritems():
      self.weight_test = self.weight_test + self.words_collection[key] * self.final_weight[key]
    self.weight_test += self.final_bias
    # print "self.weight_test", self.weight_test
    if self.weight_test >= 0.0:
      return 'pos'
    return 'neg'

  # def training(self, iterations):
    

  def addExample(self, klass, words):
    """
     * TODO
     * Train your model on an example document with label klass ('pos' or 'neg') and
     * words, a list of strings.
     * You should store whatever data structures you use for your classifier 
     * in the Perceptron class.
     * Returns nothing
    """
    for word in words:
      self.vocabulary[word] += 1.0



    # Write code here

    pass
  
  def train(self, split, iterations):
      """
      * TODO 
      * iterates through data examples
      * TODO 
      * use weight averages instead of final iteration weights
      """
      for i in range(iterations):
        for example in split.train:
          words = example.words
          self.addExample(example.klass, words)
        # print len(self.vocabulary)
        for key,value in self.vocabulary.iteritems():
          self.w_0[key] = 0.0
          self.w_1[key] = 0.0
        self.c = 1.0
        self.b_0 = 0.0
        self.b_a = 0.0
        random.shuffle(split.train)
        for example in split.train:
          word_vec = collections.defaultdict(lambda:0)
          y_n = 1.0 if example.klass == 'pos' else -1.0
          # print "y_n",y_n
          for word in example.words:
            word_vec[word] += 1
          prod = 0.0
          for key,value in word_vec.iteritems():
            prod = prod + word_vec[key] * self.w_0[key]
          prod = y_n*(prod + self.b_0)
          if prod <= 0.0:
            for key, value in word_vec.iteritems():
              self.w_0[key] = self.w_0[key] + y_n * word_vec[key]
            self.b_0 = self.b_0 + y_n
            for key, value in word_vec.iteritems():
              self.w_1[key] = self.w_1[key] + self.c * y_n * word_vec[key]
            self.b_a = self.b_a + self.c * y_n
          self.c = self.c + 1.0
      for key, value in self.w_0.iteritems():
        self.final_weight[key] = self.w_0[key] - self.w_1[key]/self.c
      self.final_bias = self.b_0 - self.b_a/self.c

       
      

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
    posTrainFileNames = os.listdir('%s/pos/' % trainDir)
    negTrainFileNames = os.listdir('%s/neg/' % trainDir)
    for fileName in posTrainFileNames:
      example = self.Example()
      print '%s/pos/%s' % (trainDir, fileName)
      example.words = self.readFile('%s/pos/%s' % (trainDir, fileName))
      example.klass = 'pos'
      split.train.append(example)
    for fileName in negTrainFileNames:
      example = self.Example()
      example.words = self.readFile('%s/neg/%s' % (trainDir, fileName))
      example.klass = 'neg'
      split.train.append(example)
    return split


  def crossValidationSplits(self, trainDir):
    """Returns a lsit of TrainSplits corresponding to the cross validation splits."""
    splits = [] 
    posTrainFileNames = os.listdir('%s/pos/' % trainDir)
    negTrainFileNames = os.listdir('%s/neg/' % trainDir)
    #for fileName in trainFileNames:
    for fold in range(0, self.numFolds):
      split = self.TrainSplit()
      for fileName in posTrainFileNames:
        example = self.Example()
        example.words = self.readFile('%s/pos/%s' % (trainDir, fileName))
        example.klass = 'pos'
        if fileName[2] == str(fold):
          split.test.append(example)
        else:
          split.train.append(example)
      for fileName in negTrainFileNames:
        example = self.Example()
        example.words = self.readFile('%s/neg/%s' % (trainDir, fileName))
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

def test10Fold(args):
  pt = Perceptron()
  
  iterations = int(args[1])
  splits = pt.crossValidationSplits(args[0])
  avgAccuracy = 0.0
  fold = 0
  for split in splits:
    classifier = Perceptron()
    accuracy = 0.0
    classifier.train(split,iterations)
  
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
    
    
def classifyDir(trainDir, testDir,iter):
  classifier = Perceptron()
  trainSplit = classifier.trainSplit(trainDir)
  iterations = int(iter)
  classifier.train(trainSplit,iterations)
  testSplit = classifier.trainSplit(testDir)
  #testFile = classifier.readFile(testFilePath)
  accuracy = 0.0
  for example in testSplit.train:
    words = example.words
    guess = classifier.classify(words)
    if example.klass == guess:
      accuracy += 1.0
  accuracy = accuracy / len(testSplit.train)
  print '[INFO]\tAccuracy: %f' % accuracy
    
def main():
  (options, args) = getopt.getopt(sys.argv[1:], '')
  
  if len(args) == 3:
    classifyDir(args[0], args[1], args[2])
  elif len(args) == 2:
    test10Fold(args)

if __name__ == "__main__":
    main()
