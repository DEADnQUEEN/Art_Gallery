import os
import string
from flask import Flask, render_template
from jinja2 import Environment, FileSystemLoader

app = Flask(__name__)
link = '.html'
page_source = app.static_folder + '\\Pages'


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
        pth = "..\\static" + f"{path}\\{ls[i]}"[len(app.static_folder):]
        if os.path.isdir(f"{path}/{ls[i]}"):
            data["dirs"][ls[i]] = data_compose(f"{path}\\{ls[i]}")
        else:
            for ex in range(len(extents)):
                if extents[ex] in ls[i]:
                    data[extents[ex][1:]][ls[i].rstrip(string.ascii_letters)[:-1]] = pth
                    break
            else:
                data["content"].append(pth)

    return data


def create_template(filename):
    if filename not in os.listdir(page_source):
        filename = "Error"

    env = Environment(loader=FileSystemLoader(app.template_folder))
    data = data_compose(page_source + '\\' + filename)
    template = env.get_template(data['html'])
    return template.render(data=data)


@app.route('/')
def main():
    return create_template('Gallery')


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return create_template(path)


if __name__ == '__main__':
    app.run()
