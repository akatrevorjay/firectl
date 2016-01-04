from setuptools import setup

import firectl

try:
    import pypandoc
    long_description = pypandoc.convert("README.md", "rst")
except:
    long_description = ""


setup(
    name="firectl",
    version=firectl.__version__,
    description="Control firejail desktop integration.",
    long_description=long_description,
    url="https://github.com/rahiel/firectl",
    license="GPLv2+",

    py_modules=["firectl"],
    install_requires=["click"],
    entry_points={"console_scripts": ["firectl=firectl:cli"]},

    author="Rahiel Kasim",
    author_email="rahielkasim@gmail.com",
    classifiers=[
        # "Development Status :: 5 - Production/Stable",
        # "Development Status :: 6 - Mature",
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Topic :: Security"
    ],
    keywords="firejail sandbox desktop integration"
)
