import werkzeug.exceptions
from werkzeug.wrappers.response import HTTPStatus
from flask import redirect, abort, Flask
from site_data import Functions

app = Flask(__name__)
functions = Functions(app)


@app.route('/')
def main_route():
    return redirect('Gallery', Response=None, code=HTTPStatus.FOUND)


@app.route('/<string:page>')
def pages(page: str):
    if page in functions.pages:
        return functions.create_template(page)
    elif page.capitalize() in functions.pages:
        return redirect(f'/{page.capitalize()}', Response=None, code=HTTPStatus.FOUND)
    return abort(HTTPStatus.NOT_FOUND)


@app.errorhandler(werkzeug.exceptions.HTTPException)
def exc(e: werkzeug.exceptions.HTTPException):
    data = functions.data_compose(functions.error_folder)
    data['code'] = e.code
    data['description'] = e.description
    template = functions.env.get_template(data['html'])

    return template.render(data=data)


def main():
    app.run()


if __name__ == '__main__':
    main()
