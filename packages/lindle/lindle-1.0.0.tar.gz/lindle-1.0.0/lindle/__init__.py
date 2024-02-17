import requests

class Lindle:
    def __init__(self, api_key):
        self.api_key = api_key

    # GETTING LINKS AND FOLDERS

    def get_user(self):
        headers = {"Authorization": f"Bearer {self.api_key}"}
        res = requests.get("https://www.lindle.me/api/user", headers=headers).json()
        return {
            "id": res["_id"],
            "name": res["name"],
            "image": res["image"],
            "linkLimit": res["count"],
        }

    def get_links(self):
        headers = {"Authorization": f"Bearer {self.api_key}"}
        res = requests.get("https://www.lindle.me/api/links", headers=headers).json()
        links = []
        for item in res:
            links.append({
                "id": item["_id"],
                "name": item["name"],
                "url": item["url"],
                "folder": item.get("folder", ""),
                "favourite": item.get("favourite", False),
            })
        return links

    def get_folders(self, with_links=False):
        headers = {"Authorization": f"Bearer {self.api_key}"}
        res = requests.get("https://www.lindle.me/api/folders", headers=headers).json()
        folders = []
        links = self.get_links() if with_links else []
        for item in res:
            if item.get("public") is None:
                item["public"] = False
                
            if item.get("codename") is None:
                item["codename"] = ""
                
            folders.append({
                "id": item["_id"],
                "name": item["name"],
                "publicFolder": item["public"],
                "journeyLink": f"https://lindle.click/{item['codename']}",
                "links": [link for link in links if link["folder"] == item["_id"]],
            })
        return folders

    def get_synced_bookmarks(self):
        headers = {"Authorization": f"Bearer {self.api_key}"}
        res = requests.get("https://www.lindle.me/api/links/bookmarks/sync", headers=headers).json()
        folders = [{
            "id": item["id"],
            "name": item["name"],
            "date": item["date"],
            "folder": item["folder"],
        } for item in res["folders"]]
        links = [{
            "id": item["id"],
            "name": item["name"],
            "date": item["date"],
            "folder": item["folder"],
            "url": item["url"],
        } for item in res["links"]]
        return {"folders": folders, "links": links}

    # CREATING LINKS AND FOLDERS

    def create_link(self, name, url, folder=None, favourite=None):
        headers = {"Authorization": f"Bearer {self.api_key}"}
        data = {"name": name, "url": url, "folder": folder, "favourite": favourite}
        res = requests.post("https://www.lindle.me/api/links", json=data, headers=headers).json()
        item = res.get("link", {})
        link = {
            "id": item.get("_id", ""),
            "name": item.get("name", ""),
            "url": item.get("url", ""),
            "folder": item.get("folder", ""),
            "favourite": item.get("favourite", False),
        } if item else None
        return {"message": res.get("message", ""), "result": res.get("result", ""), "link":link}
    
    
    
    def create_folder(self, name, public_folder=None):
        headers = {"Authorization": f"Bearer {self.api_key}"}
        payload = {"name": name, "public": public_folder}
        response = requests.post("https://www.lindle.me/api/folders", json=payload, headers=headers)
        data = response.json()
        return data

    # UPDATING LINKS AND FOLDERS

    def update_link(self, link_id, name=None, url=None, folder=None, favourite=None):
        headers = {"Authorization": f"Bearer {self.api_key}"}
        payload = {"name": name, "url": url, "folder": folder, "favourite": favourite}
        response = requests.patch(
            f"https://www.lindle.me/api/links/{link_id}", json=payload, headers=headers
        )
        data = response.json()
        return data

    def update_folder(self, folder_id, name=None, public_folder=None):
        headers = {"Authorization": f"Bearer {self.api_key}"}
        payload = {"name": name, "public": public_folder}
        response = requests.patch(
            f"https://www.lindle.me/api/folders/{folder_id}", json=payload, headers=headers
        )
        data = response.json()
        return data

    # DELETE and REMOVAL

    def delete_link(self, link_id):
        headers = {"Authorization": f"Bearer {self.api_key}"}
        response = requests.delete(f"https://www.lindle.me/api/links/{link_id}", headers=headers)
        data = response.json()
        return data

    def delete_folder(self, folder_id):
        headers = {"Authorization": f"Bearer {self.api_key}"}
        response = requests.delete(
            f"https://www.lindle.me/api/folders/{folder_id}", headers=headers
        )
        data = response.json()
        return data