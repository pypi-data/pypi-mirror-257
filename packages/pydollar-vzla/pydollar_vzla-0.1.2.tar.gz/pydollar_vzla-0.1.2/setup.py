import setuptools

found_packages = setuptools.find_packages(where="src")

with open("README.md", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pydollar_vzla",
    version="0.1.2",
    author="Antonio Vila",
    author_email="vila.antoniojose@gmail.com",
    description="Una librería en Python para obtener el precio del dólar de diferentes fuentes.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AntonioVilaV/pydollar_vzla",
    package_dir={"": "src"},
    packages=found_packages,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
