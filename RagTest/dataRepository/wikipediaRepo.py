import requests
import json
class wikipedia_repo:
    def query_wiki_pages(self, page_ids):
        data = {}
        for page_id in page_ids:
            url = "https://en.wikipedia.org/w/api.php?format=json&action=query&pageids={}&prop=extracts&explaintext=true".format(str(page_id))
            r = requests.get(url)
            content = json.loads(r.text)
            for page in content.get("query").get("pages"):
                data[page] = content.get("query").get("pages").get(page).get("extract")
                print("Chunking and storing contents of page titled: ", content.get("query").get("pages").get(page).get("title"))
        return data
        
    def query_data(self, wiki_query_str):   
        '''This function provides information on the topic of the parameter passed, "wiki_query_str"
        '''
        try:
            url = "https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={}&utf8=&format=json".format(wiki_query_str)
            r = requests.get(url)
            content = json.loads(r.text)
            page_ids = []
            for page in content.get("query").get("search"):
                page_ids.append(page.get("pageid"))
                if len(page_ids) > 4:
                    break
            return self.query_wiki_pages(page_ids)
        except:
            print("Wikipedia data retrieval failed!")
            return {}