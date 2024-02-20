
from bigzhu_py.time_z import now


# print whith zh_now time
def now_print(str_in: str):
    t = now()
    print(f"{t} {str_in}", flush=True)


if __name__ == "__main__":
    now_print("Hello, World!")
    now_print("你好，世界！")
    now_print("こんにちは世界！")
    now_print("안녕하세요 세계!")
