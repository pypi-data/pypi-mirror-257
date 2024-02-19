import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


# install requirements
install_requires = [
    'numpy>=1.25',
    'scipy>=1.11',
]


# Read version file
version_info = {}
with open("cdosolve/_version.py") as f:
    exec(f.read(), version_info)


setup(
    name='cdosolve',
    version=version_info['__version__'],
    # description="CDO solve",
    # author="Guillermo Navas-Palencia",
    # author_email="g.navas.palencia@gmail.com",
    # url="https://github.com/guillermo-navas-palencia/cdosolve",
    packages=['cdosolve'],
    platforms="any",
    include_package_data=True,
    license="Apache Licence 2.0",
    python_requires='>=3.9',
    install_requires=install_requires,
    tests_require=['pytest'],
    classifiers=[
        'Topic :: Scientific/Engineering :: Mathematics',
        'Topic :: Office/Business :: Financial',
        'Topic :: Software Development :: Libraries',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3'],
    keywords='finance risk quantitative'
)