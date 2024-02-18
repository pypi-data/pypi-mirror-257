from setuptools import setup

import setuptools

setup(
    name="akatsuki_kafka",
    version="0.1.0",
    author="Akatsuki",
    description="Kafka consumer & producer abstraction for Akatsuki",
    packages=setuptools.find_packages(),
    install_requires=["protobuf", "aiokafka"],
    python_requires=">=3.9",
)