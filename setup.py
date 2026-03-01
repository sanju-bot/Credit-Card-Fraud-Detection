"""
Setup configuration for Credit Card Fraud Detection System
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="credit-card-fraud-detection",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Production-ready credit card fraud detection system with ML and real-time alerts",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/credit-card-fraud-detection",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Financial and Insurance Industry",
        "Topic :: Office/Business :: Financial",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.9",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "fraud-detection=app.app:main",
        ],
    },
    package_data={
        "": ["*.pkl", "*.joblib", "*.csv"],
    },
    include_package_data=True,
    keywords=[
        "fraud-detection",
        "machine-learning",
        "credit-card",
        "random-forest",
        "streamlit",
        "data-science",
    ],
    project_urls={
        "Bug Reports": "https://github.com/yourusername/credit-card-fraud-detection/issues",
        "Source": "https://github.com/yourusername/credit-card-fraud-detection",
        "Documentation": "https://github.com/yourusername/credit-card-fraud-detection#readme",
    },
)
