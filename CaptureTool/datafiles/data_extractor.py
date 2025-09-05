import json
from config.config import GAME_DATA_URLS
from models.wish import WishSchema

class DataExtractor:
    
    def __init__(self):
        self.result = []
    
    def build_files(self):
        self.extract_from_url(GAME_DATA_URLS)
        with open("combined_data.json", "w", encoding="utf-8") as f:
            json.dump(self.result, f, ensure_ascii=False, indent=2)
    
    def extract_from_url(self, url_list: list[str]):
        """Fetches JSON from a list of URLs and appends transformed objects to result"""
        import requests
        
        for url in url_list:
            response = requests.get(url)
            
            if response.status_code == 200:
                data = response.json()
                
                # data can be a dict of items; iterate over values if needed
                if isinstance(data, dict):
                    res = WishSchema.from_json(data)
                    self.result.extend(res)
                elif isinstance(data, list):
                    for item in data:
                        res = WishSchema.from_json(item)
                        self.result.extend(res)
                else:
                    # single JSON object
                    res = WishSchema.from_json(data)
                    self.result.append(res)
            else:
                print(f"Error fetching {url}: {response.status_code}")
