import subprocess
def subprocess_cmd(command):
                process = subprocess.Popen(command,stdout=subprocess.PIPE, shell=True)
                x=process.communicate()[0].strip()
                return x

