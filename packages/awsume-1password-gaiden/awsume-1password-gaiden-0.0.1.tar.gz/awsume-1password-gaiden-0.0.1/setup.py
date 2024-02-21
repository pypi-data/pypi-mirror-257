from setuptools import setup

setup(
    name='awsume-1password-gaiden',
    version='0.0.1',
    long_description='Fetches AWS access keys and MFA from 1Password',
    description='Fetches AWS access keys and MFA from 1Password',
    entry_points={
        'awsume': [
            'onepassword = onepassword'
        ]
    },
    author='Sam Simpson',
    author_email='pypi@sams.wtf',
    url='https://github.com/samsimpson1/awsume-1password',
    py_modules=['onepassword'],
)
