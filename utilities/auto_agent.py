# import paramiko
#
# # 创建一个通道
# transport = paramiko.Transport(('47.110.134.247', 22))
# transport.connect(username='root', password='Sipras67905856')
#
# # 实例化SSHClient
# client = paramiko.SSHClient()
# client._transport = transport
#
# # 打开一个Chanent并执行命令
# order0 = "cd / && "
# order1 = "cd /usr/local/webserver/nginx/backend/bilibili && "
# order2 = "cat data.xlsx"
#
# stdin, stdout, stderr = client.exec_command(order0 + order1 + order2)
# # stdout 为正确输出，stderr为错误输出，同时是有1个变量有值
#
#
# # 打印结果
# print(stdout.read().decode('utf8'))
# print(stdout.err().decode('utf8'))
#
# # 关闭连接
# transport.close()

import paramiko

trans = paramiko.Transport(('47.110.134.247', 22))

trans.connect(username='root', password='Sipras67905856')

sftp = paramiko.SFTPClient.from_transport(trans)

# put('你要上传的文件','上传的位置+文件名')
# sftp.put('jdd', '/opt/newjdd')
# get('你要下载的文件','下载的位置+文件名')
sftp.get('/usr/local/webserver/nginx/backend/bilibili/data.xlsx', '20200214.xlsx')

sftp.close()
