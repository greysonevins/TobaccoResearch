import unittest
from JSONFix import JsonDOAJFix
import json
from ast import literal_eval
import pandas as pd
from pandas.util.testing import assert_frame_equal

class TestJsonFix(unittest.TestCase):

    def setUp(self):
        with open("testData/test_json.json") as file:
            self.json_test = json.load(file)["results"]

        dtypes = {
                'author_display': object, 'bibjson.abstract': object, 'bibjson.month': object,
               'bibjson.start_page': object, 'bibjson.title': object, 'bibjson.year': object, 'created_date': object,
               'id': object, 'issns': object, 'journal.country': object, 'journal.number': object, 'journal': object,
               'journal.title': object, 'journal.volume': object, 'language': object, 'last_updated': object,
               'license.title': object, 'license.type': object, 'license.url': object, 'link.type': object, 'link.url': object,
               'subject.code': object, 'subject.scheme': object, 'subject.term': object, 'DOI': object, 'EISSN': object,
               'PISSN': object
        }
        self.test_df = pd.read_csv("testData/test_json_df.csv", header=0, index_col=0, dtype=dtypes)
        self.test_df["DOI"].fillna("", inplace=True)
        self.test_df["PISSN"].fillna("", inplace=True)

        dataFix = ["author_display", "subject.code", "subject.scheme", "subject.term"]
        def tryFix(data):
            try:
                return literal_eval(data)
            except:
                return data
        for columns in dataFix:
            self.test_df[columns] = self.test_df[columns].apply(lambda data: tryFix(data))

        self.newJSON = JsonDOAJFix(self.json_test).finalizeJSON()

    def test_json_fix(self):

        assert_frame_equal(self.newJSON, self.test_df)


if __name__ == "__main__":
    unittest.main()
