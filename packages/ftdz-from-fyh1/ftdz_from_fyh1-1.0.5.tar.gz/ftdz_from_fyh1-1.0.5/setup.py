import setuptools
setuptools.setup(
    name='ftdz_from_fyh1',
    version='1.0.5',
    author='bob',
    author_email='56141537@qq.com',
    description='a game.',
    long_description_content_type="""text/markdown""",
    url='https://www.github.com/',
    packages=['ftdz_from_fyh1'],
    install_requires=['pygame','requests'],#需要下载的第三方库
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ]
)
