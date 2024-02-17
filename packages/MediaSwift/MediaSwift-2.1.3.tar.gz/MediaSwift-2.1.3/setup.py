# setup.py
# ---------

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("license.txt", "r", encoding="utf-8") as fh:
    license_text = fh.read()

setup(
    name="MediaSwift",
    version="2.1.3",
    author="ROHIT SINGH",
    author_email="rs3232263@gmail.com",
    description="A MediaSwift PYTHON PACKAGE FOR VIDEO CONVERSION PROBING AND PLAY.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ROHIT-SINGH-1/PYTHON-MEDIASWIFT.git",
    project_urls={
        "Documentation": "https://github.com/ROHIT-SINGH-1/PYTHON-MEDIASWIFT/blob/main/README.md",
        "Source Code": "https://github.com/ROHIT-SINGH-1/PYTHON-MEDIASWIFT",
        "Bug Tracker": "https://github.com/ROHIT-SINGH-1/PYTHON-MEDIASWIFT/issues",
    },
    license="GPL-3.0",
    keywords=["media", "video conversion", "probing"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Topic :: Multimedia :: Video",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    packages=find_packages(),
    package_data={
        "MediaSwift": ["bin/*"],
    },
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "ffpe = MediaSwift.ffpe:ffpe",
            "ffpr = MediaSwift.ffpr:ffpr",
            "ffpl = MediaSwift.ffpl:ffpl",
        ],
    },
    python_requires=">=3.9",
    install_requires=[
        "rich",
    ],
    zip_safe=False,
)
