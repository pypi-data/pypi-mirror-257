# pydantic-wrangler

## Description
pydantic-wrangler was born out of the necessity of representing data (originally serialized in YAML files) as python 
objects not only capable of exhibiting complex business-logic behaviors, but also ensuring stringent data validation.

As a result, it streamlines the process of parsing data from various serialization formats into Pydantic models, and if 
necessary, re-serializing them back into any supported format. In essence, pydantic-wrangler serves as a comprehensive 
tool for your data, facilitating a seamless journey from serialization to deserialization (and back, if you so wish).

## Installation

Install it with pip:
```bash
pip install pydantic-wrangler
```

or poetry:
```bash
poetry add pydantic-wrangler
```


## Features

- **Pydantic Integration**: Converting serialized data into Python objects is the oldest trick in the book, but pydantic-wrangler 
elevates this process by directly converting the data into Pydantic models, which brings the added advantage of robust 
data validation. The models used in this process are defined by classes that inherit from either the 
***PydanticWranglerBaseModel*** or ***PydanticWranglerRenderableModel***. This not only provides flexibility in setting up 
behaviors for your data, but also ensures data integrity through Pydantic's validation mechanisms.


- **Multiple Formats Support**: Currently, it supports loading serialized data from JSON, YAML, TOML  and INI streams/files.
While support for other formats is planned, the package is designed to be easily extensible. Adding your own loader function(s) 
to support additional formats (and/or to include use-case specific business-logic) is as simple as defining them in a python module 
(.py file) and creating an env var with name 'LOADERS_MODULE' containing the python dotted path to that module. 
For more information, please refer to the [Custom Loaders](#custom-loaders) section.  

## Table of Contents [pending]
- [Usage](#usage)
- [Base Models](#base-models)
- [Loaders](#custom-loaders)
- [Dumpers](#custom-dumpers)
- [Extensibility](#configs)
- [Example use-case](#example-use-case)
- [Contributing](#contributing)

