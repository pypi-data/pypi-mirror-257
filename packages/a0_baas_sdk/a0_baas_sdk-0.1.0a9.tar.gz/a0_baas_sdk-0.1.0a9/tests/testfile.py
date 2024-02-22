from io import BytesIO
import sys
import os
sys.path = [os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))] + sys.path
import a0_baas_sdk.file as file

# upload file

fd = file.upload("hel lo%@$!@#$%^&*()\.txt", b'hello world')
print("[paas] ①  upload success")
print("          file id: ", fd.id)
print("          file url: ", fd.url)

# download file with file id
resp = file.download(fd.id)
print("[paas] ②  download success")
print("          file content: ", resp.decode("utf8"))
# delete file
file.delete(fd.id)
print("[paas] ③  delete success")
# try to dwonload deleted file, this option should failed with FileNotFound
try:
    file.download(fd.id)
except file.FileNotFound:
    print("[paas] ④  can not download deleted file!")