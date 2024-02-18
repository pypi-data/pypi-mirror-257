import subprocess

class Project:
    def __init__(self, name, description, creator, organization=None, category='Research', mode='Public'):
        self.name=name
        self.description = description
        self.creator = creator
        self.organization = organization
        self.category = category
        self.mode = mode
        

    def delete(self):
        proc = subprocess.run(['mrg', 'delete', 'project',self.project], check=True)        
        return proc.returncode



