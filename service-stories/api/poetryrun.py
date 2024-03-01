import subprocess
import uvicorn


def watch():
    subprocess.run(
        'ptw --runner "pytest -v" --onpass "/usr/bin/say yes" --onfail "/usr/bin/say no"',
        shell=True,
    )


def test():
    subprocess.run(["pytest"], check=True)


def dev():
    uvicorn.run("api.main:app", host="0.0.0.0", port=8001, reload=True)
