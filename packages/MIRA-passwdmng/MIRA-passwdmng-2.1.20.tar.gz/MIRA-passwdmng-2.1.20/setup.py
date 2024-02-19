from setuptools import setup

setup(
        name='MIRA-passwdmng',
        version='2.1.20',
        py_modules=['mira'],
        install_requires=[
            'cryptography',
            'termcolor',
            'argon2-cffi',
            'prompt-toolkit',
            'password-strength',
            'validators',
            'phonenumbers'
        ],
        entry_points={
            'console_scripts': [
                'mira = mira:main',
            ],
        },
        description='Girasec Solutions introduces Mira. Mira is our innovative password management solution designed specifically for the command-line interface (CLI). With a streamlined and efficient approach, Mira provides a robust solution to the vulnerabilities associated with password management in the digital era.',
        long_description=open('README.md').read(),
        long_description_content_type='text/markdown',
        author='veilwr4ith && icode3rror',
        author_email='girasecsolutions@gmail.com',
        url='https://github.com/GiraSec/MIRA_lite',
        classifiers=[
            'Programming Language :: Python :: 3',
        ],
)
