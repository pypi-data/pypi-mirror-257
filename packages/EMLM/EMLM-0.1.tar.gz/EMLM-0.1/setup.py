from setuptools import setup

setup(
    name='EMLM',
    version='0.1',
    packages=['EMLM'],
    url='https://github.com/yourusername/EMLM',
    license='MIT',
    author='Your Name',
    author_email='sidhuser2690@gmail.com',
    description='A package for Bayesian linear regression with mixture models',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    install_requires=[
        'numpy',
        # Add other dependencies here
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
