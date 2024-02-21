from setuptools import setup, find_packages

setup(
    name='forfloatrange',
    version='1.0.5',
    packages=find_packages(),
    description='Range with float',
    author='Nova D Andrew',
    author_email='andrew.d.nova@icloud.com',
    python_requires='>=3.6',
    license='MIT',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
