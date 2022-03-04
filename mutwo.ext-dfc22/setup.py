import setuptools  # type: ignore


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

extras_require = {"testing": ["nose", "coveralls"]}

setuptools.setup(
    name="mutwo.ext-dfc22",
    version="0.1.0",
    license="GPL",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Levin Eric Zimmermann",
    author_email="levin.eric.zimmermann@posteo.eu",
    packages=[
        package
        for package in setuptools.find_namespace_packages(include=["mutwo.*"])
        if package[:5] != "tests"
    ],
    setup_requires=[],
    install_requires=[
        "mutwo.ext-core>=0.55.0, <0.56.0",
        "mutwo.ext-music>=0.7.0, <1.0.0",
        "mutwo.ext-mbrola>=0.2.0, <1.0.0",
        "mutwo.ext-zimmermann>=0.1.1, <0.2.0",
        "mutwo.ext-csound>=0.3.0, <0.4.0",
        # To make ascii art like images
        "pillow==8.1.2",
        # To draw vector based letters
        "Qahirah==1.1",
        # Utility to draw vector based letters
        # (abstraction of geometrical figures).
        "geometer==0.3.2",
    ],
    extras_require=extras_require,
    python_requires=">=3.9, <4",
)
