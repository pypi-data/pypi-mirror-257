# AKM Addition Package

AKM Addition Package is a simple Python package that provides an addition operation. It includes a basic implementation of addition and unit tests to ensure its correctness.

## Project Structure

```plaintext
akmaddition/
|-- akmaddition/
|   |-- __init__.py
|   `-- operations.py
|-- setup.py
|-- README.md
```

## Installation
create a virtual env
```bash
python3 -m venv env
source env/bin/activate
```

Install the package:
```bash 
pip install git+https://github.com/vishal-meshram/akmaddition.git
```
## How to use this package
```bash
>python3
>>> from akmaddition.operations import Operations
>>> op = Operations()
>>> numbers = [2, 3, 4, 5]  # Example list of numbers
>>> sum_result = op.addition(numbers)
>>> product_result = op.multiplication(numbers)
```
### Added renovate bot in the git repo
Installation of renovate bot:
```bash
https://github.com/apps/renovate
```
configure the renovate on repo.

#### added the renovate.json5 file in the project