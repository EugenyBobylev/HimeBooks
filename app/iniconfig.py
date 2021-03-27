"""
 модуль работы с app_config.ini
"""
import configparser
from typing import List

from config import Config


def get_config() -> Config:
    _config = configparser.ConfigParser(allow_no_value=True)
    _config.optionxform = lambda option: option
    return _config


def get_config_fn() -> str:
    """
     return path to config file name
    """
    _fn = str(Config.BASE_DIR) + '/app/static/config/config.ini'
    return _fn


def create_config_ini(fn: str, paths: List[str] = None):
    ini = get_config()
    ini['PATHS'] = {}
    if paths is not None:
        for path in paths:
            ini['PATHS'][path] = None

    with open(fn, 'w') as f:
        ini.write(f)


def read_paths() -> List[str]:
    _config = get_config()
    _fn = get_config_fn()
    _config.read(_fn)
    _paths = [k for k in _config['PATHS']]
    return _paths


if __name__ == '__main__':
    fn = get_config_fn()
    create_config_ini(fn, ['/home/bobylev/Downloads/Books/',
                           '/home/bobylev/Downloads/Telegram Desktop/',
                           '/media/bobylev/Data/Downloads/Telegram Desktop/'])
#    paths = read_paths()
#    print(paths)
