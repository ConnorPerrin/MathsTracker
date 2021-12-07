import json
import random

from pandas import *

#import pandas as pd
import matplotlib.pyplot as plt
import pandas
import seaborn as sb
import numpy as np

class MathsTracker:
    def __init__(self):
        print("Welcome to MathsTracker")
        
        self.limits = 50

        #self.createDefaultJSON()

        self.loadJSON()
        self.commands()
        self.run()
        self.saveJSON()
        self.createGraphs()

    def loadJSON(self):
        with open('../data/data.json') as json_file:
            self.data = json.load(json_file)
        
    def saveJSON(self):
        with open('../data/data.json', 'w') as outfile:
            json.dump(self.data, outfile, indent=4)

    def commands(self):
        self.range = input("Please choose the max range (0-50): ")

        # self.timed = input("Do you want this session to be timed (Y/n): ")
        # if(self.timed.lower() == 'y'):
        #     self.sessionTime = input("How long do you want this session to last: ")

        self.ready = 'n'
        while(self.ready == 'n'):
            self.ready = input("Are you ready to start (Y/n): ")
            

    def createDefaultJSON(self):
        self.data = {}
        for x in range(1, self.limits+1):
            self.data[x] = {}
            for y in range(1, self.limits+1):
                self.data[x][y] = {'numCorrect': 0, 'numSeen': 0}

    def run(self):
        while(True):
            left = random.randint(1, int(self.range))
            right = random.randint(1, int(self.range))

            answer = input(str(left) + " * " + str(right) + " = ")

            if(answer == "quit"):
                break
            else:
                self.checkAnswer(left, right, answer)

        self.saveJSON()

    def checkAnswer(self, left, right, answer):
        strLeft = str(left)
        strRight = str(right)

        self.data[strLeft][strRight]['numSeen'] += 1

        if(int(answer) == (left*right)):
            print("Correct!")
            self.data[strLeft][strRight]['numCorrect'] += 1
        else:
            print("Incorrect: " + str(left*right))
        
    def getPercentage(self, data):
            if(data['numSeen'] == 0):
                return 0
            else:
                return (data['numCorrect'] / data['numSeen'])*100

    def createGraphs(self):
        image_ranges = [10,20,30,40,50]
        label_skips = [1, 1, 5, 5, 10]

        for (heat_range, skip_amount) in zip(image_ranges, label_skips):
            plt.figure()
            plt.title("Percentage accuracy for 1-"+str(heat_range))
            ax = sb.heatmap(self.get2DArray(heat_range), xticklabels=range(1, heat_range+1), yticklabels=range(1, heat_range+1))
            ax.xaxis.set_ticks_position('top')

            [l.set_visible(False) for (i,l) in enumerate(ax.xaxis.get_ticklabels()) if i != 0 and (i+1) % skip_amount != 0]
            [l.set_visible(False) for (i,l) in enumerate(ax.yaxis.get_ticklabels()) if i != 0 and (i+1) % skip_amount != 0]

            plt.savefig('../images/heatmap_range_'+str(heat_range)+'.png')
            plt.close('all')

    def get2DArray(self, heat_range):
        numpy_data = np.zeros((heat_range, heat_range), dtype=np.float32)

        for row in range(1, heat_range):
            for col in range(1, heat_range):
                numpy_data[row][col] = self.getPercentage(self.data[str(row)][str(col)])
        
        return numpy_data 

def run():
    MathsTracker()

if __name__ == "__main__":
    run()