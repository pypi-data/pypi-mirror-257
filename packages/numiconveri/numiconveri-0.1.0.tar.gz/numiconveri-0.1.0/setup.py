import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="numiconveri",
    version="0.1.0",
    author="Torrez",
    author_email="your@email.com",
    description="Short description of your package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/PYthonCoder1128/numiconveri",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    entry_points={
        "console_scripts": [
            "your_script_name = your_package_name.module_name:main_function"
        ]
    },
)

del setuptools

del long_description
