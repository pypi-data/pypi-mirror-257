import setuptools
with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()
setuptools.setup(
    name="michaelPanUtilsLib",  # 库的名称
    version="0.0.3",  # 库的版本号
    author="chuntong pan",  # 库的作者
    author_email="panzhang1314@gmail.com",  # 作者邮箱
    description="Commonly Used Functions.",  # 库的简述
    install_requires=['pillow', 'michaelPanPrintLib', 'numpy', 'pydantic'],  # 需要的依赖库
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires='>=3.8',
    platforms=["all"],
    include_package_data=True,
    package_data={
        'michaelPanUtilsLib': ['static/*']
    },
    packages=setuptools.find_packages(),
    classifiers=["Programming Language :: Python :: 3", "Operating System :: OS Independent"],
)
