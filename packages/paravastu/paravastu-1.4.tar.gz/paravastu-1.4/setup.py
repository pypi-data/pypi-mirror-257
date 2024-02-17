import setuptools

setuptools.setup(
    name="paravastu",  # Replace with your own username
    version="1.4",
    author="Paravastu Lab",
    long_description="lab package",
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
    install_requires=["numpy", "pandas", "biopandas"],
)
