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
    dirName = r'D:\School\2e Jaar\IPFJURI\Images'
    listOfFiles = getListOfFiles(dirName)
    print(listOfFiles)


if __name__ == "__main__":
    main()
