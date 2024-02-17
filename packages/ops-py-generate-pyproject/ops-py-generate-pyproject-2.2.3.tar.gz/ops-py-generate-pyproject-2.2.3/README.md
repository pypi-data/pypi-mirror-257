# generate-pyproject

## Before you begin
Please refer to the [example-code](https://pypi.org/project/ops-py-example-code)
if you are planning on writing a Python package and distribute it to https://pypi.org

---

## Usage

### Install this package:
`pip install ops-py-generate-pyproject`


### Export the VERSION and PROJECT_NAME environment variables 
The PyPI project name and version, e.g.:

```
export VERSION=1.2.3
export PROJECT_NAME=my-fabulous-projects
```

### Run the code
Be sure to be in the directory where the `src` dir of you code is located. Then run the following:   
`python3 -m generate_pyproject.generate_pyproject`

When executing the above code, the following files should then be generated in the `src/my-fabulous-projects` directory:   
- `setup.py`
- `pyproject.toml`

### Build the pip package
Be sure to be inside the `src` directory and then run:   
`python -m build`

### Upload to pypi.org
Be sure to be inside the `src` directory and then run:   
`python -m twine upload --verbose dist/*`