from setuptools import setup

docs = """
Simple Python 3 obfuscator

Support many techniques, such as exec expression, variable renaming, etc.

To use it, simply type "obfsimp" in terminal

There are many example programs and obfuscated programs at the examples folder
"""
setup(
    name="obfsimp",
    version="1.0.0",
    description="Simple Python 3 obfuscator",
    long_description=docs,
    packages=["obfsimp", "obfsimp.methods", "obfsimp.examples"],
    classifiers=[
        "Programming Language :: Python :: 3 :: Only",
        "Operating System :: OS Independent",
    ],
    keywords=["obfuscator"],
    entry_points={"console_scripts": ["obfsimp=obfsimp.cli:_cli"]},
    install_requires=["pygments"],
    python_requires=">=3",
)
