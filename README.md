
# buzzvil-python-styleguide


[Buzzvil](https://www.buzzvil.com) 의 Python 프로젝트에서 공유되는 flake8, black, mypy의 configuration file들과 flake8의 plugin 모음.

flake8의 플러그인 형태이며, [nitpick](https://nitpick.readthedocs.io/en/latest/index.html)을 사용한다.
공유되는 configuration file들을 local project에 다운받아주는 형식이 **_아닌_**, 공유되는 configuration이 local project에 잘 설정 되어있는지 확인해준다. (configuration file들을 lint해준다)

## 1. How to integrate

### 1.1 Install dependency

#### Using pip-tools

Append to `requirements-dev.in`

```text
buzzvil-python-styleguide==0.1.0
```

#### Using Poetry

Execute code below

```shell script
poetry add buzzvil-python-styleguide@0.1.0
```

### 1.2 Configure nitpick

Append code below to `pyproject.toml` with correct `VERSION` value. (e.g. `0.1.0`)

```toml
[tool.nitpick]
style = "https://github.com/Buzzvil/buzzvil-python-styleguide/raw/{VERSION}/src/buzzvil_python_styleguide/styles/nitpick-style.toml"
```

### 1.3 Run `flake8` to verify configuration

```shell script
flake8 .  # src나 tests가 아닌 `.`가 중요함
```

를 실행하면 local project가 [1.2](#configure_nitpick)에서 설정한 공유 configuration들이 잘 설정 되어있는지 확인해준다.