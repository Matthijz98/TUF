class Hash:

    import hashlib

    def hashing(self, filename):

        hash = self.hashlib.md5()

        with open(filename, 'rb') as file:
            buffer = file.read()
            hash.update(buffer)
        return hash.hexdigest()

if __name__ == '__main__':
    value = hashing("Voer hier het pad in")
    print(value)
