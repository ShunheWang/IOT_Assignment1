from generateScatterPlot import scatterGraph
from generateLinePlot import lineGraph


#Choose wanted analysis graph
class analyticsGraph:
    def chooseGraph(self):
        chooseIndex = input("Please choose graph " +
                            "(1. Scatter plot, 2. Line Plot): ")
        if(chooseIndex == '1'):
            print("Scatter graph is generated successfully")
            createScatter = scatterGraph()
            createScatter.createGrph()
        elif(chooseIndex == '2'):
            print("Line graph is generated successfully")
            createLine = lineGraph()
            createLine.createGrph()


ag = analyticsGraph()
ag.chooseGraph()
