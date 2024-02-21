import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="flowmelet",
    version="0.0.7",
    author="yhow",
    author_email="yhow11@gmail.com",
    description="Flowmelet - Airflow DAG Compile-time Generator with unified features from Airflow, dagfactor, Gusty, and DBT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yhow101/flowmelet.git",
    packages=setuptools.find_packages(),
    include_package_data=True,
    package_data={'': ['static/*', 'flowmelet/templates/*']},
    install_requires=[
        "apache-airflow",
        "Jinja2",
        "PyYAML",
        "argparse"
    ],
    entry_points={
        "console_scripts": [
            "flowmelet = flowmelet.main:main",
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License'
    ],
    python_requires=">=3.6",
)