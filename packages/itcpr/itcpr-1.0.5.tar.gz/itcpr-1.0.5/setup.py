import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name="itcpr",
    version="1.0.5",
    description="Your tools for ITCPR",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/abdussamiakanda/itcpr-tools",
    author="Md. Abdus Sami Akanda",
    author_email="abdussamiakanda@gmail.com",
    license="MIT",classifiers=[
    'Programming Language :: Python :: 3',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    ],
    py_modules=["spintronics"],
    package_dir={'': 'src'},
    install_requires=[],
)