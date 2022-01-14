import sys
import urllib.error
import urllib.request as req
import zipfile
import client.buildSettings as Settings
from client.modules import fileManager


class ClientUpdater:
    """
    Класс для загрузки клиента с сервера.

    :arg server адрес сервера
    :arg path путь до файла на сервере
    """

    def __init__(self, server, path):
        self.server_ip = server
        self.file_path = path

    def download_to_temp_dir(self):
        tempDir = fileManager.TempDir()
        try:
            url = req.urlopen(self.server_ip + '/' + self.file_path)

            try:
                download = open(tempDir.path_to_dir + '\\game.zip', 'wb')

                file_size_dl = 0
                block_size = 8192

                # Грузим архив из ссылки в файл
                while True:
                    buffer = url.read(block_size)
                    if not buffer:
                        break
                    file_size_dl += len(buffer)
                    download.write(buffer)

                download.close()

                # Распаковываем
                with zipfile.ZipFile(tempDir.path_to_dir + '\\game.zip', 'r') as archive:
                    archive.extractall(fileManager.getPathToParentDir(tempDir.path_to_dir))

            except IOError as IO_err:
                print(IO_err)

            finally:
                tempDir.remove()

        except urllib.error.HTTPError as http_err:
            print(http_err)


class UpdateListener:
    """
    Класс для прослушивания изменений на сервере
    """


class GameFilesChecker:
    """
    Класс для проверки файлов клиента на наличие изменений.
    Если изменения обнаружены - обновляемся с сервера.
    """

    def __init__(self):
        self.target = Settings.GAME_FILES_FOLDER
