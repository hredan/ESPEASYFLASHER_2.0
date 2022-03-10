if  not exist "./venv" (
    py -3 -m venv ./venv
    call ./venv/Scripts/activate.bat
    python -m pip install -r requirements.txt
) else (
    call ./venv/Scripts/activate.bat
)
cd ..
coverage run -m pytest tests
coverage html
htmlcov\index.html
pause