from app.server import create_app
from wsgiref.simple_server import make_server

app = create_app()

if __name__ == '__main__':
    with make_server('0.0.0.0', 8000, app) as httpd:
        httpd.serve_forever()
