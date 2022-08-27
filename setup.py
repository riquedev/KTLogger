import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="KTLogger",
    version="0.0.1",
    author="Henrique da Silva Santos",
    author_email="henrique.santos@4u360.com.br",
    description="""KT Logger allows you to read and download log files from the Django admin page.
    KT Log is based on Django Log Viewer.""",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="Apache License 2.0",
    url="https://github.com/riquedev/django-initials-avatar",
    keywords="logs,logger,kt,koter, framework, django",
    project_urls={
        "Bug Tracker": "https://github.com/riquedev/django-advanced-wallet/issues",
        "Repository": "https://github.com/riquedev/django-advanced-wallet",
    },
    install_requires=[
        'Django>=3.2.14',
        'datefinder',
        'django_mock_queries',
        'file_read_backwards'
    ],
    classifiers=[
        "Framework :: Django",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3"
    ],
    packages=setuptools.find_packages(exclude=("kt_logger", "kt_logger.*", "tests", "logs", "example_app","resources",)),
    include_package_data=True,
    python_requires=">=3.7"
)
