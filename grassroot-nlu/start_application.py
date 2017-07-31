from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Here we will put some things!'


if __name__ == '__main__':
    app.run()
