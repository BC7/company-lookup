import csv

class CsvManager(object):

    def __init__(self, file_path):
        self.file = file_path

    def getOrgs(self):
        data = []
        with open(self.file, newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in spamreader:
                data.append(row)
            return data
            # print(', '.join(row)+"\n\n")