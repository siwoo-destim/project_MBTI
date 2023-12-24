from BACK.models.mbti import MBTIRelationship
import re
import traceback

def interpreter(text: str):

    pattern = r'{@ mbti @}\s*([\w, ]+)\s*{@ relationship @}\s*(.*?)\s*{@ endmbti @}'
    matches = re.finditer(pattern, text, re.DOTALL)

    data = []
    for match in matches:
        stakeholders = [x.strip() for x in match.group(1).split(',')]
        relationship = match.group(2).strip()
        entry = MBTIRelationship(stakeholders=stakeholders, relationship=relationship)
        data.append(entry)

    return data



async def main():
    file_path = 'mbti_relationship.html'  # 파일 경로를 지정해주세요
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            data = interpreter(content)
            print(data)
            await MBTIRelationship.delete_all()
            await MBTIRelationship.insert_many(data)


    except FileNotFoundError:
        print(f"파일이 {file_path} 경로에 존재하지 않습니다.")
    except Exception as e:
        print(f"요류임: {e}")
        traceback_message = traceback.format_exc()
        print(traceback_message)
