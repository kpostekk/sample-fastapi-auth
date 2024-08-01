from pickle import loads, dumps
from base64 import b64encode, b64decode


def read_session(base64str):
    return loads(b64decode(base64str))


def write_session(session) -> str:
    return b64encode(dumps(session)).decode()


with open("b64.txt", "r", encoding="utf8") as f:
    data = f.read()
    s = read_session(data)
    print(data)
    print(s)
    s["user"] = "admin"
    print(write_session(s))
    print(s)

# issa_{osint_done_right}
# Special treat no. 5
