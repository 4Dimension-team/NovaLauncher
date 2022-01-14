import os
import shutil
from pathlib import Path
import client.buildSettings as Settings


class TempDir:
    def __init__(self):
        self.path_to_dir = os.getenv("APPDATA") + "\\" + Settings.GAME_FILES_FOLDER + "\\.temp"
        if os.path.exists(self.path_to_dir):
            self.remove()
        os.makedirs(self.path_to_dir)

    def remove(self):
        if os.path.exists(self.path_to_dir):
            shutil.rmtree(self.path_to_dir, True)


def getPathToParentDir(path_to_dir):
    return Path(path_to_dir).parents[0]
