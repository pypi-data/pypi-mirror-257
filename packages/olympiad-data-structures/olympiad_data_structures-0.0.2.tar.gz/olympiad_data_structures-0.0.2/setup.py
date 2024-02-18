from setuptools import setup

install_requires = ["bitarray"]

setup(
    name="olympiad_data_structures",
    version="0.0.2",
    install_requires=install_requires,
    use_scm_version=True,
    packages=["src.olympiad_data_structures"],
    include_package_data=True,
)
