from distutils.core import setup
from pathlib import Path

# read the contents of your README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

# setup function
setup(
    name = 'lppinv',
    packages = ['lppinv'],
    version = '0.4.0',
    license = 'MIT',
    description = 'A non-iterated general implementation of the LPLS estimator for cOLS, TM, and custom cases',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author = 'econcz',
    author_email = '29724411+econcz@users.noreply.github.com',
    url = 'https://github.com/econcz/lppinv',
    download_url = 'https://github.com/econcz/lppinv/archive/pypi-0_4_0.tar.gz',
    keywords = [
        'estimator', 'linear programming', 'least squares',
        'OLS constrained in values', 'transaction matrix', 'custom',
        'pseudoinverse', 'singular value decomposition',
        'numpy', 'scipy', 'statsmodels'
    ],
    install_requires = ['numpy>=1.19', 'scipy>=1.10', 'statsmodels'],
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Mathematics',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
  ],
)
