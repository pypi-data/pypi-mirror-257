## fixtup-minio-s3

[![ci](https://github.com/FabienArcellier/fixtup-minio-s3/actions/workflows/main.yml/badge.svg)](https://github.com/FabienArcellier/fixtup-minio-s3/actions/workflows/main.yml)

> NOT READY YET, WORK IN PROGRESS !!!

The `fixtup-minio-s3` plugin allows you to download the files of a fixture into an s3 bucket managed by minio 
and run the integration tests on an s3 bucket.

The plugin also allows you to manage the life cycle of the bucket on which the files are loaded by recreating 
it between each test or by emptying it between each test.

``tests/integrations/test_s3_sdk.py``
```python
import fixtup

with fixtup.up('minio'), \
    fixtup.up('s3_content'):
    # the files are loaded into the s3 bucket
    # the integration tests are running
```

Once the plugin is installed and activated in fixtup, we declare the `minio.yml` manifest in a fixture so 
that it loads the files into an s3 bucket when launched.

`tests/fixtures/s3_content/minio.yml`
```yaml
minio_endpoint: http://localhost:9000 # [optional], default : http://localhost:9000
authentification: minioadmin:minioadmin # [optional], default : minioadmin:minioadmin
bucket: bucket # [optional], default : bucket
setup_data_bucket_policy: new_bucket | clear_bucket | none # [optional], default : new_bucket
copy_ignore: [] # [optional], default : []
```

it is possible to exclude files from copying to the s3 bucket using the `copy_ignore` parameter

```yaml
copy_ignore:
  - 'file.svg'
  - '**/*.svg'
```

# Links

* Documentation : https://fixtup-minio-s3.readthedocs.io/en/latest
* PyPI Release : https://pypi.org/project/fixtup-minio-s3
* Source code: https://github.com/FabienArcellier/fixtup-minio-s3
* Chat: https://discord.gg/nMn9YPRGSY

## The latest version

You can find the latest version to ...

```bash
git clone https://github.com/FabienArcellier/fixtup-minio-s3.git
```

## Usage

The `minio` fixture starts a minio server using docker-compose. The `s3_content` fixture creates the bucket 
if it is absent and copies the fixture files into the bucket.

```python
import fixtup

with fixtup.up('minio'), \
    fixtup.up('s3_content'):
    # the files are loaded into the s3 bucket
    # the integration tests are running
    pass
```

`test/fixtures/minio/docker-compose.yml`
```yaml
version: '3.8'
services:
  database:
    image: quay.io/minio/minio
    command: server /data
    ports:
      - 9000:9000
      - 9001:9001
```

`test/fixtures/s3_content/minio.yml`
```yaml
minio_endpoint: http://localhost:9000 # [optional], default : http://localhost:9000
authentification: minioadmin:minioadmin # [optional], default : minioadmin:minioadmin
bucket: bucket # [optional], default : bucket
setup_data_bucket_policy: new_bucket | clear_bucket | none # [optional], default : new_bucket
copy_ignore: [] # [optional], default : []
```

### Publish the library on pypi

The publication use a tag-based workflow to run the publication on github action. First, a developper tag a commit using `alfred publish`, then github action publish the library on pypi.

The `alfred publish` take the version number from pyproject.toml. The command will raise an error if the current branch is not master, if changes are in progress, or if the tag already exists, if the branch is not synchronized with remote branch

```bash
alfred publish
```

### Develop with gitpod

[gitpod](https://www.gitpod.io/) can be used as an IDE. You can load the code inside to try the code.

[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/FabienArcellier/fixtup-minio-s3)

## Developper guideline

### Add a dependency

``bash
poetry add requests
``
### Install development environment

Use make to instanciate a python virtual environment in ./venv and install the
python dependencies.

```bash
poetry install
```

### Update release dependencies

Use make to instanciate a python virtual environment in ./venv and freeze
dependencies version

```bash
poetry update update
```

### Activate the python environment

When you setup the requirements, a `venv` directory on python 3 is created.
To activate the venv, you have to execute :

```bash
poetry shell
```

### Run the continuous integration process

Before commit or send a pull request, you have to execute `pylint` to check the syntax
of your code and run the unit tests to validate the behavior.

```bash
$ poetry run alfred ci
```

## Contributors

* Fabien Arcellier

## License

MIT License

Copyright (c) 2024-2024 Fabien Arcellier

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
