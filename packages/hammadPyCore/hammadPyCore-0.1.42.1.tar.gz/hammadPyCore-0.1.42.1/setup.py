import setuptools

setuptools.setup(
    name="hammadPyCore",
    version="0.1.42.01",
    author="Hammad Saeed",
    author_email="hammad@supportvectors.com",
    description="Hammad's Python Tools -- Core Library",
    long_description="""
Hammad's Python Tools

Simple Python Utility and LLM Tools.
Documentation available at: https://github.com/hsaeed3/hammad-python
    """,
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',
    install_requires=[
"colorama==0.4.6",
"numpy==1.26.4",
"pandas==2.2.0",
"prompt-toolkit==3.0.43",
"python-dateutil==2.8.2",
"pytz==2024.1",
"six==1.16.0",
"tzdata==2024.1",
"wcwidth==0.2.13",
],
)