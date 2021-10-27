
# buzzvil-python-styleguide

[Buzzvil](https://www.buzzvil.com)에서 Python 코드를 관리하는 툴들과 그 설정파일을 모든 프로젝트에 일괄 적용할 수 있는 일종의 메타 패키지.

## 1. 개요

## 사용하는 툴

### flake8

buzzvil에서 사용하는 설정: [링크](https://github.com/Buzzvil/buzzvil-python-styleguide/blob/master/src/buzzvil_python_styleguide/styles/flake8.toml)

코드 스타일을 검사하는 lint 툴.

#### 잡아낼 수 있는 예시

- 사용되지 않는 `import`
- 코드 한 줄이 너무 긴 경우
- 함수 하나가 너무 긴 경우
- `if`의 중첩의 깊이

#### 사용 예시

##### 주의

**항상 프로젝트의 root directory에서 실행해야함**

`.venv` 같이 dependency가 프로젝트 directory에 포함된 경우 그 코드 또한 flake8의 검사 대상이 됨.
이 경우 [`--extend-exclude`](https://flake8.pycqa.org/en/latest/user/options.html?highlight=exclude#cmdoption-flake8-extend-exclude) 같은 옵션으로 해당 폴더를 제외해야한다.
(**`venv`는 이미 buzzvil의 설정 파일에 exclude 되어있다.**)

```bash
flake8 .
```


### black

buzzvil에서 사용하는 설정: [링크](https://github.com/Buzzvil/buzzvil-python-styleguide/blob/master/src/buzzvil_python_styleguide/styles/black.toml)

코드를 특정한 스타일에 맞게 자동으로 변경해주는 formatter 툴.

#### black과 flake8 역할 차이

flake8과 같이 쓰는 이유는, flake8은 문제를 찾아내기만할뿐 수정해주진 않지만 black은 문제를 자동으로 수정해서 코드를 고쳐준다.

black의 자동화가 있어도 flake8을 쓰는 이유는, black은 찾을 수 없는 문제를 flake8은 찾을 수 있는 경우가 있다. 또한 모든 lint 에러를 자동으로 고칠 수 없기 때문이다. (예시: `if`의 중첩이 너무 깊은 경우)

#### black과 flake8의 실행 순서

보통 black이 자동으로 고칠 문제들은 flake8또한 찾을 수 있기 때문에 black을 먼저 실행하고 flake8로 남아있는 문제들을 확인한다.

black 실행 없이 flake8을 실행하는 경우에는 아래와 같이 두개의 에러가 발생할 수 있다. (`flake8-black`를 설치했기 때문에 `BLK100` 에러가 추가로 발생함. black과 flake8만 설치한다면 `E201`만 발생)

##### 코드

```python
cost_video_owner = models.BigIntegerField( )
```

##### flake8 실행 결과

```
<CODE_PATH>:<LINE_NUMBER>:47: E201 whitespace after '('
<CODE_PATH>:<LINE_NUMBER>:47: BLK100 Black would make changes.
```

#### 사용 예시

**항상 프로젝트의 root directory에서 실행해야함**

[IDE 연동](https://black.readthedocs.io/en/stable/integrations/editors.html) 또한 가능

```bash
black .
```


### mypy

buzzvil에서 사용하는 설정: [링크](https://github.com/Buzzvil/buzzvil-python-styleguide/blob/master/src/buzzvil_python_styleguide/styles/mypy.toml)

Python 3 이상부터 사용되는 Type Annotation을 기반으로 코드의 타입 안정성을 확인하는 정적분석 툴.

#### 사용 예시

```bash
mypy -p <PACkAGE_NAME> -p <PACKAGE_NAME>
```

아래와 같이 project root directory에 python package가 존재하는게 아니라면 `MYPYPATH=src`를 앞에 붙여줘야함 (최종: `MYPYPATH=src mypy -p package_a -p package_b`)

```
.
├── pyproject.toml
├── setup.cfg
└── src
    ├── package_a
    │   └── __init__.py
    └── package_b
        └── __init__.py
```

## 설정파일들의 일괄 적용 방식

`nitpick`이라는 flake8의 plugin을 사용한다. https://github.com/andreoliwa/nitpick

간단하게 설명하면, https://github.com/Buzzvil/buzzvil-python-styleguide/tree/master/src/buzzvil_python_styleguide/styles 의 파일들에서 볼 수 있듯, 파일과 (예: `setup.cfg`) 해당 파일에 있어야할 설정값을 정의해놓으면, flake8 실행시 그 파일들 읽어서 설정값이 포함되어있는지 확인한다.

한마디로 코드 대신 설정값을 lint 하는 플러그인.

---

## 2. How to integrate

### 2.1 기존 dependency 삭제

`requirements-dev.in` 혹은 `requirements.in` 에서 flake8, black, mypy관련된 모든 패키지를 삭제한다.

### 2.2 `buzzvil-python-styleguide` 추가

`requirements-dev.in` 에 아래 라인을 추가한다.

(아래의 패키지는 공식 pypi에는 업로드 되지않고 buzzvil private pypi에 올라가있다.)

```
buzzvil-python-styleguide==LATEST_RELEASE
```

`Django`를 사용하는 프로젝트라면 `buzzvil-python-styleguide[django]`와 같이 쓸 수 있다.

### 2.3 `pyproject.toml` 파일 작성

`pyproject.toml`에 아래 항목 추가 (파일이 없다면 project root directory에 추가)

```toml
[tool.nitpick]
style = "py://buzzvil_python_styleguide/styles/nitpick-style.toml"
```

### 2.4 툴들의 설정파일 적용

Project의 root directory에서 `flake8 .` 을 실행하면 `NIP324` 에러가 발생하면서 아래와 같은 메시지가 나올 수 있다.

2.3 에서 설정한 `nitpcik`이 `nitpick-style.toml`을 읽어서 설정값을 강제하기 때문에 발생하는 에러이며, 에러 메시지에서 지목하는 파일에 `Use this:` 아래의 값을 추가하면 된다.

아래의 경우 `setup.cfg`에 `[flake8]`로 시작하는 라인들을 추가하면 해결됨

```
./setup.py:0:1: NIP324 File setup.cfg: section [flake8] has some missing key/value pairs. Use this:
[flake8]
max-annotations-complexity = 4
max-line-length = 120
max-parameters-amount = 10
max-pos_args = 2
per-file-ignores = tests/**.py:FI18,CFQ001,E501,__init__.py:F401
pytest-parametrize-values-type = tuple
require-code = True
```

### 2.4 CI 및 docker-compose, Makefile에서 각 툴의 실행줄 수정

1 을 참고해서 flake8, black, mypy의 실행줄을 변경한다.
