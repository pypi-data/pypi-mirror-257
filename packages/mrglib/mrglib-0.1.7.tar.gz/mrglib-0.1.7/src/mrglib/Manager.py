import re, json, subprocess, time
from mrglib import Experiment, Project

class Manager:
    def __init__(self):
        pass

    def find_project(self, name):
        proc = subprocess.run(['mrg', 'show', 'project', name, '-j'], capture_output=True)
        if proc.returncode == 0:
            data=json.loads(proc.stdout.decode())
            description=None
            creator=None
            if "description" in data["project"]:
                description=data["project"]["description"]
            for m in data["project"]["members"]:
                if "role" in data["project"]["members"][m]:
                    if data["project"]["members"][m]["role"] == "Creator":
                        creator=m
            p = Project.Project(name, description, creator)
            return p
        else:
            return None

    def find_experiment(self, name, project):
        proc = subprocess.run(['mrg', 'show', 'experiment', name + "." + project, '-j'], capture_output=True)
        if proc.returncode == 0:            
            data=json.loads(proc.stdout.decode())
            real = None
            revision = 0
            if "models" in data["experiment"]:
                for rev in data["experiment"]["models"]:
                    if "realization" in data["experiment"]["models"][rev]:
                        real=data["experiment"]["models"][rev]["realization"]
                        revision=rev
                        break
            ex = Experiment.Experiment(name, project, 0)
            ex.realization = real
            ex.revision = revision
            return ex
        else:
            return None

    def create_project(self, name, description, creator, organization=None, category='Research', mode='Public'):
        cmd = ['mrg', 'new', 'project', name, description]
        if organization != None:
            cmd.extend(['--organization', organization])
        if category != None:
            cmd.extend(['--category', category])
        if mode != None:
            cmd.extend(['--mode', mode])
        print("Cmd is ", cmd)
        proc = subprocess.run(cmd, check=True)
        if (proc.returncode == 0):
            proj=Project.Project(name, description, creator, organization, category, mode)
            return proj
        else:
            return None

    def create_experiment(self, name, project, description=None, wait=True):
        if (self.find_project(project) != None):
            proc = subprocess.run(['mrg', 'new', 'experiment', name + '.' + project, description], check=True)
            if not wait: 
                ex = Experiment.Experiment(name, project, 0)
                return ex
            else:
                ex = None
                while ex == None:
                    ex = self.find_experiment(name, project)
                    time.sleep(1)
                return ex

        else:
            print("No such project ", project)
            return None
        


    


    
