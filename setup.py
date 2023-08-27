from setuptools import setup, find_packages


def get_requirements(env=""):
    if env:
        env = "-{}".format(env)
    with open("requirements{}.txt".format(env)) as fp:
        return [x.strip() for x in fp.read().split("\n") if not x.startswith("#")]


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="fastapi_pubsub",
    version="0.1.6",
    author="D Correa",
    author_email="dhiogocorrea@yahoo.com.br",
    description="A simple but yet elegant publish/subscribe socket implementation using FastAPI Websocket.",
    long_description_content_type="text/markdown",
    long_description=long_description,
    url="https://github.com/dhiogocorrea/fastapi-pubsub",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3"
    ],
    python_requires=">=3.8",
    install_requires=get_requirements(),
)
