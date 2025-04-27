from setuptools import setup, find_packages

setup(
    name="stock-analysis",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "requests>=2.31.0",
        "urllib3>=2.0.0",
        "python-dateutil>=2.8.2",
        "pandas>=2.0.0",
        "yfinance>=0.2.0",
    ],
    extras_require={
        "test": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "pytest-mock>=3.11.1",
        ],
        "dev": [
            "black>=23.7.0",
            "isort>=5.12.0",
            "flake8>=6.1.0",
        ],
    },
    python_requires=">=3.8",
    author="GeethReddy",
    description="Stock Analysis Project",
)
