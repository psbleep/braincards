import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="braincards",
    version="0.0.1",
    author="Patrick Schneeweis",
    author_email="psbleep@protonmail.com",
    description="Punchcards-inspired Brainfuck implementation.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/psbleep/braincards",
    packages=setuptools.find_packages(),
    entry_points={
        "console_scripts": ["braincards=braincards/__main__:main"]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GPLv3",
        "Operating System :: OS Independent",
    ],
)
