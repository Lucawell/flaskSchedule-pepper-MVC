import secrets

# 生成一个随机的密钥
secret_key = secrets.token_hex(16)  # 16字节的密钥
print(secret_key)