import werkzeug.exceptions
from werkzeug.wrappers.response import HTTPStatus
from flask import redirect, abort, Flask
from site_data import Functions

app = Flask(__name__)
functions = Functions(app)


@app.route('/')
def main():
    return redirect('Gallery', Response=None, code=HTTPStatus.FOUND)


@app.route('/<string:page>')
def pages(page: str):
    if page in functions.pages:
        return functions.create_template(page)
    return abort(HTTPStatus.NOT_FOUND)


@app.errorhandler(werkzeug.exceptions.HTTPException)
def exc(e: werkzeug.exceptions.HTTPException):
    data = functions.data_compose(f'{app.static_folder}\\Error')
    data['code'] = e.code
    data['description'] = e.description
    template = functions.env.get_template(data['html'])

    return template.render(data=data)


if __name__ == '__main__':
    app.run()
