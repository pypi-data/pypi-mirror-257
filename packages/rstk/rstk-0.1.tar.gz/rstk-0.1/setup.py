from setuptools import find_packages, setup

setup(
    name="rstk",
    version="0.1",
    package_dir={"rstk": "src"},
    install_requires=[
        "click",
        "pandas",
        "numpy",
        "scikit-learn",
    ],
    entry_points="""
        [console_scripts]
        rstk=cli:main
    """,
)
