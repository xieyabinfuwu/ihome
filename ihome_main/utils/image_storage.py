# -*- coding: utf-8 -*-
import logging


from qiniu import Auth, put_data

#需要填写的Ａccess Key 和　Ｓecret Key
access_key = 'RZfjRv-CzQ0VV4h7pqYrcIxwznc80PqVZEtMMyDN'
secret_key = 'pE6sI4lU7rChvL7VeugRw8BOFe1cj6ZsxKtpuzQ1'

#要上传的空间
bucket_name = 'ihome'

def storage(data):
    """七牛云存储上传文件接口"""
    if not data:
        return None
    try:
        #构建鉴权对象
        q = Auth(access_key,secret_key)
        #生成上传Ｔoken,可以指定过期时间
        token = q.upload_token(bucket_name,None, 3600)
        #上传文件
        ret,info = put_data(token,None,data)
    except Exception as e:
        logging.error(e)
        raise e
    if info and info.status_code != 200:
        raise Exception("上传文件到七牛失败")
    #返回七牛中保存的图片名，这个图片名也是访问七牛获得图片的路径
    print(info)
    print(ret)
    return ret["key"]


if __name__ == '__main__':
    # file_name = input("输入上传的文件")
    with open("./1.jpg","rb") as f:
        storage(f.read())
