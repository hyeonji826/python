# 변수
PI = 3.141592653589793

# 함수
def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

# 클래스
class Circle:
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return PI * self.radius * self.radius

# __name__은 모듈이 직접 실행될 때 "__main__"으로 설정됨.
# 다른 모듈에 의해 import 될 때는 모듈의 이름이 설정됨.
if __name__ == "__main__":
    print("이 모듈은 직접 실행되었습니다.")
else:
    print("이 모듈은 다른 모듈에 의해 import 되었습니다.")