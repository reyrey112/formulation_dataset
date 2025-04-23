import subprocess
from pathlib import Path
from os.path import isfile, join
from os import listdir


class script_preparation:
    def __init__(self):
        self.set_R_HOME()
        self.set_R_script()

    def back_to_forward_slash_switch(self, path):
        split = path.split("\\")
        new_path = "/".join(split)

        return new_path

    def set_R_HOME(self):
        script = subprocess.run("set R_HOME", shell=True, capture_output=True, text=True)
        self.R_HOME = script.stdout[7:-1]

    def set_R_script(self):
        R_script = self.R_HOME + "\\Rscript"
        self.R_script = self.back_to_forward_slash_switch(R_script)

    def get_R_script(self):
        return self.R_script

    def set_parent(self, file):
        self.parent = str(Path(file).parent)

    def get_parent(self):
        return self.parent

    def get_files_list(self, path):
        analysis_files = [i for i in listdir(path) if isfile(join(path, i))]

        return analysis_files

    def __get_r_files(self):
        files = self.get_analysis_files()
        r_files = [i for i in files if i[-2:] == ".r"]

        return r_files

    def run_script(self):
        pass
