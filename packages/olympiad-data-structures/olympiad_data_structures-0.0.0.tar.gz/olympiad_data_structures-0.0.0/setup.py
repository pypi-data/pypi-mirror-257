from setuptools import find_packages, setup

install_requires = ["bitarray"]

setup(
    name="olympiad_data_structures",
    install_requires=install_requires,
    use_scm_version=True,
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
)
