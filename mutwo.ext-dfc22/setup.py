import setuptools  # type: ignore


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

extras_require = {"testing": ["nose", "coveralls"]}

setuptools.setup(
    name="mutwo.ext-dfc22",
    version="0.2.0",
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
        "mutwo.ext-core>=0.57.1, <0.58.0",
        "mutwo.ext-music>=0.8.0, <1.0.0",
        "mutwo.ext-mbrola>=0.2.0, <1.0.0",
        "mutwo.ext-zimmermann>=0.3.5, <0.4.0",
        "mutwo.ext-csound>=0.3.0, <0.4.0",
        "mutwo.ext-isis>=0.7.0, <0.8.0",
        "mutwo.ext-common-generators>=0.8.1, <0.9.0",
        # To make ascii art like images
        "pillow==8.3.2",
        # To draw vector based letters
        "Qahirah==1.1",
        # Utility to draw vector based letters
        # (abstraction of geometrical figures).
        "geometer==0.3.2",
        # For caching variables (mutwo compute lazy function)
        "cloudpickle==2.0.0",
        "progressbar2==4.0.0",
        "quicktions==1.13",
        # "moviepy==2.0.0.dev2",
    ],
    extras_require=extras_require,
    python_requires=">=3.9, <4",
)
