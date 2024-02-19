from setuptools import find_packages, setup

setup(
    name='voliboli_pdf_scraper',
    version='1.8',
    package_dir= {"": "src"},
    packages=find_packages(where="src"),
    description='Voliboli PDF Scraper',
    author='Teodor Janez Podobnik',
    license='MIT',
    install_requires=["tabula-py", "numpy"],
    test_suite='tests'
)
