import logging
from pathlib import Path

import pytest
from test_utils import temporary_env_var

import aglog.loader.yaml_loader as target

test_config = """
version: 1
disable_existing_loggers: False
formatters:
  simple:
    format: '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
handlers:
  console:
    class: logging.StreamHandler
    formatter: simple
    stream: ext://sys.stdout
root:
  level: ${LOG_LEVEL:-WARNING}
  handlers: [console]
dummy:
  none: ${TEST:-test}
  prefix: prefix.${TEST:-test}
  postfix: ${TEST:-test}.postfix
  both: prefix.${TEST:-test}.postfix
"""

no_env_var_config = """
version: 1
"""


def test_load_yaml(tmp_path: Path) -> None:
    yaml_path = tmp_path / "test.yaml"

    with yaml_path.open("w") as f:
        f.write(test_config)

    with temporary_env_var("LOG_LEVEL", "DEBUG"):
        res = target.load_yaml(yaml_path)
    assert res["root"]["level"] == "DEBUG"

    res = target.load_yaml(yaml_path)
    assert res["root"]["level"] == "WARNING"

    # config file not found
    with pytest.raises(FileNotFoundError):
        target.load_yaml(tmp_path / "not_found.yaml")

    # no env var
    no_env_yaml_path = tmp_path / "no_env_var.yaml"
    with no_env_yaml_path.open("w") as f:
        f.write(no_env_var_config)
    res = target.load_yaml(no_env_yaml_path)
    assert res == {"version": 1}

    # prefix postfix
    with temporary_env_var("TEST", "test"):
        res = target.load_yaml(yaml_path)
    assert res["dummy"]["none"] == "test"
    assert res["dummy"]["postfix"] == "test.postfix"
    assert res["dummy"]["prefix"] == "prefix.test"
    assert res["dummy"]["both"] == "prefix.test.postfix"


def test_dict_config_from_yaml(tmp_path: Path) -> None:
    yaml_path = tmp_path / "test.yaml"

    with yaml_path.open("w") as f:
        f.write(test_config)

    with temporary_env_var("LOG_LEVEL", "INFO"):
        target.dict_config_from_yaml(yaml_path)
    assert logging.getLogger().level == logging.INFO

    target.dict_config_from_yaml(yaml_path)
    assert logging.getLogger().level == logging.WARNING
