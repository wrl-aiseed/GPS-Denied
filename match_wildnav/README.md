https://github.com/TIERS/wildnav

python3.8.10

python3 -m venv venv

source venv/bin/activate

cd wildnav
git submodule update --init --recursive

pip3 install -r requirements.txt

cd src 
python3 wildnav.pu

