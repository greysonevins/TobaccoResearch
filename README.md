# Research into Tobacco Research

## Conigure Requirements

Please use python3 and load the requirements to start project. All requirements should be saved to this environment but please use `python3 install -r requirements.txt` if issues arise.


## The file
To run project. run `main.py`

1. `PLOSApiSearch.py` The API for plos will gather every page of articles, searching for articles that have Tobacco in the Title, Abstract, or Introduction — ~ 3000. The final file should be `data/plosTobacoo.csv`
2. `DOAJApiSearch.py` Then the program searches DOAJ for the corresponding DOIs and links these articles. The final file should be `data/verifiedDOAJPlos.csv`
    1. At first, I thought the massive amount of API calls could be resolved by searching by ISSN and year, however, some ISSNs have hundreds of thousands of articles, so I decided to stick with DOIs.
    2. Because the DOAJ verify file is requesting 3000 articles, it will take a bit of time (between 20-30 minutes currently at an api call rate of ~1.8 seconds). I attempted to cut this down also by threading the process but this caused a timeout error from DOAJ. You could potential thread this on different servers.
    3. While other articles have Department data, PLOS articles do not for some odd reason. This was verified through my JSON fix process.
    4. `JSONFix.py` The JSON Fix changes the nested JSON and Nested JSON Arrays to a more practical DataFrame to use.
3. `finalResults.py` Finally, the linked Plos to Doaj data is made useful by finding the number of articles per author and journal and the rate at which  these assets are producing them. Essentially, I calculated the rate of production by taking the first article publication date and see how many articles were produced per year since that date and getting the mean of these values.
Then I produce an xlsx that has two tabs for authors and journals which should be `data/finalResults.xlsx`.


## Testing

I struggled to find a method that helped test python's `requests` module. I saw some examples of mocking the response, however, I worried that trying to figure this out would go beyond the 4 hour mark. This is something I would enjoy learning to test.

I did test my JSONFix module. You can test this function by running `python test_JSONFIX.py`
