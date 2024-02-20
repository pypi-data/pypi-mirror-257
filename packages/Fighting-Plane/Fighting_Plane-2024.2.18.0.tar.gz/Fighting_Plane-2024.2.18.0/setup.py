from setuptools import *

setup(
    name="Fighting_Plane",
    version="2024.2.18.0",
    author="Siyuan",
    author_email="yuanbaoge@outlook.com",
    python_requires=">=3.10", 
    packages=find_packages(),
    install_requires=[
       'pygame>=2.4.2'
   ],
    classifiers = [
        'Development Status :: 6 - Mature',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Environment :: MacOS X :: Cocoa',
        'Environment :: Win32 (MS Windows)',
        'Environment :: X11 Applications :: GTK',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows :: Windows 10',
        'Operating System :: Microsoft :: Windows :: Windows 11',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Software Development :: User Interfaces'
    ],
    include_package_data=True
)
