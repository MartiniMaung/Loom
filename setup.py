from setuptools import setup, find_packages

setup(
    name="loom",
    version="1.0.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "typer>=0.9.0",
        "rich>=13.0.0",
        "pydantic>=2.0.0",
        "pydantic-settings>=2.0.0",
        "python-jose>=3.3.0",
        "passlib>=1.7.4",
    ],
    entry_points={
        "console_scripts": [
            "loom=loom.cli:run",
        ],
    },
    python_requires=">=3.9",
)