import requests, zipfile, tarfile, os, json

class NgrokTunnel:
    def __init__(self, token: str, operative_system: str):
        """
        operative_system values: 'windows', 'linux'
        token: create account on Ngrok and copy paste generated free token
        """
        self.token = token
        self.operative_system = operative_system
        
    def download_and_unzip(self, url_for_download: str):
        content = requests.get(url_for_download).content
        self.filename = url_for_download.split('/')[-1]
        self.filename_without_extension = self.filename.split('.')[0]
        with open(self.filename, "wb") as o:
            o.write(content)
            
        self.path_to_compressed = os.path.join(os.getcwd(), self.filename)

        if self.operative_system == "windows":
            with zipfile.ZipFile(self.path_to_compressed, 'r') as zip_file:
               zip_file.extractall()
        elif self.operative_system == "linux":
            tar_file = tarfile.open(self.filename)
            tar_file.extractall()
            tar_file.close()
        
        print("Download complete and extraction complete!")
        
    
    def run_ngrok(self, port: int):
        if self.operative_system == "windows":
            get_ipython().system_raw(f"{os.path.join(os.getcwd(), 'ngrok.exe')} config add-authtoken {self.token}")
            get_ipython().system_raw(f"{os.path.join(os.getcwd(), 'ngrok.exe')} http {port} &")
        elif self.operative_system == "linux":
            get_ipython().system_raw(f"./ngrok config add-authtoken {self.token}")
            get_ipython().system_raw(f"./ngrok http {port} &")

    
    def get_public_url(self):
        print("Public url:", end=" ")
        print(eval(requests.get("http://localhost:4040/api/tunnels").text.replace("true", "True").replace("false", "False").replace("null", "None"))["tunnels"][0]["public_url"])