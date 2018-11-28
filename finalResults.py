import pandas as pd
from ast import literal_eval
import numpy as np

class FinalizeResults:

    def __init__(self):
        self.verifiedDOAJPlos = pd.read_csv("data/verifiedDOAJPlos.csv", header=0, index_col=0, converters={"author_display": literal_eval})
        self.authorsDF = pd.DataFrame()

    def authorResults(self):
        print("Creating an Author DataFrame")
        authorsList = []
        for key, df in self.verifiedDOAJPlos.iterrows():
            for author in df["author_display"]:
                newAuthor = df.copy()
                newAuthor["Author"] = author
                authorsList.append(newAuthor)

        self.authorsDF = pd.DataFrame(authorsList)

    def getGroup(self, group, df):
        print("Creating DataFrame for {} with new Metrics".format(group))
        timeGlobal = list(set(map(int, df.publication_date.str[:4].values)))
        return df.groupby(group).apply(lambda groupData: self.influenceData(groupData, timeGlobal)).sort_values(["Num Articles", "Pub/Year"], ascending=False)




    def influenceData(self, groupData, timeGlobal):
        count = len(groupData)
        groupYearsStr = groupData.publication_date.str[:4].values
        groupYears = list(map(int, groupYearsStr))
        groupYears.sort()

        indexStart = timeGlobal.index(groupYears[0])
        globalYears = timeGlobal[indexStart:]
        finalYears = [groupYears.count(years) for years in globalYears]

        meanPublication = np.mean(finalYears)

        return pd.Series({"Num Articles": count, "Pub/Year": meanPublication})

    def getResults(self):
        print("Starting Influence Data Builder")
        self.authorResults()
        authorSheet = self.getGroup("Author", self.authorsDF)
        journalSheet = self.getGroup("journal.title", self.verifiedDOAJPlos)
        print("Creating Excel from new dataframe with metrics")
        writer = pd.ExcelWriter("data/finalResults.xlsx")
        authorSheet.to_excel(writer, "Most Inluential Authors")
        journalSheet.to_excel(writer, "Most Inluential Journals")
        writer.save()
        print("finished save!")




if __name__ == "__main__":
    FinalResults = FinalizeResults()
    FinalResults.getResults()
