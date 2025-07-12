import uvicorn

import api.app as app


def run_api():
    uvicorn.run(app.app, host='127.0.0.1', port=8000)


if __name__ == '__main__':
    run_api()
    