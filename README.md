WSPR Propogation Maps
=====================

Install:
~~~
python3 -m venv .
. ./bin/activate
pip install -r requirements.txt
~~~

Download .gz files from http://wsprnet.org/drupal/downloads to ./data/

Run:
~~~
mkdir ./output
python genmaps.py ./data/[filename].gz
~~~
