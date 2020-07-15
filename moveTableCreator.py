import pickle

def createFile(filename, data):
    exportDict = open(filename, "wb")
    pickle.dump(data, exportDict)
    exportDict.close()

def addData(filename):
    exportDict = open(filename, "rb")
    dict1 = pickle.load(exportDict)
    exportDict.close()
    dict1['a'] = "HelloWorld"
    dict1['b'] = [0, 1, 5, 6]
    createFile(filename, dict1)

def printData(filename):
    exportDict = open(filename, "rb")
    dict1 = pickle.load(exportDict)
    exportDict.close()
    print(len(dict1))
    print(dict1.keys())
    print(dict1.values())
# printData("3size3inRow")
# createFile("3size3inRow", {})
# printData("3size3inRow")

# createFile("4size4inRow", {})
# printData("4size4inRow") 

# createFile("5size5inRow", {})
# printData("5size5inRow") 