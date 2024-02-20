from setuptools import setup, find_packages

setup(
    name='vision_oslo_extension',
    version='0.5.1',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        # your dependencies
        "tk",
        "numpy",
        "pandas",
        "networkx",
        "openpyxl",
        "matplotlib",
    ],
    # entry_points={
    #     'console_scripts': [
    #         'vo_start = vision_oslo_extension.master:main',
    #     ],
    # },
)

