import os, json, socket, re, subprocess, shutil
from datetime import datetime
from jsonschema import validate
from pathlib import Path
from pnote.layout import *
from pnote.metadata import *

class ProjectConfig:
    FILE="config.json"
    DEFAULT_CONFIG = {
        "layout": "%Y/%m",
        "filename": "%Y-%m-%d.md",
        "editor": ["vim"],
        "template": ""
    }
    SCHEMA_CONFIG = {
        "type": "object",
        "properties": {
            "layout": {"type": "string"},
            "filename": {"type": "string"},
            "editor": {"type": "array"},
            "template": {"type": "string"}
        },
        "required":[
            "layout",
            "filename",
            "editor",
            "template"
        ]
    }
    
    def __init__(self, root):
        self.pfile=os.path.join(root,self.FILE)
        if "EDITOR" in os.environ:
            self.DEFAULT_CONFIG["editor"]=[os.environ["EDITOR"]]
        self.config=self.DEFAULT_CONFIG
        self.load()

    def load(self):
        if os.path.exists(self.pfile):
            with open(self.pfile) as f:
                self.config=json.load(f)
                try:
                    validate(instance=self.config, schema=self.SCHEMA_CONFIG)
                except:
                    print("Invalid configuration file")
                    exit(1)
        else:
            self.save()
                    
    def save(self):
        with open(self.pfile, "w") as f:
            f.write(json.dumps(self.config,indent=4, sort_keys=True))

    def __getitem__(self, key):
        return self.config[key]

    def __setitem__(self, key, value):
        self.config[key]=value

        
class Project:

    def __init__(self, path):
        self.paths={
            "root": path,
            "files": os.path.join(path,"files"),
            "lockfile": os.path.join(path,"lockfile"),
        }

        if not os.path.exists(self.paths["root"]):
            print("Creating project...")
        Path(self.paths["root"]).mkdir(parents=True, exist_ok=True)
        Path(self.paths["files"]).mkdir(parents=True, exist_ok=True)

        self.conf=ProjectConfig(self.paths["root"])
        self.metadata=Metadata(self.paths)
        self.layout=Layout(self.conf,self.paths)
        
        if os.path.exists(self.paths["lockfile"]):
            print("Your project contains a lock file! Your project might be corrupted :(")
            exit(1)

    def lock(self):
        open(self.paths["lockfile"], 'a').close()

    def unlock(self):
        os.remove(self.paths["lockfile"])

    def create(self,subpath=None):
        self.lock()
        if subpath is None:
            subpath=self.layout.create()
        try:
            self.metadata.create(subpath, self.layout.gettoday())
        except sqlite3.IntegrityError:
            print("The file you are trying to edit was deleted!")
            answer=input("Do you want to use its old metadata [Y/n]? ")
            if answer.lower() not in ["yes", "y", ""]:
                self.metadata.delete(self.layout.todaysubpath())
                self.metadata.create(subpath)
        self.unlock()

    def find(self, string):
        files=list()
        for file in self.layout.flatten():
            if string is None:
                files.append(str(file))
            elif string in file.name:
                files.append(str(file))
        return files

    def getfileinfo(self,subpath, name):
        return self.metadata.getfileinfo(subpath,name)

    def grep(self,exp):
        r=re.compile(exp)
        results=list()
        for subpath in self.layout.flatten():
            path=os.path.join(self.paths["files"],subpath)
            lines=list()
            with open(path, "r") as f:
                ln=1
                for line in f:
                    if r.search(line):
                        lines.append((ln,line.rstrip()))
                    ln+=1
            if len(lines) > 0:
                results.append((str(subpath),lines))
        return results

    def searchtag(self,tag):
        return self.metadata.searchtag(tag)

    def addtags(self, subpaths, tags):
        for subpath in subpaths:
            for tag in tags:
                self.metadata.addtag(subpath, tag)

    def addtagslastedited(self, tags):
        subpath=self.metadata.getcache("last_edited")
        if subpath is not None:
            for tag in tags:
                self.metadata.addtag(subpath, tag)
        else:
            print("You did not edit any files yet!")
            exit(1)

    def addfile(self,filepath,timestamp=None):
        if timestamp is not None:
            self.layout.settoday(timestamp)
        path=self.layout.todaypath()
        ignore=False
        if not os.path.exists(path):
            self.create()
        else:
            print("The following subpath is already taken: "+self.layout.todaysubpath())
            answer=""
            while answer.lower() not in ["ignore","replace","append", "i", "r", "a"]:
                answer=input("What do you want to do [Ignore/Replace/Append]? ")
            if answer.lower() in ["ignore", "i"]:
                ignore=True
            elif answer.lower() in ["append", "a"]:
                ignore=True
                with open(filepath, "r") as src:
                    with open(path, "a") as dst:
                        for line in src:
                            dst.write(line)
        if timestamp is not None:
            self.layout.restoretoday()
        if not ignore:
            shutil.copyfile(filepath, path)
                
    def addtagstoday(self,tags):
        path=self.layout.todaypath()
        subpath=self.layout.todaysubpath()
        if not os.path.exists(path):
            print("Today's file not created yet!")
            exit(1)
        else:
            for tag in tags:
                self.metadata.addtag(subpath, tag)

    def listtags(self,subpath=None):
        return self.metadata.listtags(subpath)

    def deletetags(self, subpaths, tags):
        for subpath in subpaths:
            for tag in tags:
                self.metadata.deletetag(subpath, tag)

    def obliteratetags(self, tags):
        for tag in tags:
            self.metadata.obliteratetag(tag)

    def getpath(self,subpath):
        return os.path.join(self.paths["files"],subpath)

    def fix(self, dry):
        self.metadata.fix_deleted(dry)
        self.metadata.fix_new(self.layout,dry)

    def apply_template(self):
        template_path=os.path.join(self.paths["root"],self.conf["template"])
        if os.path.isfile(template_path):
            result = subprocess.run([template_path, self.layout.todaysubpath()], stdout=subprocess.PIPE)
            with open(self.layout.todaypath(), "w") as f:
                f.write(result.stdout.decode('utf-8'))

    def open(self,string):
        if string is None:
            path=self.layout.todaypath()
            if not os.path.exists(path):
                self.create()
                self.apply_template()
            self.exec_editor(self.layout.todaysubpath())
        else:
            files=list()
            for path in self.layout.flatten():
                if string in path.name:
                    files.append(path)
            if len(files) == 0:
                path=self.getpath(string)
                if not os.path.exists(path):
                    self.create(string)
                    self.apply_template()
                self.exec_editor(string)
            elif len(files) == 1:
                self.exec_editor(files[0])
            else:
                print("Multiple file match:")
                for path in files:
                    print(path.name)

    def exec_editor(self, subpath):
        self.metadata.setcache("last_edited",subpath)
        path=self.getpath(subpath)
        command=self.conf["editor"]+[path]
        try:
            os.execvp(command[0],command)
        except:
            print("Cannot open editor \"{}\"".format(self.conf["editor"]))
            exit(1)

    def navigate(self, from_subpath=None, desc=True):
        for subpath in self.metadata.flatten_ordered(desc):
            path=os.path.join(self.paths["files"],subpath)
            with open(path, "r") as f:
                for line in f:
                    print(line,end="")
