from setuptools import setup, find_packages

setup(
    name="trigger_informer_scan",
    version="0.2",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.1"
    ],
    author="Paul Collingwood",
    author_email="paul.collingwood@informer.io",
    description="Trigger scans in Informer via your CI/CD pipeline",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'triggerInformerScan=trigger_informer_scan.trigger:main',
        ],
    },
)
