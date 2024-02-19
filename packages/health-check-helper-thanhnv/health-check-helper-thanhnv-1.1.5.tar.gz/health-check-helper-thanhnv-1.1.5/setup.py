from pathlib import Path

import setuptools

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()


setuptools.setup(
    name="health-check-helper-thanhnv",
    version="1.1.5",
    author="LinLin",
    author_email="nguyenthanh2303@gmail.com",
    description="",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/thanhnv2303/HelpTool",
    project_urls={
        "Bug Tracker": "https://github.com/thanhnv2303/HelpTool",
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9'
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src",exclude=[ 'tests']),
    # python_requires=">=3.6",
    install_requires=[
        'requests>=2.26.0',
        'sortedcontainers>=2.4.0',
        'pyspnego==0.9.2',
        'requests-kerberos==0.14.0'
    ]
)