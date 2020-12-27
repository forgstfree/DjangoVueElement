import subprocess
import sys
from django.conf import settings

class ExecJar(object):
    def run(self,source_path,num,target_path):
        command = "java -jar /mnt/code/djcode/mysite/externalscript/DataMigrationAndAnalysis_v2.jar"
        cmd = [command, source_path, num, target_path]
        new_cmd = " ".join(cmd)
        return subprocess.run(new_cmd,shell=True)

if __name__ == "__main__":
    pass