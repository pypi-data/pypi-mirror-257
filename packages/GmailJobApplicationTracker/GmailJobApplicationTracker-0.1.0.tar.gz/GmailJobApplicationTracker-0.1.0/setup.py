from setuptools import setup, find_packages

setup(
    name='GmailJobApplicationTracker',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'google-auth-oauthlib',
        'google-api-python-client',
        'google-auth-httplib2',
        'spacy',
        'pandas',
        'openpyxl',
        # Add any other dependencies you need
    ],
    entry_points={
        'console_scripts': [
            'track=ApplicationTracker.main:main',
        ],
    },
    # Additional metadata about your package
    author="Eshaan Deshpande",
    author_email="meet.eshaan@gmail.com",
    description="A brief description of your package",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',  # This is important for a markdown README
)