import subprocess, re

class User:
    def __init__(self, username, password):
        self.username=username
        self.password=password

    def login(self):
        proc = subprocess.run(['mrg', 'login', self.username, '-p', self.password], check=True)
        return proc.returncode
        
