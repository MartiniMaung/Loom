from setuptools import setup, find_packages

setup(
    name="loom-os",
    version="0.1.0",
    description="The Open-Source Pattern Weaver",
    author="Loom Collective",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.10",
    install_requires=[
        "pydantic>=2.0",
        "typer>=0.9.0", 
        "rich>=13.0",
        "networkx>=3.0",
        "python-dotenv>=1.0",
    ],
    entry_points={
        "console_scripts": [
            "loom=loom.cli:run",
        ],
    },
)
