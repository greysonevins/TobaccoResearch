import requests
import math
import time
import pandas as pd

class TobaccoPLOSData:

    def __init__(self):
        self.plosAPI = "http://api.plos.org/search"
        self.articles = []

        self.start = 1
        self.r = 200
        self.params = {
            "q"     : "title:Tobacco OR abstract:Tobacco OR introduction:Tobacco",
            "start" : self.start,
            "rows"  : self.r
                    }

        self.headers = {"User-Agent" : "student-research-2018"}

        self.numFound = 0

    def get_plos_data(self):
        print("searching PLOS")

        req = requests.get(self.plosAPI, params=self.params, headers=self.headers)

        self.articles.append(req.json())

        time.sleep(1)
        #test if excecption raised?

        self.numFound = req.json()["response"]["numFound"]

        self.get_pages_data()

    def get_pages_data(self):
        print("getting the rest of the PLOS pages")
        for rows in range(1, math.ceil(self.numFound / 200)):
            self.params["start"] = rows * 200
            req = requests.get("http://api.plos.org/search", params=self.params)
            #test if excecption raised?
            self.articles.append(req.json())
            time.sleep(1)


    def refine_plos_data(self):
        print("refining PLOS data into csv")
        docValues = [docs for response in self.articles for docs in response["response"]["docs"]]

        docsPD = pd.DataFrame(docValues)
        docsPD.dropna(subset=["author_display"], inplace=True)
        docsPD.to_csv("data/plosTobacoo.csv")

    def plos_job(self):
        print("starting PLOS API searcb")
        self.get_plos_data()
        self.refine_plos_data()
        print("finished")

if __name__ == "__main__":
    TobaccoPlos = TobaccoPLOSData()
    TobaccoPlos.plos_job()
