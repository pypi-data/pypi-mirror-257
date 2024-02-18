from setuptools import setup, find_packages

setup(
    name='fahoorm',
    version='0.1.0',
    author='Lhoussaine HSSINI and  Fatma KARKACH',
    author_email='bontop.2028@gmail.com',
    description='A custom ORM framework for Python',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/lhoussaine-HSSINI/fahoorm',
    packages=find_packages(),
    install_requires=[
        'pymysql',
        'psycopg2',
        'pymongo',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
