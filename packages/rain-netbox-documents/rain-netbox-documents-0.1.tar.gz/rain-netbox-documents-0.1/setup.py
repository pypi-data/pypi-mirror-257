from setuptools import find_packages, setup

setup(
    name='rain-netbox-documents',
    version='0.1',
    author='Gabri Botha',
    author_email='gabri.botha@rain.co.za',
    description='Simple document manager for rain NetBox',
    install_requires=[],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)

