import time, re, json
import subprocess, socket
import validators, paramiko
from urllib.request import urlretrieve

# Basic experiment manipulation, such as pushing model to experiment,
# leasing and relinquishing resources and deleting experiments.
# TODO: Add ways to execute commands on nodes
class Experiment:
    def __init__(self, name, project, revision = 0):
        self.name = name
        self.project = project
        self.revision = revision
        self.realization = None

    # Add or update experiment model
    def set_model(self, filepath):
        # This assumes file is accessible locally from XDC
        # but we could expand it so that it can work with URLs too
        if validators.url(filepath):
            urlretrieve(filepath, "localfile")
            filepath="localfile"
        proc = subprocess.run(['mrg', 'push', filepath,
                               self.name + "." + self.project],
                              check=True, capture_output=True)
        out=proc.stdout.decode()
        items=out.split()
        self.revision = items[3]
        return self.revision

    # Lease resources for limited time
    # We can choose not to wait for this action to complete
    def lease(self, realization="real", duration="1w", wait = True):
        if self.revision == 0:
            return False

        # Really should cover minutes too, so I pre-emptively added it
        r = re.match(r'(\d+w)?(\d+d)?(\d+h)?(\d+m)?(\d+s)?', duration)
        if r.end() == 0:
            duration="1w"

        proc = subprocess.run(['mrg', 'realize', realization
                               + "." + self.name + "." + self.project,
                               "revision", self.revision,
                               "--duration", duration], check=True)
        
        if proc.returncode == 0:
            if not wait:
                return True
            retcode = 1
            while retcode != 0:
                proc = subprocess.run(['mrg', 'show', 'realization',
                                       realization + "." + self.name
                                       + "." + self.project])
                retcode = proc.returncode
                time.sleep(1)
            self.realization = realization
            return True
        else:
            return False

    # Modify the lease
    def modify(self, duration="1w"):
        if self.realization == None:
            print("No existing lease. Please use lease() function and not modify()")
            return False

        # Really should cover minutes too, so I pre-emptively added it
        r = re.match(r'(\d+w)?(\d+d)?(\d+h)?(\d+m)?(\d+s)?', duration)
        if r.end() == 0:
            duration="1w"

        proc = subprocess.run(['mrg', 'update', 'realization', 'expiration', realization
                               + "." + self.name + "." + self.project,
                               duration])
        
        if proc.returncode == 0:
            return True
        else:
            return False


    # Materialize the experiment - allocate leased resources to the experiment
    def allocate(self, wait = True):
        if self.realization is None:
            print("No realization")
            return False

        proc = subprocess.run(['mrg', 'materialize', self.realization
                               + "." + self.name + "." + self.project])

        if (proc.returncode == 0):
            while wait:
                proc = subprocess.run(['mrg', 'show', 'materialization',
                                       self.realization + "." + self.name
                                       + "." + self.project, "-j"],
                                      capture_output=True)

                try:
                    data=json.loads(proc.stdout.decode())
                    status=None
                    if "status" in data:
                        if "HighestStatus" in data["status"]:
                            if data["status"]["HighestStatus"] == "Success":
                                return True
                            elif data["status"]["HighestStatus"] == "Error":
                                return False
                except:
                    pass
                
                time.sleep(1)
        else:
            return False
    

    # Dematerialize the experiment, still keep the resources
    def deallocate(self):
        if self.realization is None:
            print("No realization")
            return False

        proc = subprocess.run(['mrg', 'dematerialize', self.realization + "." + self.name + "." + self.project], check=True)        
        return proc.returncode
    
    # Relinquish leased resources
    def relinquish(self):
        if self.realization is None:
            print("No realization")
            return False

        proc = subprocess.run(['mrg', 'relinquish', self.realization + "." + self.name + "." + self.project], check=True)        
        return proc.returncode

    # Terminate the experiment, delete everything
    def delete(self):
        proc = subprocess.run(['mrg', 'delete', 'experiment', self.name + "." + self.project], check=True)        
        return proc.returncode

    # Attach the experiment to xdc
    def attach(self, xdc=None):
        hostname = socket.gethostname().split('-')[0]

        # Check if it is already attached and detach if so
        status = subprocess.getoutput('mrg list xdc -j | jq -r --arg XDC ' + hostname + ' \'.XDCs[] | select(.name == $XDC).materialization\'')
        if status != 'null':
            proc = subprocess.run(['mrg', 'xdc', 'detach', hostname])
            if proc.returncode != 0:
                return False
            
        proc = subprocess.run(['mrg', 'xdc', 'attach', hostname, self.realization + "." + self.name + "." + self.project])
        return (proc.returncode == 0)
                

    # Execute command on node using SSH
    def exec_on_node(self, username, node, cmd):
        ssh_client = paramiko.SSHClient()
        private_key = paramiko.RSAKey.from_private_key_file("/home/testuser/.ssh/merge_key")
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(node, username=username, pkey=private_key)
        stdin, stdout, stderr = ssh_client.exec_command(cmd)
        ssh_client.close()
        return (stdin, stdout, stderr)
        
