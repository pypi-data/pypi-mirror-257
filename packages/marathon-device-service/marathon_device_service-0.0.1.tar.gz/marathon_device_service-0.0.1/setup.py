from setuptools import setup, find_packages

setup(
    name='marathon_device_service',
    version='0.0.1',
    author='MarathonLabs',
    author_email='em@marathonlabs.io',
    description='A Python library to manage a device in Marathon Cloud.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://marathonlabs.io',
    packages=find_packages(),
    install_requires=[
        'requests',
        'python-magic',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    include_package_data=True,
    keywords='camera media upload service Marathon Cloud device emulator Android',
)
