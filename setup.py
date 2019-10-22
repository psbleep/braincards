import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="braincards",
    version="0.0.2",
    author="Patrick Schneeweis",
    author_email="psbleep@protonmail.com",
    description="Punchcards-inspired Brainfuck implementation.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/psbleep/braincards",
    packages=setuptools.find_packages(),
    include_package_data=True,
    python_requires=">=3",
    install_requires=[
        "bfi==1.0.2",
        "Pillow==6.2.0",
        "RPi.GPIO==0.6.5",
        "picamera==1.13"
    ],
    entry_points={
        "console_scripts": ["braincards=braincards.__main__:main"]
    },
    license="GPLv3",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX",
        "Intended Audience :: Developers",
        "Topic :: Software Development",
    ],
)
