
def makecase(path, name):
    print(path + name)
    Settings.makeDefaultConfig()
    db = Sqlite.Sqlite(path, name)