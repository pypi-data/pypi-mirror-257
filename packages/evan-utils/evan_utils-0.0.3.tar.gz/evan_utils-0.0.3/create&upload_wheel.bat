cd D:\Projects\create_whl
rmdir /s dist

python -m build
pip install --upgrade twine
python -m twine upload --repository pypi dist/*
pypi-AgEIcHlwaS5vcmcCJGIxMmJiNTIzLTdkNzQtNGI2MS1iMGM2LTg2ZDMyNjQ4ZjBiZAACKlszLCJlZWVlYTI5Mi03MTNiLTQyYmQtYTk3Yi1hYzI3MTJjNzE1YTQiXQAABiABjNHOg3OJ_kl5hrRHOdzEmoofuXB_Cydiuhxe0eJrYA

pause