python.exe -m venv .venv
.venv/Scripts/activate
pip install -r requirements.txt
python.exe manage.py makemigrations
python.exe manage.py migrate