import subprocess

class Project:
    def __init__(self, name, description, creator):
        self.name=name
        self.description = description
        self.creator = creator
        

    def delete(self):
        proc = subprocess.run(['mrg', 'delete', 'project',self.project], check=True)        
        return proc.returncode



