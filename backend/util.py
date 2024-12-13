import bcrypt

bytes = "username=alwexis;email=redthelegendarytrainer@gmail.com;version=1.0.0".encode('utf-8')
salt = bcrypt.gensalt(14)
hash = bcrypt.hashpw(bytes, salt) 
with open("./user.wavebond", "w") as f:
    f.write(str(hash))