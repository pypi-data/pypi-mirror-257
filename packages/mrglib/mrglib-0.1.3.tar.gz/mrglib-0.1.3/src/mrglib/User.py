import subprocess, re

class User:
    def __init__(self):
        pass

    def login(self):
        proc = subprocess.run(['mrg', 'login', self.username, '-p', self.password], check=True)
        self.username=username
        self.password=password
        return proc.returncode
        
