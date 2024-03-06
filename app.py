import os
import string
from flask import Flask, render_template, request, make_response
from jinja2 import Environment, FileSystemLoader
import json

app = Flask(__name__)
env = Environment(loader=FileSystemLoader(f'{app.template_folder}\\'))
link = '.html'
page_source = app.static_folder + '\\Pages'


def data_compose(path: str) -> dict[str: str or dict or list]:
    """
    Compose data of directory to dict keys -> title, dirs, content + extends(['.css', '.js'])
    :param path: str -> path to dir
    :return: dict -> data, stored by keys (title, dirs, content + extends(['.css', '.js']))
    """
    ls = os.listdir(path)
    extents = ['.css', '.js', '.html']
    data: dict[str: str or dict] = {
        "title": path.split('/')[-1],
        "dirs": {},
        "content": []
    }

    for i in range(len(extents)):
        data[extents[i][1:]] = {}

    for i in range(len(ls)):
        if os.path.isdir(f"{path}/{ls[i]}"):
            data["dirs"][ls[i]] = data_compose(f"{path}\\{ls[i]}")
        else:
            for ex in range(len(extents)):
                if extents[ex] in ls[i]:
                    data[extents[ex][1:]][ls[i].rstrip(string.ascii_letters)[:-1]] = f"{path}\\{ls[i]}"
                    break
            else:
                data["content"].append(f"{path}\\{ls[i]}")

    return data


def create_template(file_name):
    tmp_name = 'Errors/error.html'
    if file_name in os.listdir(page_source):
        data = data_compose(page_source + '\\' + file_name)
        print(data['html'])
        template = env.get_template(data['html']['index'])

        return template.render(data=data)

    return render_template(tmp_name)


def get_type(value: any) -> str:
    print(type(value))
    return str(type(value))


@app.route('/')
def main():
    temp = env.get_template("main_index.html")
    temp.globals.update({'get_type': get_type})
    return temp.render(data=data_compose('static\\Pages\\Gallery'))


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return create_template(path)


if __name__ == '__main__':
    app.run()
