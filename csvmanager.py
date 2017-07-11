import csv

class CsvManager(object):

    def __init__(self, file_path):
        self.file = file_path
        self.file_header = []
    def getOrgs(self):
        data = []
        with open(self.file, newline='') as csvfile:
            csvreader = csv.reader(csvfile, delimiter=',', quotechar='|')

            for row in csvreader:
                data.append(row)


            res = {}
            for i in data:
                res[i[0]] = (i[1:])

            # will add the header again when updated the file
            # iterating over keys in url_scrape without the header
            self.file_header = res.pop("Company Name")

        csvfile.close()
        return res

    def updateCSV(self, data):
        with open(self.file, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=',', quotechar='|')

            # re-add header as the first row
            csvwriter.writerow([self.file_header[0],self.file_header[1],self.file_header[2],self.file_header[3],self.file_header[4],self.file_header[5],self.file_header[6]])#,self.file_header[7],self.file_header[8]])
            for key in data.keys():
                print(str(key) + "\n")
                csvwriter.writerow([key , str(data[key][0]) , data[key][1] , data[key][2] , data[key][3] , data[key][4] , data[key][5] , data[key][6] ]) # , data[key][7] ])
        csvfile.close()