import argparse
import re

# 假设你的 setup.py 文件位于项目根目录
SETUP_PY_PATH = 'setup.py'
VERSION_FLAG = 'version'


def increment_version(version_str):
    if (version_str.count(".") == 2):
        # 将版本号字符串分割成主要、次要、补丁部分
        major, minor, patch = map(int, version_str.split('.'))
        # 增加补丁版本号
        new_patch = patch + 1
        # 格式化新的版本号
        new_version = f'{major}.{minor}.{new_patch}'
        return new_version
    elif (version_str.count(".") == 1):
        # 将版本号字符串分割成主要、次要部分
        major, minor = map(int, version_str.split('.'))
        # 增加补丁版本号
        new_minor = minor + 1
        # 格式化新的版本号
        new_version = f'{major}.{new_minor}'
        return new_version
    else:
        # 版本号只有一个数字
        major = int(version_str)
        # 增加补丁版本号
        new_major = major + 1
        # 格式化新的版本号
        new_version = f'{new_major}'
        return new_version


def update_version_in_setup_py(current_version, new_version):
    # 读取 setup.py 文件内容
    with open(SETUP_PY_PATH, 'r') as file:
        content = file.read()

    # 使用正则表达式查找并替换版本号
    updated_content = re.sub(fr'{VERSION_FLAG}\s*=\s*[\'\"]([^\'\"]*)[\'\"]',
                             f'{VERSION_FLAG}=\'{new_version}\'',
                             content,
                             flags=re.MULTILINE | re.IGNORECASE)

    # 将更新后的内容写回 setup.py 文件
    with open(SETUP_PY_PATH, 'w') as file:
        file.write(updated_content)

    print(f'Updated version in {SETUP_PY_PATH}: {current_version} -> {new_version}')


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', help='the file containing the version text', default="setup.py", type=str,
                        required=False)
    parser.add_argument('-n', '--name', help='the version flag name', default='version', type=str, required=False)
    parser.add_argument("-v", "--version", action='version', version='1.0.3', help='print the version flag')
    args = parser.parse_args()
    return args


def main():
    # 解析命令行参数
    args = parse_args()
    if args and args.file and args.file is not None and args.file != "":
        SETUP_PY_PATH = args.file
    if args and args.name and args.name is not None and args.name != "":
        VERSION_FLAG = args.name


    # 读取当前的版本号
    with open(SETUP_PY_PATH, 'r') as file:
        content = file.read()
        match = re.search(fr'{VERSION_FLAG}\s*=\s*[\'\"]([^\'\"]*)[\'\"]', content, flags=re.MULTILINE | re.IGNORECASE)
        if match:
            current_version = match.group(1)
            new_version = increment_version(current_version)
            update_version_in_setup_py(current_version, new_version)
        else:
            print(f"Could not find the version number in {SETUP_PY_PATH}")


if __name__ == '__main__':
    main()
