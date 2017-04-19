from setuptools import setup

tests_require = [
    'lektor',
    'pytest',
    'pytest-cov',
    ]

setup(
    name='lektor-datetime-helpers',
    description='Lektor plugin to help with dates and times',
    author=u'Jeff Dairiki',
    author_email='dairiki@dairiki.org',
    url='https://github.com/dairiki/lektor-datetime-helpers',
    version='0.1',
    license='BSD',
    py_modules=['lektor_datetime_helpers'],
    tests_require=tests_require,
    install_requires=[
        'tzlocal',
        ],
    extras_require={'testing': tests_require},
    entry_points={
        'lektor.plugins': [
            'datetime-helpers = lektor_datetime_helpers:DatetimeHelpersPlugin',
        ]
    }
)
