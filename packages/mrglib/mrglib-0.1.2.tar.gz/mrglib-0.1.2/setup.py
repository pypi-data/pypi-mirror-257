from setuptools import find_packages, setup

setup(
    name='mrglib',
    packages=['mrglib'],
    package_dir={"": "src"},
    version='0.1.2',
    license='MIT',
    url='https://github.com/STEELISI/mrglib',
    download_url='https://github.com/STEELISI/mrglib/archive/refs/tags/0.1.2.tar.gz',
    description='Library wrapping many mrg functionalities',
    author='Jelena Mirkovic, USC/ISI',
    author_email='mirkovic@isi.edu',
    install_requires=['pytest-runner', 'validators', 'paramiko', 'urllib3'],
    keywords=['mrg', 'SPHERE', 'mrglib', 'merge'],
    setup_requires=[],
    tests_require=['pytest'],
    test_suite='tests',
    classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.10'
  ],
)

