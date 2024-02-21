from setuptools import setup, find_packages


with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    # 包的名称
    name='ppg_package',

    # 包的版本
    version='0.1.0',

    # 包的作者和联系方式
    author='JunYue Zhuang',
    author_email='1505472915@qq.com',

    # 包的简短描述
    description='A comprehensive package for processing and analyzing PPG signals',

    # 长描述 README文件的内容
    
    long_description=long_description,
    long_description_content_type='text/markdown',
    # 项目的主页，例如GitHub仓库链接
    url='https://github.com/zhuangjunyue/Deep-Learning-Network-for-Extracting-CO-from-PPG-Signals?tab=readme-ov-file',

    # 找到包内所有子包
    packages=find_packages(),

    # 包的依赖项
    install_requires=[
        'numpy',
        'matplotlib',
        'scipy',
        'PyWavelets'  
    ],

    # 包的关键字或标签
    keywords='PPG, signal processing, analysis, FFT, PSD, CWT',

    # 许可证
    license='MIT',

    # 包的分类信息
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],

    # 包含的非代码文件
    include_package_data=True,

    
)
