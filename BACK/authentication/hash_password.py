from passlib.context import CryptContext

# bcrypt는 단방향 암호화 알고리즘이다. 여기선 아마 이 알고리즘을 사용하여 암호화한다고 선언하는듯
# 더 자세한건 https://fastapi.tiangolo.com/tutorial/security/first-steps/

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_hash(password: str):
    return password_context.hash(password)


def verify_hash(plain_password: str, hashed_password: str):
    return password_context.verify(plain_password, hashed_password)
