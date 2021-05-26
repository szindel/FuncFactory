from setuptools import setup

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))

with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name = 'funcfactory',         # How you named your package folder (MyLib)
    packages = ['funcfactory'],   # Chose the same as "name"
    python_requires=">=3.7",
    version = '0.1.6',      # Start with a small number and increase it with every change you make
    license='Apache 2.0',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    long_description=long_description,
    long_description_content_type='text/markdown',
    description = 'Python package The FuncFactory! Easily adaptable production grade code on the fly.',   # Give a short description about your library
    author = 'Steven Zindel', # Type in your name
    author_email = 'steven.zindel@gmail.com', # Type in your E-Mail
    url = 'https://github.com/szindel/FuncFactory',   # Provide either the link to your github or to your website
    download_url = 'https://github.com/user/reponame/archive/v_01.tar.gz',    # I explain this later on
    keywords = ['FuncFactory', 'Functions', 'Production Code'],   # Keywords that define your package best
    classifiers=[
        'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Developers',      # Define that your audience are developers
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',   # Again, pick a license
        'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
