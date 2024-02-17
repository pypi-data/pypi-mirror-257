def ssh上传文件(服务器ip,端口,用户名,密码,本地路径,远程路径):
    import paramiko

    # 设置远程服务器的IP地址、用户名和密码
    hostname = 服务器ip
    port = 端口
    username = 用户名
    password = 密码

    # 设置本地文件路径和远程目标路径
    local_path = 本地路径
    remote_path = 远程路径

    # 创建SSH客户端对象
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # 连接远程服务器
        ssh_client.connect(hostname, port, username, password)

        # 创建SFTP客户端对象
        sftp_client = ssh_client.open_sftp()

        # 上传本地文件到远程服务器
        sftp_client.put(local_path, remote_path)

        print("文件上传成功！")

        # 关闭SFTP客户端连接
        sftp_client.close()

    except Exception as e:
        print("文件上传失败:", e)


    finally:
        # 关闭SSH客户端连接
        ssh_client.close()
def ssh下载文件(服务器ip,端口,用户名,密码,本地路径,远程路径):
    import paramiko

    # 设置远程服务器的IP地址、用户名和密码
    hostname = 服务器ip
    port = 端口
    username = 用户名
    password = 密码

    # 设置远程文件路径和本地目标路径
    remote_path = 远程路径
    local_path = 本地路径

    # 创建SSH客户端对象
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # 连接远程服务器
        ssh_client.connect(hostname, port, username, password)

        # 创建SFTP客户端对象
        sftp_client = ssh_client.open_sftp()

        # 从远程服务器下载文件到本地
        sftp_client.get(remote_path, local_path)

        print("文件下载成功！")

        # 关闭SFTP客户端连接
        sftp_client.close()

    except Exception as e:
        print("文件下载失败:", e)

    finally:
        # 关闭SSH客户端连接
        ssh_client.close()
def ssh上传文件夹(服务器ip,端口,用户名,密码,本地路径,远程路径):
    import paramiko
    import os

    # 设置远程服务器的IP地址、用户名和密码
    hostname = 服务器ip
    port = 端口
    username = 用户名
    password = 密码

    # 设置本地文件夹路径和远程目标路径
    local_folder_path = 本地路径
    remote_folder_path = 远程路径 # 远程服务器上的目标文件夹路径

    # 创建SSH客户端对象
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # 连接远程服务器
        ssh_client.connect(hostname, port, username, password)

        # 创建SFTP客户端对象
        sftp_client = ssh_client.open_sftp()

        # 递归上传本地文件夹到远程服务器
        for root, dirs, files in os.walk(local_folder_path):
            # 创建远程文件夹
            remote_root = os.path.join(remote_folder_path, os.path.relpath(root, local_folder_path))
            try:
                sftp_client.mkdir(remote_root)
            except:
                pass
            for file in files:
                local_file_path = os.path.join(root, file)
                remote_file_path = os.path.join(remote_root, file)
                sftp_client.put(local_file_path, remote_file_path)

        print("文件夹上传成功！")

        # 关闭SFTP客户端连接
        sftp_client.close()

    except Exception as e:
        print("文件夹上传失败:", e)

    finally:
        # 关闭SSH客户端连接
        ssh_client.close()

def ssh下载文件夹(服务器ip, 端口, 用户名, 密码, 远程路径, 本地路径):
    import paramiko
    import os
    import stat
    # 设置远程服务器的IP地址、用户名和密码
    hostname = 服务器ip
    port = 端口
    username = 用户名
    password = 密码

    # 设置远程文件夹路径和本地目标路径
    remote_folder_path = 远程路径
    local_folder_path = 本地路径

    # 创建SSH客户端对象
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # 连接远程服务器
        ssh_client.connect(hostname, port, username, password)

        # 创建SFTP客户端对象
        sftp_client = ssh_client.open_sftp()

        # 递归下载远程文件夹到本地
        def download_dir(remote_dir, local_dir):
            for item in sftp_client.listdir_attr(remote_dir):
                remote_path = remote_dir + '/' + item.filename
                local_path = os.path.join(local_dir, item.filename)
                if stat.S_ISDIR(item.st_mode):
                    os.makedirs(local_path, exist_ok=True)
                    download_dir(remote_path, local_path)
                else:
                    sftp_client.get(remote_path, local_path)

        download_dir(remote_folder_path, local_folder_path)
        print("文件夹下载成功！")

        # 关闭SFTP客户端连接
        sftp_client.close()

    except Exception as e:
        print("文件夹下载失败:", e)

    finally:
        # 关闭SSH客户端连接
        ssh_client.close()
