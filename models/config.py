import yaml
from pathlib import Path

class Config:
    config_dir = str(Path().absolute()) + '/' + "config"
    file_location = None
    def __init__(self):
        self.get_config_files()

    def load_config(self, idx):
        with open(self.filelist[idx]) as stream:
            self.file_location = self.filelist[idx]
            self.file = yaml.safe_load(stream)

    def get_config_files(self):
        self.filelist = []
        self.games_config = []
        for p in Path(self.config_dir).iterdir():
            if p.is_file():
                self.filelist.append(self.config_dir + '/' + p.name)
                self.games_config.append(p.stem)
