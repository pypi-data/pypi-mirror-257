from setuptools import setup, find_packages

setup(
    name='real-ids',
    version='0.0.3',
    description='Real Time IDS by whitehat team',
    author='HoangNV2001',
    author_email='HoangNV2001@gmail.com',
    url='https://github.com/HoangNV2001/Real-time-IDS/tree/master',
    install_requires=['tqdm', 'pandas', 'scikit-learn',],
    packages=find_packages(exclude=[]),
    keywords=['security', 'ids', 'security', 'python', 'pypi'],
    python_requires='>=3.6',
    package_data={},
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
