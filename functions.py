import os
import requests
import time


def validate_path(path):
    path_ = path
    path_ = path_.lstrip().rstrip()
    if os.path.isdir(path_):
        return True
    return False


def validate_url(url):
    try:
        url_ = url
        url_ = url_.lstrip().rstrip()
        requests.get(url_)
        return True
    except requests.exceptions.ConnectionError:
        return False

    except requests.exceptions.MissingSchema:
        return False


def validate_url_taiwebs(url):
    url_ = url
    url_ = url_.lstrip().rstrip()

    if "taiwebs.com/" in url_ and "/download" in url_:
        return True
    return False


def wait_download_file(path):

    def latest_download_file():

        os.chdir(path)
        files = sorted(os.listdir(os.getcwd()), key=os.path.getmtime)
        newest = files[-1]
        return newest

    fileends = "crdownload"
    while "crdownload" == fileends:
        time.sleep(1)
        newest_file = latest_download_file()
        if "crdownload" in newest_file:
            fileends = "crdownload"
        else:
            fileends = "none"
            time.sleep(1)
