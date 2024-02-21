from setuptools import setup, find_packages

with open('requirements.txt', 'r') as f:
    requirements = f.read().splitlines()

requirements = [r for r in requirements if '# build' not in r]

setup(
    name='pybell',
    version='0.1.3',
    packages=find_packages(),
    url='',
    license='',
    author='Oliver Vea',
    author_email='oliver.vea@gmail.com',
    description='Simple module to play a ding with Python.'
                'Useful for notifying you that a long-running shell command is done.',
    include_package_data=True,
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'pybell=pybell:main',
        ],
    },
)
