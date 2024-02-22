from setuptools import setup, find_packages

# with open("README", "r") as f:
#     long_description = f.read()

setup(
    name="cyp2d6_parser",
    version="0.0.5",
    license="MIT",
    description="Parser to match CYP2D6 parsing reccomendations by PharmVar.",
    author="Andrew Haddad, PharmD",
    author_email="andrew.haddad@pitt.edu",
    packages=find_packages(),
    entry_points={"console_scripts": ["cyp2d6_parser = cyp2d6_parser.__main__:main"]},
    install_requires=["pandas", "numpy"],
    package_data={"cyp2d6_parser": ["*.csv"]},
    include_package_data=True,
)
