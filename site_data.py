from __future__ import annotations

import os
import types
import string
from typing import Union
from jinja2 import Environment, FileSystemLoader
from werkzeug.wrappers.response import HTTPStatus
from flask import abort, Flask


EXTENDS = ['.css', '.js']
TYPES = Union[str, dict, list, int]


class Site:
    @property
    def link(self):
        return '.html'

    @property
    def page_source(self):
        return '.' + os.path.join(self.static_folder, self.__pages_dir_root)

    @property
    def static_folder(self):
        return self.__flask.static_url_path

    @property
    def template_folder(self):
        return self.__flask.template_folder

    @template_folder.setter
    def template_folder(self, value: str | os.PathLike[str] | None):
        self.__flask.template_folder = value

    @property
    def pages(self):
        return os.listdir(self.page_source)

    @property
    def env(self):
        return self.__env

    @property
    def get_flask(self) -> Flask:
        return self.__flask

    @property
    def error_folder(self):
        return '.' + os.path.join(self.static_folder, self.__error_dir_root)

    def __init__(
            self,
            flask: Flask,
            pages_dir_root: str | os.PathLike[str] = "Pages",
            error_dir_root: str | os.PathLike[str] = "Error"
    ):
        self.__flask = flask
        self.__pages_dir_root: str = pages_dir_root
        self.__error_dir_root: str = error_dir_root
        self.__env = Environment(loader=FileSystemLoader(flask.template_folder))

        if not os.path.isdir(self.page_source):
            os.mkdir(self.page_source)


class Functions(Site):
    def __init__(self, flask: Flask, pages_dir_root: str | os.PathLike[str] = "Pages"):
        super().__init__(flask, pages_dir_root)
        self.__func_extents: dict[str: types.FunctionType] = {
            '.txt': self.text_extend
        }

    @staticmethod
    def text_extend(file_path: str) -> list[str]:
        with open(file_path[3:], 'r', encoding='utf-8') as text:
            txt = (text.read()).split('\n')
            out: list = [
                txt[i] for i in range(len(txt))
            ]

        return out

    def create_template(self, folder_name: str) -> str:
        """
        Create a page layout by given folder name.
        Must have a same '.html' file at template folder otherwise connection would be aborted.
        :param folder_name: str -> name of folder for create a page template. Must hava a same <string:filename>.html.
        :return: str -> rendered template.
        """
        if folder_name not in os.listdir(self.page_source):
            abort(HTTPStatus.NOT_FOUND)

        data = self.data_compose(self.page_source + '\\' + folder_name)
        template = self.env.get_template(data['html'])

        return template.render(data=data)

    def data_compose(self, path: str) -> dict[str, TYPES]:
        """
        Compose data of directory to dict keys -> title, dirs, content + extends(['.css', '.js']).
        :param path: str -> path to dir.
        :return: dict -> data, stored by keys (title, dirs, content + extends(['.css', '.js'])).
        """
        ls = os.listdir(path)

        title = os.path.split(path)[-1]

        data: dict[str: TYPES] = {
            "title": title,
            "dirs": {},
            "content": [],
            "html": title + self.link
        }

        for i in range(len(EXTENDS)):
            data[EXTENDS[i][1:]] = {}

        for key in self.__func_extents.keys():
            data[key[1:]] = []

        for i in range(len(ls)):
            pth = f".{path}\\{ls[i]}"
            file = os.path.splitext(pth)

            if file[1] == '':
                data["dirs"][ls[i]] = self.data_compose(pth[1:])
            elif file[1] in EXTENDS:
                data[file[1][1:]][file[0]] = pth
            elif file[1] in self.__func_extents.keys():
                data[file[1][1:]].append(self.__func_extents[file[1]](pth))
            else:
                data["content"].append(pth)

        return data
