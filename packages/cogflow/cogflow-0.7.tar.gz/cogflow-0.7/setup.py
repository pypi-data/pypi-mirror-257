from setuptools import setup, find_packages

setup(
    name='cogflow',
    version='0.7',
    author='Sai_kireeti',
    author_email='sai.kireeti@hiro-microdatacenters.nl',
    description='cog modules',
    packages=find_packages(),
    install_requires=[
        'mlflow[extras]',
        'kfp[extras]==1.8.22',
        'tensorflow[extras]',
        'boto3[extras]',
	'tenacity[extras]',
	'pandas[extras]',
	'numpy[extras]',
	'kubernetes[extras]',
	'minio[extras]',
	'scikit-learn[extras]',
	'awscli[extras]',
	's3fs[extras]',
	'setuptools[extras]',
	'kserve[extras]'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)

