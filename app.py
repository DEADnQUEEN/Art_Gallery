import os
import string
import werkzeug.exceptions
from werkzeug.wrappers.response import HTTPStatus
from flask import Flask, redirect, abort, url_for
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
    data: dict[str: str or dict] = {
        "title": path.split(sub)[-1],
        "dirs": {},
        "content": [],
        "html": f'{path.split(sub)[-1]}.html'
    }

    for i in range(len(extents)):
        data[extents[i][1:]] = {}

    for i in range(len(ls)):
        pth = "..\\static" + (f"{path}\\{ls[i]}"[len(app.static_folder):])
        if os.path.isdir(f"{path}/{ls[i]}"):
            data["dirs"][ls[i]] = data_compose(f"{path}\\{ls[i]}")
        else:
            for ex in range(len(extents)):
                if extents[ex] in ls[i]:
                    data[extents[ex][1:]][ls[i].rstrip(string.ascii_letters)[:-1]] = pth
                    print(pth)
                    break
            else:
                data["content"].append(pth)

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


@app.route('/Gallery')
def gallery():
    return create_template('Gallery')


@app.route('/test')
def test():
    return env.get_template('test.html').render()


def error_template(error: HTTPStatus):
    data = data_compose(f'{app.static_folder}\\Error')
    data['code'] = error.value
    data['description'] = error.description
    template = env.get_template(data['html'])
    return template.render(data=data)


@app.route('/Error<int:e>')
def error_load(e: int):
    error: HTTPStatus
    for state in HTTPStatus:
        if state.value == e:
            error = state
            break
    else:
        error = HTTPStatus.NOT_FOUND

    return error_template(error)


@app.errorhandler(werkzeug.exceptions.HTTPException)
def exc(e: werkzeug.exceptions.HTTPException):
    return redirect(url_for('error_load', e=e.code), Response=None, code=HTTPStatus.FOUND)


if __name__ == '__main__':
    app.run()
