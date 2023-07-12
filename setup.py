from setuptools import setup, find_packages

setup(
    name='aiworkflows',
    version='0.0.1',
    url='https://github.com/ai-workflows/sdk',
    description='AI Workflows Python SDK',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Joseph Vitko',
    author_email='me@josephvitko.com',
    license='MIT',
    install_requires=[
        'requests',
    ],
    python_requires='>=3.10',
    classifiers=[
        'Development Status :: 1 - Planning',
    ]
)