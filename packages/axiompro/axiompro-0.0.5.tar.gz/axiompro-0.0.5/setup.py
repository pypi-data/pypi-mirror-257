from setuptools import setup

setup(
	name='axiompro',
	version='0.0.5',
    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points={
        'console_scripts': [
            'axiompro=axiompro.axiom:main'
        ]
    },
)
