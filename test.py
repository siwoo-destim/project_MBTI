from BACK.models.mbti import MBTIRelationship
import re
import traceback

def interpreter(relationship_data: str, detail_data: str):
    pattern = r'{@ mbti @}\s*([\w, ]+)\s*{@ relationship @}\s*(.*?)\s*{@ endmbti @}'
    matches = re.finditer(pattern, relationship_data, re.DOTALL)



    pattern2 = r'{@ mbti @}\s*(.*?)\s*{@ detail @}\s*(.*?)\s*{@ endmbti @}'
    matches2 = re.finditer(pattern2, detail_data, re.DOTALL)

    parsed_detail_datas = {}
    for match2 in matches2:
        stakeholder = match2.group(1).strip()
        detail = match2.group(2).strip()
        parsed_detail_datas[stakeholder] = detail


    data = []
    for match in matches:
        stakeholders = [x.strip() for x in match.group(1).split(',')]
        print(stakeholders)
        relationship = (match.group(2).strip() +
                        '<hr>' +
                        parsed_detail_datas.get(stakeholders[0], f'{stakeholders[0]}detail 못 찾음') +
                        '<hr>' +
                        parsed_detail_datas.get(stakeholders[1], f'{stakeholders[1]}detail 못 찾음'))



        entry = MBTIRelationship(stakeholders=stakeholders, relationship=relationship)
        data.append(entry)

    return data



async def main():
    relationship_file_path = 'mbti_relationship.html'  # 파일 경로를 지정해주세요
    detail_file_path = 'details.html'
    try:
        with (open(relationship_file_path, 'r', encoding='utf-8') as file,
              open(detail_file_path, 'r', encoding='utf-8') as file2):

            relationship_data = file.read()
            detail_data = file2.read()
            data = interpreter(relationship_data, detail_data)
            print(data)
            await MBTIRelationship.delete_all()
            await MBTIRelationship.insert_many(data)


    except FileNotFoundError:
        print(f"파일이 {detail_file_path} 경로에 존재하지 않습니다.")
    except Exception as e:
        print(f"요류임: {e}")
        traceback_message = traceback.format_exc()
        print(traceback_message)

