from __future__ import annotations

import os
import types
import inspect
from typing import Union
from jinja2 import Environment, FileSystemLoader
from werkzeug.wrappers.response import HTTPStatus
from flask import abort, Flask

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

    @property
    def main_template(self):
        return self.__main_template

    def __init__(
            self,
            flask: Flask,
            pages_dir_root: str | os.PathLike[str] = "Pages",
            error_dir_root: str | os.PathLike[str] = "Error",
            main_template: str | os.PathLike[str] = "main_index.html"
    ):
        self.__flask = flask
        self.__pages_dir_root: str = pages_dir_root
        self.__error_dir_root: str = error_dir_root

        self.__env = Environment(loader=FileSystemLoader(flask.template_folder))

        if main_template[len(main_template) - len(self.link):] != self.link:
            raise FileExistsError(f"Template file must have '{self.link}' end")

        if main_template not in os.listdir(self.template_folder):
            raise FileExistsError("MainTemplate does not exists")

        self.__main_template: str = main_template

        if not os.path.isdir(self.page_source):
            os.mkdir(self.page_source)


class Functions(Site):
    @property
    def __extends(self):
        return '.css', '.js'

    @staticmethod
    def txt_extend(file: str) -> TYPES:
        with open(file[3:], 'r', encoding='utf-8') as text:
            txt = (text.read()).split('\n')
            out: list = [txt[i] for i in range(len(txt))]

        return out

    def __init__(
            self, flask: Flask,
            pages_dir_root: str | os.PathLike[str] = "Pages",
            error_dir_root: str | os.PathLike[str] = "Error",
            main_template: str | os.PathLike[str] = "main_index.html"
    ):
        super().__init__(flask, pages_dir_root, error_dir_root, main_template)

        sig = inspect.FullArgSpec(['file'], None, None, None, [], None, {'return': 'TYPES', 'file': 'str'})
        prefix = "_extend"

        self.__func_extents: dict[str: types.FunctionType] = {}
        f = inspect.getmembers(Functions, inspect.isfunction)
        for i in range(len(f)):
            if prefix in f[i][0] and sig == inspect.getfullargspec(f[i][1]):
                self.__func_extents['.' + f[i][0].replace(prefix, '')] = f[i][1]

    def create_template(self, folder_name: str) -> str:
        f"""
        Create a page layout by given folder name.
        Must have a same '{self.link}' file at template folder otherwise connection would be aborted.
        :param folder_name: str -> name of folder for create a page template. 
        Must have a same <string:filename>.{self.link}.
        :return: str -> rendered template.
        """
        if folder_name not in os.listdir(self.page_source):
            abort(HTTPStatus.NOT_FOUND)

        data = self.data_compose(self.page_source + '\\' + folder_name)
        template = self.env.get_template(data['html'])

        return template.render(data=data)

    def data_compose(self, path: str) -> dict[str, TYPES]:
        f"""
        Compose data of directory to dict keys -> title, dirs, content + extends({self.__extends}).
        :param path: str -> path to dir.
        :return: dict -> data, stored by keys (title, dirs, content + extends({self.__extends})).
        """
        ls = os.listdir(path)

        title = os.path.split(path)[-1]

        data: dict[str, TYPES] = {
            "title": title,
            "main_template": self.main_template,
            "dirs": {},
            "content": [],
            "html": title + self.link
        }

        for i in range(len(self.__extends)):
            data[self.__extends[i][1:]] = {}

        for key in self.__func_extents.keys():
            data[key[1:]] = []

        for i in range(len(ls)):
            pth = "." + os.path.join(path, ls[i])
            file = os.path.splitext(pth)

            if file[1] == '':
                data["dirs"][ls[i]] = self.data_compose(pth[1:])
            elif file[1] in self.__extends:
                data[file[1][1:]][file[0]] = pth
            elif file[1] in self.__func_extents.keys():
                data[file[1][1:]].append(self.__func_extents[file[1]](pth))
            else:
                data["content"].append(pth)

        return data
