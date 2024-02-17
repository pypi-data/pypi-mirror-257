from setuptools import setup


setup(
    name='qshader',

    packages=['qshader'],

    version='1.0.0',

    license='MIT',

    description='QShader - Shaders support for 2D PyQt Games.',

    long_description_content_type='text/x-rst',
    long_description=open('README.rst', 'r').read(),

    author='Ivan Perzhinsky.',
    author_email='name1not1found.com@gmail.com',

    url='https://github.com/xzripper/qshader',
    download_url='https://github.com/xzripper/qshader/archive/refs/tags/v1.0.0-alpha.tar.gz',

    keywords=['pyqt', 'qt', 'shaders', 'games', '2d'],

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Games/Entertainment',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3'
    ]
)
