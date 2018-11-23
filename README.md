# xross_common
[![CircleCI](https://circleci.com/gh/alunir/xross_common.svg?style=svg)](https://circleci.com/gh/alunir/xross_common)

This repo contains common library for alunir project.

## SystemUtil
:memo: SystemUtil refers a **relative** path where ini files located, as an environment variable CONFIG_PATH.
For instance, in test cases, CONFIG_PATH should set "tests" because test_config.ini located at DOCKER_DIST_DIR / CONFIG_PATH.
In another module importing SystemUtil, DOCKER_DIST_DIR and CONFIG_PATH should be set.
 - DOCKER_DIST_DIR = the full path to the another module importing SystemUtil
 - CONFIG_PATH = the relative path to the another module


## How to install
```bash
python setup.py install
```

## How to run tests
```bash
python setup.py test
```