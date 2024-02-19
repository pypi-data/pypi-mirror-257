from setuptools import setup, find_packages

setup(
  name='turkle-monitoring',
  version='0.1.4',
  packages=find_packages(),
  install_requires = [
    "pandas",
    "numpy",
    "matplotlib",
    "scikit-learn"
  ],
  author="Turkle",
  author_email="jonathan@turkle.io",
  description="Monitoring package for credit scoring models",
  url="https://github.com/Turkle-io/turkle-monitoring",
  classifiers=[
    'Operating System :: OS Independent',
    'Programming Language :: Python :: 3.11',
  ]
)