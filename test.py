from BACK_TOOL.COMMON.verify.mbti import verify_format_mbti_name
from BACK_TOOL.COMMON.verify.name import verify_name

a = "학편라"
b = verify_format_mbti_name(a)
c = verify_name(a)

print(b)
print(c)