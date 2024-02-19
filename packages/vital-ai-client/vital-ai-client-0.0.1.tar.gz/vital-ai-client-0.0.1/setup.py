from setuptools import setup, find_packages

setup(
    name='vital-ai-client',
    version='0.0.1',
    author='Marc Hadfield',
    author_email='marc@vital.ai',
    description='Vital.ai API Client',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/vital-ai/vital-client-python',
    packages=find_packages(),
    license='Apache License 2.0',
    install_requires=[
            'vital-ai-vitalsigns',
            'vital-ai-domain',
            'vital-ai-aimp'
        ],
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',
)
