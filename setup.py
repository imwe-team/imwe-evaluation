from setuptools import setup


setup(
    name='imweEvalTools',
    version='0.0.1',
    description='A module containing useful methods for analyzing the evaluation of the IMWe with survs.com',
    url='https://github.com/jebuss/imwe-evaluation',
    author='Jens Buss',
    author_email='jens.buss@tu-dortmund.de',
    license='MIT',
    packages=[
        'eval_tools',
    ],
    # package_data={
    #     '': ['resources/*', 'credentials/credentials.encrypted']
    # },
    # tests_require=['pytest>=3.0.0'],
    # setup_requires=['pytest-runner'],
    install_requires=[
        'numpy',
        'matplotlib>=1.8',
        'python-dateutil',
        'setuptools',
        'pandas',
        'tables',  # pytables in anaconda
        'click'
    ],
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'imwe_eval_extract_comments = eval_tools.scripts.extractComments:main',
            'imwe_eval_extract_ws_comments = eval_tools.scripts.extractWsComments:main',
        ],
        }
)
