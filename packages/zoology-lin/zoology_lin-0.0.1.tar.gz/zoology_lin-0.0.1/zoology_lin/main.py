import itertools

case_list = ["用户名", "密码"]
value_list = ["OK", "KO"]

def gen_case(item=case_list, value=value_list):
    """输出笛卡尔用例集合"""
    for i in itertools.product(item, value):
        print("输入".join(i).center(10, "*"))

def test_pprint():
    print("欢迎来到香格里拉")


if __name__ == '__main__':
    test_pprint()