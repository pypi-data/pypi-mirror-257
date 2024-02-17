from pathlib import Path
from datetime import datetime
import os

class Layout:

    def __init__(self, conf, paths):
        self.conf=conf
        self.paths=paths
        self.today=datetime.today()
        self.today_backup=self.today

    def settoday(self,timestamp):
        self.today=datetime.fromtimestamp(timestamp)

    def restoretoday(self):
        self.today=self.today_backup

    def gettoday(self):
        return self.today

    def flatten(self):
        paths=list(Path(self.paths["files"]).rglob("*"))
        result=list()
        for p in paths:
            if os.path.isfile(p):
                result.append(p.relative_to(self.paths["files"]))
        return result

    def create(self):
        file=self.todaypath()
        if not os.path.exists(file):
            open(file, 'a').close()
        return self.todaysubpath()
        
    def todayname(self):
        return self.today.strftime(self.conf["filename"])

    def todaysubdir(self):
        """
        Must be overriden by child classes
        """
        subdir=self.today.strftime(self.conf["layout"])
        if not os.path.exists(subdir):
            Path(os.path.join(self.paths["files"],subdir)).mkdir(parents=True, exist_ok=True)
        return subdir

    def todaysubpath(self):
        subdir=self.todaysubdir()
        return os.path.join(self.todaysubdir(), self.todayname())
    
    def todaypath(self):
        return os.path.join(self.paths["files"],self.todaysubpath())
