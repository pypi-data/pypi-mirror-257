import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="l0n0lrdp",
    version="1.0.1",
    author="l0n0l",
    author_email="1038352856@qq.com",
    description="屏幕共享",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitee.com/l00n00l/l0n0lrdp",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
    include_package_data=True,
    package_data={
        "": ["*.html"]
    },
    install_requires=[
        "aiohttp"
    ],
    entry_points={
        "console_scripts": [
            "l0n0lrdp = l0n0lrdp.server:start_server",
        ]
    }
)