from setuptools import setup, find_packages
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read().splitlines()
setup(
    name = 'email_in_validate',
    version = '2.1.2',  
    author = 'Abdiel Wilson',
    author_email = 'wilsonabdiel86@gmail.com',
    license = 'MIT License',
    description = 'This Python function, email_validator, checks if an input string is a valid email address',
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = 'https://github.com/Wilsonabdiel/regex-gen',
    py_modules = ['email_in_validate', 'app'],
    packages = find_packages(),
    install_requires = requirements,
    python_requires='>=3.7',
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
    ],
    entry_points = '''
        [console_scripts]
        cooltool=my_tool:cli
    '''
)