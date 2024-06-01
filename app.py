import os
import string
import types
import werkzeug.exceptions
from werkzeug.wrappers.response import HTTPStatus
from flask import Flask, redirect, abort, request
from jinja2 import Environment, FileSystemLoader

app = Flask(__name__)
link = '.html'
page_source = app.static_folder + '\\Pages'
env = Environment(loader=FileSystemLoader(app.template_folder))


def data_compose(path: str) -> dict[str: str or dict or list]:
    """
    Compose data of directory to dict keys -> title, dirs, content + extends(['.css', '.js'])
    :param path: str -> path to dir
    :return: dict -> data, stored by keys (title, dirs, content + extends(['.css', '.js']))
    """
    ls = os.listdir(path)
    sub = '\\'
    extents = ['.css', '.js']

    def text_extend(file_path: str) -> dict:
        out = {
            'title': '',
            'subtitle': '',
            'content': '',
            'footer': '',
        }

        with open(file_path[3:], 'r', encoding='utf-8') as text:
            lines = text.readlines()
            for line in range(len(lines)):
                out[list(out.keys())[line]] = lines[line][:-1]

        return out

    func_extents: dict[str: types.FunctionType] = {
        '.txt': text_extend
    }

    data: dict[str: str or dict or list or int] = {
        "title": path.split(sub)[-1],
        "dirs": {},
        "content": [],
        "html": f'{path.split(sub)[-1]}.html'
    }

    for i in range(len(extents)):
        data[extents[i][1:]] = {}

    for key in func_extents.keys():
        data[key[1:]] = []

    for i in range(len(ls)):
        pth = "..\\static" + (f"{path}\\{ls[i]}"[len(app.static_folder):])
        if os.path.isdir(f"{path}/{ls[i]}"):
            data["dirs"][ls[i]] = data_compose(f"{path}\\{ls[i]}")

        else:
            for ex in range(len(extents)):
                if extents[ex] in ls[i]:
                    data[extents[ex][1:]][ls[i].rstrip(string.ascii_letters)[:-1]] = pth
                    break
            else:
                for key in func_extents.keys():
                    if key in ls[i]:
                        data[key[1:]].append(func_extents[key](pth))
                        break
                else:
                    data["content"].append(pth)

    data['blocks'] = min(len(data['content']), len(data['txt']))

    return data


def create_template(filename):
    if filename not in os.listdir(page_source):
        abort(HTTPStatus.NOT_FOUND)

    data = data_compose(page_source + '\\' + filename)
    template = env.get_template(data['html'])
    return template.render(data=data)


@app.route('/')
def main():
    return redirect('Gallery', Response=None, code=HTTPStatus.FOUND)


@app.route('/Gallery', methods=['GET'])
def gallery():
    return create_template('Gallery')


@app.route('/Abstract', methods=['GET'])
def abstract():
    return create_template('Abstract')


@app.route('/Minimalism', methods=['GET'])
def minimalism():
    return create_template('Minimalism')


@app.route('/Modern', methods=['GET'])
def modern():
    return create_template('Modern')


@app.route('/Portrait', methods=['GET'])
def portrait():
    return create_template('Portrait')


@app.route('/About', methods=['GET'])
def about():
    return create_template('About')


@app.errorhandler(werkzeug.exceptions.HTTPException)
def exc(e: werkzeug.exceptions.HTTPException):
    data = data_compose(f'{app.static_folder}\\Error')
    data['code'] = e.code
    data['description'] = e.description
    template = env.get_template(data['html'])

    return template.render(data=data)


if __name__ == '__main__':
    app.run()
