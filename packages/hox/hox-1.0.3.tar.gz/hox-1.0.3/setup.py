from setuptools import setup

setup(
    name='hox',
    version='1.0.3',
    license='MIT',
    url = 'https://github.com/usedToBeTomas/hox',
    author='usedToBeTomas',
    description='Lightweight nn library project.',
    packages=['hox'],
    python_requires='>=3.6',
    keywords = ['neural network', 'ml', 'ai', 'machine learning','vanilla','nn'],
    install_requires=[
        'numpy',
        'tqdm'
    ],
)
