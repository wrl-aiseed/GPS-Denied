https://github.com/TerboucheHacene/visual_localization

python3.8.10

python3 -m venv venv

source venv/bin/activate

git submodule update --init --recursive

pip install poetry

poetry install

poetry install --only main

poetry shell

python scripts/main.py


