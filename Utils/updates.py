
import shutil


from . import (
    GITHUB_TAGS_URL, GITHUB_RELEASES_URL, Release, CheckUpdatesResponses, InstallUpdateResponses, exceptions,
    CheckUpdatesResponse
)
from configs import CONFIGS_DIR, STORAGE_DIR, PLUGINS_DIR, CACHE_DIR, UPDATE_DIR, BACKUP_DIR


import requests
from zipfile import ZipFile


from pathlib import Path
from time import sleep
import json


__all__ = [
    'get_new_releases',
    'download_zip',
    'extract_update_archive',
    'create_backup',
    'extract_backup_archive',
    'install_release',
    'install_backup'
]


HEADERS = {
    "accept": "application/vnd.github+json"
}


def get_tags(current_tag: str) -> list[str]:
    '''
    Получает все теги с GitHub репозитория.

    :param current_tag: текущий тег.
    :type current_tag: str
    :raises GitHubRequestError: Ошибка, возникающая при ошибке запроса к GitHub'у.
    :return: Список тегов.
    :rtype: list[str]
    '''
    page = 1
    json_response: list[dict] = []

    while not any([el.get("name") == current_tag for el in json_response]):
        if page != 1: sleep(1)


        response = requests.get(f"{GITHUB_TAGS_URL}?page={page}", headers=HEADERS)

        if not response.status_code == 200 or not response.json(): raise exceptions.GitHubRequestError(response)

        else:
            json_response.extend(response.json())
            page += 1


    tags = [i.get("name") for i in json_response]

    return tags


def get_next_tag(tags: list[str], current_tag: str) -> str | None:
    '''
    Ищет след. тег после переданного. Если не находит текущий тег, возвращает первый. Если текущий тег - последний, возвращает None.

    :param tags: Список тегов.
    :type tags: list[str]
    :param current_tag: Текущий тег.
    :type current_tag: str
    :return: След. тег / первый тег / None.
    :rtype: str | None
    '''
    try: curr_index = tags.index(current_tag)

    except ValueError: return tags[len(tags) - 1]


    if not curr_index: return None

    return tags[curr_index - 1]


def get_releases(from_tag: str) -> list[Release]:
    '''
    Получает данные о доступных релизах, начиная с тега.

    _extended_summary_

    :param from_tag: Тег релиза, с которого начинать поиск.
    :type from_tag: str
    :raises GitHubRequestError: Ошибка, возникающая при ошибке запроса к GitHub'у.
    :return: Список релизов.
    :rtype: list[Release]
    '''
    page = 1
    json_response: list[dict] = []
    while not any([el.get("tag_name") == from_tag for el in json_response]):
        if page != 1: sleep(1)


        response = requests.get(f"{GITHUB_RELEASES_URL}?page={page}", headers=HEADERS)

        if not response.status_code == 200 or not response.json(): raise exceptions.GitHubRequestError(response.status_code)

        else:
            json_response.extend(response.json())
            page += 1


    result = []
    to_append = False

    for el in json_response[::-1]:
        if (name := el.get("tag_name")) == from_tag: to_append = True

        if to_append:
            description = el.get("body")

            sources = el.get("zipball_url")

            if "#unskippable" in description: to_append = False


            release = Release(name, description, sources)

            result.append(release)


            if not to_append: break


    return result


def get_new_releases(current_tag: str) -> CheckUpdatesResponse:
    '''
    Проверяет на наличие обновлений.

    :param current_tag: Тег текущей версии.
    :type current_tag: str
    :return: Ответ.
    :rtype: CheckUpdatesResponse
    '''
    try: tags = get_tags(current_tag)


    except Exception as err:
        return CheckUpdatesResponse(
            CheckUpdatesResponses.TAGS_NOT_FOUND,
            err
        )


    next_tag = get_next_tag(tags, current_tag)


    if not next_tag: return CheckUpdatesResponse(
        CheckUpdatesResponses.CARDINAL_IS_UP_TO_DATE
    )


    try:
        releases = get_releases(next_tag)

        if not releases: raise Exception('Не удалось получить информацию о новой версии')


    except Exception as err:
        return CheckUpdatesResponse(
            CheckUpdatesResponses.RELEASES_NOT_FOUND,
            err
        )


    return CheckUpdatesResponse(
        CheckUpdatesResponses.UPDATE_AVAILABLE,
        releases=releases
    )


def download_zip(url: str) -> None:
    '''
    Загружает zip архив с обновлением в кеш.

    :param url: ссылка на zip архив.
    :type url: str
    '''
    with requests.get(url, stream=True) as r:
        r.raise_for_status()

        with open(CACHE_DIR / 'update.zip', 'wb') as fp:
            for chunk in r.iter_content(chunk_size=8192): fp.write(chunk)


    return


def extract_update_archive() -> str:
    '''
    Разархивирует скачанный update.zip.

    :return: Название папки с обновлением (storage/cache/update/<папка с обновлением>).
    :rtype: str
    '''
    if UPDATE_DIR.exists(): shutil.rmtree(UPDATE_DIR, ignore_errors=True)


    with ZipFile(CACHE_DIR / 'update.zip', "r") as zip:
        folder_name = zip.filelist[0].filename

        zip.extractall(UPDATE_DIR)


    return folder_name


def zipdir(path: Path, zip_obj: ZipFile) -> None:
    '''
    Рекурсивно архивирует папку.

    :param path: Путь до папки.
    :type path: Path
    :param zip_obj: Объект zip архива.
    :type zip_obj: ZipFile
    '''
    for root, dirs, files in path.walk():
        if root.name == "__pycache__": continue

        for file in files: zip_obj.write(root.joinpath(file), root.joinpath(file).relative_to(path.parent))


    return


def create_backup() -> None:
    '''
    Создает резервную копию с папками storage, configs и plugins.
    '''
    with ZipFile("backup.zip", "w") as zip:
        zipdir(STORAGE_DIR, zip)
        zipdir(CONFIGS_DIR, zip)
        zipdir(PLUGINS_DIR, zip)


    return


def extract_backup_archive() -> None:
    '''
    Разархивирует скачанный backup.zip в папку бекапа.
    '''
    if BACKUP_DIR.exists(): shutil.rmtree(BACKUP_DIR, ignore_errors=True)

    BACKUP_DIR.mkdir(parents=True, exist_ok=True)


    with ZipFile(CACHE_DIR / 'backup.zip', "r") as zip: zip.extractall(BACKUP_DIR)


    return


def install_release(folder_name: str) -> InstallUpdateResponses:
    '''
    Устанавливает обновление.

    :param folder_name: Название папки со скачанным обновлением в папке обновлений.
    :type folder_name: str
    :return: Статус обновления.
    :rtype: InstallUpdateResponses
    '''
    reboot_flag = False

    try:
        release_folder = UPDATE_DIR.joinpath(folder_name)

        if not release_folder.exists(): return InstallUpdateResponses.UPDATE_FOLDER_NOT_FOUND


        update_info_path = release_folder.joinpath('update.json')

        reboot_flag = False

        if update_info_path.exists():
            with open(update_info_path, "r", encoding="utf-8") as fp: data = json.loads(fp.read())

            reboot_flag = data.get('reboot_required', False)


        for _ in release_folder.iterdir():
            file = _.name

            if file == 'update.json': continue


            if _.is_file(): shutil.copy2(_, file)

            else: shutil.copytree(_, file, dirs_exist_ok=True)


        if reboot_flag: return InstallUpdateResponses.REBOOT_IS_REQUIRED

        return InstallUpdateResponses.INSTALL_SUCCESS

    except: return InstallUpdateResponses.UNEXCEPTED_ERROR


def install_backup() -> None:
    '''
    Устанавливает бекап.

    :raises BackupNotFoundError: Если отсутствует распакованный бекап.
    '''
    if not BACKUP_DIR.exists(): raise exceptions.BackupNotFoundError()


    for _ in BACKUP_DIR.iterdir():
        file = _.name

        if _.is_file(): shutil.copy2(_, file)

        else: shutil.copytree(_, file, dirs_exist_ok=True)


    return