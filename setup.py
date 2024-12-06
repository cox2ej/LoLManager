from setuptools import setup, find_packages

setup(
    name="lol_manager",
    version="0.1.0",
    author="Your Name",
    description="A League of Legends team management simulation game",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'lol_manager': [
            'src/database/schema.sql',
            'src/data/*.py',
            'src/ui/assets/*',
        ],
    },
    install_requires=[
        'PyQt6>=6.4.0',
    ],
    entry_points={
        'console_scripts': [
            'lol_manager=src.main:main',
        ],
    },
    python_requires='>=3.8',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: End Users/Desktop',
        'Topic :: Games/Entertainment :: Simulation',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Operating System :: Microsoft :: Windows',
    ],
)
