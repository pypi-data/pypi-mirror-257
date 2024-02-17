import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="utility-sentry",
    version="1.0.0",
    author="Ankit Prajapat",
    author_email="ankitprajapat948@gmail.com",
    description="Utility Sentry provides common components for software"
    " development to reduce developers efforts.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=[
        "utilitysentry",
        "utilitysentry.comman",
        "utilitysentry.config",
        "utilitysentry.exception",
        "utilitysentry.logger",
        "utilitysentry.response",
        "utilitysentry.validation",
        "utilitysentry.validation.helper",
        "utilitysentry.validation.validator_class",
        "utilitysentry.validation.validator_class.boolean",
        "utilitysentry.validation.validator_class.datetime",
        "utilitysentry.validation.validator_class.dictionary",
        "utilitysentry.validation.validator_class.email",
        "utilitysentry.validation.validator_class.list",
        "utilitysentry.validation.validator_class.number",
        "utilitysentry.validation.validator_class.password",
        "utilitysentry.validation.validator_class.phone",
        "utilitysentry.validation.validator_class.regex",
        "utilitysentry.validation.validator_class.set",
        "utilitysentry.validation.validator_class.string",
        "utilitysentry.validation.validator_class.tuple",
        "utilitysentry.validation.validator_class.uuid"
    ],
    install_requires=[
        'PyYAML'
    ]
)
