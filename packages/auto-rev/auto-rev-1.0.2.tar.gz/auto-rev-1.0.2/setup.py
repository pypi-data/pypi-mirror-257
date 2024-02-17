from setuptools import setup

setup(
    name='auto-rev',
    version='1.0.2',
    description='auto reversion tool',
    author='alexzshl',
    author_email='alexzshl@126.com',
    # packages=find_packages(),
    entry_points={
        'console_scripts': [
            'auto-rev = main:main'
        ]
    },
    install_requires=[
        # 这里列出你的项目依赖
        'argparse~=1.4.0'
    ],
)
