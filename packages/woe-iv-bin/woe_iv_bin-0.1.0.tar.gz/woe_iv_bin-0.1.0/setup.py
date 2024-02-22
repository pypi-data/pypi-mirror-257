from setuptools import setup, find_packages

setup(
    name='woe_iv_bin',
    version='0.1.0',
    packages=find_packages(),
    description='A Python Library for WoE, IV Calculation, and Continuous Binning Optimization.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Kwadwo Daddy Nyame Owusu - Boakye',
    author_email='kwadwo.owusuboakye@outlook.com',
    url='https://github.com/knowusuboaky/woe-iv-bin',
    install_requires=[
        "pandas>=1.1.5",
        "numpy>=1.19.5",
        "matplotlib>=3.3.3",
        "seaborn>=0.11.1",
        'pandas>=1.0.0'
    ],
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    keywords=['woe', 'iv', 'binning', 'feature-engineering', 'weight of evidence', 'optimization', 'scoring', 'predictive-modeling']
)
