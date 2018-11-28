from pandas.io.json import json_normalize


class JsonDOAJFix:
    def __init__(self, jsonList):
        self.jsonList = jsonList
        self.newJSON = {}
        self.updatedJSON = []

    def iterJSON(self):
        for json in self.jsonList:
            for key, values in json.items():
                if type(values) is not str:
                    self._iterJSON(key, values)
                else:
                    self.newJSON[key] = values

            self.updatedJSON.append(self.newJSON)
            self.newJSON = {}


    def _iterJSON(self, key, values):
        if type(values) is not str and values is not None:

            if type(values) is dict:

                for new_keys, new_vals in values.items():
                    if type(new_vals) is not str:
                        self._iterJSON(new_keys, new_vals)
                    else:
                        keyDict = "{}.{}".format(key, new_keys)
                        if self.newJSON.get(keyDict):
                            if type(self.newJSON[keyDict]) == str:
                                newList = [self.newJSON[keyDict], new_vals]
                                self.newJSON[keyDict] = newList
                            else:
                                self.newJSON[keyDict].append(new_vals)

                        else:
                            self.newJSON[keyDict] = new_vals
            if type(values) is list:
                for new_vals in values:

                    self._iterJSON(key, new_vals)
        else:

            if self.newJSON.get(key):

                if type(self.newJSON[key]) is str:
                    newList = [self.newJSON[key], values]
                    self.newJSON[key] = newList
                else:

                    self.newJSON[key] = self.newJSON[key].append(values)
            else:
                self.newJSON[key] = values

    def finalizeJSON(self):
        self.iterJSON()
        jsonFIX = json_normalize(self.updatedJSON)

        doi, eissn, pissn = [], [], []

        for ite, vals in jsonFIX.iterrows():
            if "doi" in vals["identifier.type"]:
                indDOI = vals["identifier.type"].index("doi")
                doi.append(vals["identifier.id"][indDOI])
            else:
                doi.append("")

            if "eissn" in vals["identifier.type"]:
                indEISSN = vals["identifier.type"].index("eissn")
                eissn.append(vals["identifier.id"][indEISSN])
            else:
                eissn.append("")

            if "pissn" in vals["identifier.type"]:
                indPISSN = vals["identifier.type"].index("pissn")
                pissn.append(vals["identifier.id"][indPISSN])
            else:
                pissn.append("")

        jsonFIX.drop(["identifier.type", "identifier.id"], axis=1, inplace=True)

        jsonFIX["DOI"], jsonFIX["EISSN"], jsonFIX["PISSN"] = doi, eissn, pissn

        jsonFIX.rename(columns={"author.name": "author_display", "title": "title_display", "journal.publisher": "journal"}, inplace=True)

        return jsonFIX
