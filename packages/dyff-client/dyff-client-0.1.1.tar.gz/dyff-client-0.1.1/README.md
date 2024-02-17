# dyff-client

<!-- BADGIE TIME -->

[![pipeline status](https://img.shields.io/gitlab/pipeline-status/dyff/dyff-client?branch=main)](https://gitlab.com/dyff/dyff-client/-/commits/main)
[![coverage report](https://img.shields.io/gitlab/pipeline-coverage/dyff/dyff-client?branch=main)](https://gitlab.com/dyff/dyff-client/-/commits/main)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)
[![code style: black](https://img.shields.io/badge/code_style-black-000000.svg)](https://github.com/psf/black)
[![imports: isort](https://img.shields.io/badge/imports-isort-1674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![code style: prettier](https://img.shields.io/badge/code_style-prettier-ff69b4.svg)](https://github.com/prettier/prettier)

<!-- END BADGIE TIME -->

Python client for the Dyff AI auditing platform.

> Do not use this software unless you are an active collaborator on the
> associated research project.
>
> This project is an output of an ongoing, active research project. It is
> published without warranty, is subject to change at any time, and has not been
> certified, tested, assessed, or otherwise assured of safety by any person or
> organization. Use at your own risk.

## Getting started

### Installation

The Dyff client requires Python 3.8+ and can be installed using pip:

```bash
python3 -m pip install dyff
```

### Setup

```python
from dyff.client import Client

client = Client(api_key="XXXXXX")
```

The API key must be provisioned by a Dyff administrator.

### Usage

```python
dataset = client.datasets.create_arrow_dataset(
    "/my/data", account="XXX", name="mydata"
)
```

For more examples, see the [client
examples](https://docs.dyff.io/examples/client/).

For the full API, see the [client API
reference](https://docs.dyff.io/api-reference/client/).

## License

Copyright 2024 UL Research Institutes.

Licensed under the Apache License, Version 2.0 (the "License"); you may not use
this file except in compliance with the License. You may obtain a copy of the
License at

<http://www.apache.org/licenses/LICENSE-2.0>

Unless required by applicable law or agreed to in writing, software distributed
under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
