from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="",
    author="Steven Zindel <steven.zindel@gmail.com>",
    description="",
    long_description=long_description,
    version="0.1.0",
    packages=find_packages(include=["funcfactory", "funcfactory.*"]),
)


from distutils.core import setup
setup(
    name = 'funcfactory',         # How you named your package folder (MyLib)
    packages = ['funcfactory'],   # Chose the same as "name"
    version = '0.1',      # Start with a small number and increase it with every change you make
    license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    description = 'Python package The FuncFactory! Easily adaptable production grade code on the fly.',   # Give a short description about your library
    author = 'Steven Zindel',                   # Type in your name
    author_email = 'steven.zindel@gmail.com',      # Type in your E-Mail
    url = 'https://github.com/szindel/FuncFactory',   # Provide either the link to your github or to your website
    download_url = 'https://github.com/user/reponame/archive/v_01.tar.gz',    # I explain this later on
    keywords = ['FuncFactory', 'Functions', 'Production'],   # Keywords that define your package best
    install_requires=['PyYAML==5.4.1'],
    classifiers=[
        'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Developers',      # Define that your audience are developers
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',   # Again, pick a license
        'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)