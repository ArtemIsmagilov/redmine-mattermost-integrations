import subprocess


def patch_mattermostdriver():
    result = subprocess.run('find / -type f -name "websocket.py"', shell=True, stdout=subprocess.PIPE, encoding='utf-8')
    print(f"{result.stdout=}", flush=True)
    path_file = result.stdout.strip()
    if path_file:
        data = open(path_file, mode='r', encoding='utf-8').read().replace('CLIENT_AUTH', 'SERVER_AUTH', 1)
        open(path_file, mode='w', encoding='utf-8').write(data)


if __name__ == '__main__':
    patch_mattermostdriver()
