from setuptools import setup, find_packages

setup(
    name='beautifultext',
    version='0.0.1',
    description='Beautiful colored console',
    author='ArinaFegus',
    author_email='ArinaFegus@gmail.com',
    install_requires=['tqdm', 'pandas', 'scikit-learn',],
    packages=find_packages(exclude=[]),
    keywords=['color', 'console', 'python', 'pypi'],
    python_requires='>=3.6',
    package_data={'coloredtxt':['libs/*.*']},
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)

