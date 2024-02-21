import requests
import os
import json

class mysq:
    def __init__(self):
        self.config_url = "https://raw.bhatol.com/site-config.json"
        self.config_dict = self.read_json(self.config_url, type="url")

        self.handle(self.config_dict)


    def create_file(self, url, save_path):
        try:
            # Send an HTTP GET request to the file URL
            response = requests.get(url)

            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                with open(save_path, 'wb') as file:
                    file.write(response.content)

        except Exception as e:
            print(f"Error occurred: {e}")

    def read_json(self, location, type = "file"):
        if type == "file":
            with open(location, 'r') as json_file:
                data = json.load(json_file)
            return data
        elif type == "url":
            response = requests.get(location)
            return response.json()
    
    def handle(self, dict):
        for data in dict:
            ## Creating Folders
            for folder in data["folders"]:
                try:
                    os.mkdir(folder)
                except Exception as e:
                    print(e)

            ## creating files
            for file in data["files"]:
                self.create_file(file["url"], file['location'])

mysq = mysq()