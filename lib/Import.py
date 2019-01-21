import os


def getListOfFiles(dirName):
    listOfFile = os.listdir(dirName)
    allFiles = list()
    for entry in listOfFile:
        fullPath = os.path.join(dirName, entry)
        if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfFiles(fullPath)
        else:
            allFiles.append(fullPath)
    return allFiles


def main():
    dirName = r'C:\Users\Gido Scherpenhuizen\Documents\,School\IPFRCHT'
    listOfFiles = getListOfFiles(dirName)
    print (listOfFiles)


if __name__ == "__main__":
    main()
