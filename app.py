import os
from flask import Flask, render_template
from jinja2 import Environment, FileSystemLoader
app = Flask(__name__)
env = Environment(loader=FileSystemLoader(f'{app.template_folder}/'))


@app.route('/')
def main():
    temp = env.get_template("index.html")
    return temp.render(data_source=[
            {
                "title": dir_name,
                "image_sources": [
                    f'static/Pages/{dir_name}/image_names/' + link
                    for link in os.listdir(f'static/Pages/{dir_name}/image_names')
                ],
            }
            for dir_name in os.listdir('static/Pages')
        ])


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def sub_directory(path):
    if path + '.html' in os.listdir(f'./{app.template_folder}'):
        return render_template(path + '.html')

    return render_template('error.html')


if __name__ == '__main__':
    app.run()
