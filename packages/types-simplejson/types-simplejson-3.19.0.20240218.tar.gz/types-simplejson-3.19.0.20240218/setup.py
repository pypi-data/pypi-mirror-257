from setuptools import setup

name = "types-simplejson"
description = "Typing stubs for simplejson"
long_description = '''
## Typing stubs for simplejson

This is a [PEP 561](https://peps.python.org/pep-0561/)
type stub package for the [`simplejson`](https://github.com/simplejson/simplejson) package.
It can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
PyCharm, etc. to check code that uses
`simplejson`.

This version of `types-simplejson` aims to provide accurate annotations
for `simplejson==3.19.*`.
The source for this package can be found at
https://github.com/python/typeshed/tree/main/stubs/simplejson. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/main/README.md for more details.
This package was generated from typeshed commit `e961db9492aee8afc998ed9e95e055503d96dcfe` and was tested
with mypy 1.8.0, pyright 1.1.342, and
pytype 2024.2.13.
'''.lstrip()

setup(name=name,
      version="3.19.0.20240218",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/simplejson.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['simplejson-stubs'],
      package_data={'simplejson-stubs': ['__init__.pyi', 'decoder.pyi', 'encoder.pyi', 'errors.pyi', 'raw_json.pyi', 'scanner.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      python_requires=">=3.8",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
