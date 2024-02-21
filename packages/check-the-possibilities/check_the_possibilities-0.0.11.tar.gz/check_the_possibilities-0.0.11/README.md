# Prototype python library

This library is implemented for educational purposes



To update the library you need:
1. Refactor code
2. Update requirements if it needs
3. Update the library version number
4. In the terminal, run the following commands sequentially:
 - python setup.py sdist bdist_wheel
 - twine upload --repository pypi dist/*