from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.1.4'
DESCRIPTION = 'Dynamic menu for easier customization'
LONG_DESCRIPTION = "It's a tool to create a dynamic shell menu with easier customization by json." \
                   "This module is under development and will become more powerful."

# Setting up
setup(
    name="menu_setter3",
    version=VERSION,
    Home_page="https://github.com/pksenpai/MenuSetter",
    author="Parsa Ahmadian(PKPY)",
    author_email="<p3ahmadian@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=open('README.md').read(),
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'menu', 'dynamic', 'dynamic menu', 'menu setter', 'python menu', 'terminal'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
