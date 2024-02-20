import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='bpx-api',
    version='1.0.0',
    author='syp25815',
    author_email='syp25815@gmail.com',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url=' https://github.com/syp25815/bpx-api-py',
    packages=setuptools.find_packages(),
)
