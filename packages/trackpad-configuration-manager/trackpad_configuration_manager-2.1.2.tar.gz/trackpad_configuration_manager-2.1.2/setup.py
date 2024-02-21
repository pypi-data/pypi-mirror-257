import setuptools
from setuptools.command.install import install

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


def download_cmsis_packs(install_lib):
    import os
    import requests

    # URLs and download paths
    urls = [
        'https://www.keil.com/pack/Keil.STM32F0xx_DFP.2.1.1.pack',
        'http://www.keil.com/pack/Keil.STM32G0xx_DFP.1.4.0.pack',
        'https://www.keil.com/pack/Keil.STM32U5xx_DFP.2.0.0.pack'
    ]
    download_paths = [
        'cmsis-pack/Keil.STM32F0xx_DFP.2.1.1.pack',
        'cmsis-pack/Keil.STM32G0xx_DFP.1.4.0.pack',
        'cmsis-pack/Keil.STM32U5xx_DFP.2.0.0.pack'
    ]

    for url, download_path in zip(urls, download_paths):
        # download to the subfolder download_path
        abs_download_path = os.path.join(install_lib, "trackpad_configuration_manager", download_path)

        os.makedirs(os.path.dirname(abs_download_path), exist_ok=True)

        print("Downloading file from {} to {}".format(url, abs_download_path))
        response = requests.get(url)
        with open(abs_download_path, 'wb') as f:
            f.write(response.content)


class InstallCmsisPack(install):
    def run(self):
        print("Running custom installation install logic...")
        # Download the files
        download_cmsis_packs(self.install_lib)

        # Continue with the default installation process
        install.run(self)


setuptools.setup(
    name="trackpad_configuration_manager",
    version="2.1.2",
    author="Pascal-Frédéric St-Laurent",
    author_email="pfstlaurent@boreas.ca",
    description="Trackpad Configurator Library that allows to read/write configuration/calibration files (json format) "
                "from/to a device",
    long_description=long_description,
    long_description_content_type="text/markdown",
    zip_safe=False,
    url="https://github.com/BoreasTechnologies/trackpad-configurator-plus-plus.git",
    packages=[
        'trackpad_configuration_manager',
        'trackpad_configuration_manager.probe',
        'trackpad_configuration_manager.utils',
        'trackpad_configuration_manager.boreas_data_converter'],
    classifiers=[
        "License :: Other/Proprietary License",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.11",
        "Operating System :: Microsoft :: Windows",
    ],
    install_requires=[
        "auto-py-to-exe==2.36.0",
        "cmsis-pack-manager==0.5.2",
        "crc==1.3.0",
        "flake8==6.1.0",
        "pyocd==0.34.3",
        "PySide6==6.5.2",
        "intelhex==2.3.0",
        "requests==2.31.0",
        "build",
        "twine",
        "setuptools"
    ],
    setup_requires=[
        "setuptools",
        "requests",
    ],
    cmdclass={
        'install': InstallCmsisPack,
    },
    include_package_data=True,
    python_requires='>=3.11',
)
