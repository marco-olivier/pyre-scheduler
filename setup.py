from setuptools import setup, find_packages

setup(
    name="pyre-scheduler",
    version="0.1.0",
    author="Marco Olivier",
    author_email="marco.olivier@pyre-scheduler.dev",
    description="Distributed task scheduler for compute workloads",
    packages=find_packages(),
    python_requires=">=3.9",
    install_requires=[
        "redis>=4.5.0",
        "celery>=5.3.0",
        "pydantic>=2.0.0",
    ],
    extras_require={
        "gpu": ["pynvml>=11.0"],
        "dev": ["pytest", "pytest-asyncio"],
    },
)
