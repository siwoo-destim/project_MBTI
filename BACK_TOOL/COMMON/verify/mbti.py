import re


def verify_format_name_weakly(mbti_name):
    p = re.compile('\w{1,16}')
    m = p.match(mbti_name)

    if m:
        if m.group() == mbti_name:
            return m.group()

    return False


def verify_format_mbti_mbti(mbti_mbti):
    p = re.compile('[IE][SN][TF][JP]')
    m = p.match(mbti_mbti)

    if m:
        if m.group() == mbti_mbti:
            return m.group()

    return False

