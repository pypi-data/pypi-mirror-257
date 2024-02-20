import os
import re

from setuptools import setup, find_packages

def read_requirements():
    with open("requirements.txt", "r") as f:
        return [line.strip() for line in f.readlines()]

def read_version(init_file_path):
    with open(init_file_path, "r") as f:
        content = f.read()
        version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", content, re.M)
        if version_match:
            return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

def write_version(init_file_path, version):
    with open(init_file_path, "r+") as f:
        content = re.sub(r"(^__version__ = ['\"])([^'\"]*)(['\"])",
                         f"\\g<1>{version}\\g<3>", f.read(), flags=re.M)
        f.seek(0)
        f.write(content)
        f.truncate()

def increment_version(version_str):
    major, minor, patch = map(int, version_str.split('.'))
    return f"{major}.{minor}.{patch + 1}"

def generate_py_modules_list(directory, root_directory=None, prefix="fhailib"):
    """
    주어진 디렉토리 및 하위 디렉토리 내의 모든 .py 파일에 대한 모듈 리스트를 생성합니다.
    이 리스트는 setup.py 파일 내의 py_modules 매개변수에 사용될 수 있습니다.

    Parameters:
    - directory (str): .py 파일을 검색할 디렉토리의 경로입니다.
    - root_directory (str): 최상위 디렉토리의 경로입니다. 재귀 호출에 사용됩니다.
    - prefix (str): 모듈 경로 앞에 추가할 이전 경로 또는 프리픽스입니다.

    Returns:
    - List[str]: 모든 .py 파일의 모듈 경로 리스트를 반환합니다.
    """
    if root_directory is None:
        root_directory = directory

    py_modules = []
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.endswith(".py") and filename != "__init__.py":
                module_relative_path = os.path.relpath(os.path.join(root, filename), root_directory)
                module_path = module_relative_path.replace('.py', '').replace(os.sep, '.')
                # 이전 경로(프리픽스)가 제공된 경우, 모듈 경로 앞에 추가
                if prefix:
                    module_path = f"{prefix}.{module_path}"
                py_modules.append(module_path)

    return py_modules

# 경로 설정
directory = 'E:\\Mytask\\main\\module\\fhailib\\fhailib'
init_file_path = os.path.join(directory, '__init__.py')

# 버전 업데이트
current_version = read_version(init_file_path)
new_version = increment_version(current_version)
write_version(init_file_path, new_version)

# py_modules 리스트 생성
py_modules_list = generate_py_modules_list(directory)
print(py_modules_list)
setup(
    name='fhailib',
    version='1.0.6',
    description='FH,FJ Vision AI SYSTEM LIB',
    author='LEE_DH',
    author_email='ldh9616@nate.com',
    url='https://github.com/LEE-pyt/AI_Module.git',
    install_requires=read_requirements(),
    packages=find_packages(exclude=[]),
    py_modules=py_modules_list,
    classifiers=[
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
)