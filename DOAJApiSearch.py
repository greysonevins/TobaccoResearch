import requests
import time
import pandas as pd
from JSONFix import JsonDOAJFix
from ast import literal_eval
from tqdm import tqdm



class DOAJDateVerify:
    def __init__(self):
        try:
            self.plosData = pd.read_csv("data/plosTobacoo.csv", header=0, index_col=0, converters={"author_display": literal_eval})
            self.dois = set(self.plosData.id.values)
            self.headers = {"User-Agent" : "student-research-2018"}
            self.doajAPI = "https://doaj.org/api/v1/search/articles/doi:{}"

            self.verifiedArticles = []
            self.apicounter = 0
            self.unvalidated = []
        except:
            print("Missing Plos Tobacco Data")

    def get_doaj_journal(self):
        print("starting search on DOAJ")
        print("this may take some time...")
        try:
            for doi in tqdm(self.dois):

                urlNotBroken = True
                while urlNotBroken:
                    req = requests.get(self.doajAPI.format(doi), headers=self.headers)
                    response = req.json()
                    self.apicounter += 1
                    if req.status_code != 200:
                        counterAttempts+=1
                        time.sleep(5*counterAttempts)
                        print("API Issues with status: {}".format(status_code))
                        print("sleeping 4 seconds...")
                    if req.status_code != 200 and counterAttempts == 4:
                        raise TimeoutError

                    elif len(response["results"]) == 0:
                        self.unvalidated.append(doi)
                        urlNotBroken = False
                        break
                    else:
                        self.verifiedArticles.append(response["results"][0])
                        urlNotBroken = False
                        break
                #### Sorry for the error. Your computer must be faster than mine :)
                ## This should fix it
                time.sleep(1)
        except TimeoutError:
            print("API response error")




    def doaj_verify(self):
        self.get_doaj_journal()
        if len(self.unvalidated): print("API Done with {} Unvalidated DOIs that will not be used".format(len(self.unvalidated)))
        else: print("API Done")
        print("Fixing JSON/Flattening From DOAJ")
        newJSON = JsonDOAJFix(self.verifiedArticles).finalizeJSON()

        print("Merging DOAJ and PLOS Data")
        columnsUsed = newJSON.columns.difference(self.plosData.columns)
        finalDoajPlosDf = pd.merge(self.plosData, newJSON[columnsUsed], left_on="id", right_on="DOI")


        finalDoajPlosDf.to_csv("data/verifiedDOAJPlos.csv")
        print("New CSV Created")
        print("Finished DOAJ Verify")


if __name__ == "__main__":
    DOAJVerify = DOAJDateVerify()
    DOAJVerify.doaj_verify()
