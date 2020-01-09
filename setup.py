from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='travelplanner',
    version='0.0.1',
    packages=find_packages(
        exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    description="Arrange a best trip for passengers\
        with different speed and destination",
    author='Shouyi',
    author_email='907501712@qq.com',
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=('numpy', 'matplotlib'),
    url='https://github.com/UCL/mphy0021-2019-travel-planner-SWang999',
    entry_points={
        'console_scripts': [
            'bussimula = travelplanner.command:process'
        ]}
)
