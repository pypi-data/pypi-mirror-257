from setuptools import setup, find_packages

setup(
    name='pybell',
    version='0.1.5',
    packages=find_packages(),
    url='',
    license='',
    author='Oliver Vea',
    author_email='oliver.vea@gmail.com',
    description='Simple module to play a ding with Python'
                'Useful for notifying you that a long-running shell command is done.',
    include_package_data=True,
    install_requires=[
        'audioplayer~=0.6',
        'xdialog~=1.1.1.1'
    ],
    entry_points={
        'console_scripts': [
            'pybell=pybell:main',
        ],
    },
)
