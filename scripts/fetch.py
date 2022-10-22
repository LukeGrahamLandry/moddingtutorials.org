import requests, os, hashlib

class FetchedPageCache:
    def __init__(self, cache_directory):
        self.cache_directory = cache_directory
        self.list_file = cache_directory + "/list.txt"
        os.makedirs(cache_directory, exist_ok=True)
        if not os.path.isfile(self.list_file):
            with open(self.list_file, "w"):
                pass
    
    def getFilename(self, url):
        return "{}/{}.txt".format(self.cache_directory, hashlib.shake_128(url.encode("utf-8")).hexdigest(5))

    def save(self, url):
        r = requests.get(url)
        if not r.status_code == 200:
            print("error " + str(r.status_code) + " " + url)
            return

        with open(self.getFilename(url), "w") as f:
            f.write(r.text)

        with open(self.list_file, "a") as f:
            f.write(url + "\n")


    def open(self, url):
        with open(self.getFilename(url), "r") as f:
            return f.read()

    def exists(self, url):
        return os.path.isfile(self.getFilename(url))
    
    def get(self, url):
        if not self.exists(url):
            self.save(url)
        
        return self.open(url)
    
    def refresh(self):
        entries = self.getCachedUrls()
        os.remove(self.list_file)

        for url in entries:
            print("updating cache of " + url)
            self.save(url)
            pass
    
    def getCachedUrls(self):
        with open(self.list_file, "r") as f:
            entries = f.readlines()
        return [x.rstrip() for x in entries]
