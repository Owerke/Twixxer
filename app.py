from bottle import get, view, run

@get("/")
@view("index")
def _():
    return "Hello World"

run(host='localhost', port=6969)
