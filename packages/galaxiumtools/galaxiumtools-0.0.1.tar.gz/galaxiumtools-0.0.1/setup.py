from setuptools import setup

setup(
    name="galaxiumtools",
    version="0.0.1",
    description="Tools to interact with an AI cluster",
    url="https://github.com/helloerikaaa/galaxium-tools",
    author="Erika Sánchez-Femat",
    author_email="erikasafe@gmail.com",
    license="BSD 2-clause",
    packages=["galaxiumtools"],
    install_requires=["minio", "mlflow", "loguru", "tqdm"],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
