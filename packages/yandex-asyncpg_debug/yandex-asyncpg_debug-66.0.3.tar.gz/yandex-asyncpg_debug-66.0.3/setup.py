from setuptools import setup
from setuptools.command.install import install


class InstallCommand(install):
    def run(self):
        raise RuntimeError("You are trying to install a stub package yandex-asyncpg_debug. Maybe you are using the wrong pypi?")


setup(
    name='yandex-asyncpg_debug',
    version='66.0.3',
    author='Yandex',
    author_email='security@yandex-team.ru',
    url='https://ya.ru',
    readme="README.md",
    long_description="""This is a security placeholder package.""",
    long_description_content_type='text/markdown',
    description='A package to prevent Dependency Confusion attacks against Yandex.',
    cmdclass={
        'install': InstallCommand,
    },
)
