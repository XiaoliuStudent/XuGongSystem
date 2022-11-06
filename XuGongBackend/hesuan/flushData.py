import gc
import json

# 定义清洗数据
import re


def flushData(res_context, doc_url=None, class_name="20计转本"):
    # 加载来自请求的数据
    global doc_title
    doc_data = json.loads(res_context)['clientVars']  # "clientVars": { "title": "在线-9月14日核酸检测名单", "collab_client_vars":

    # 做容错处理，涉及到了全员核酸表格和抽检核酸表格
    # doc_bodys = doc_data['collab_client_vars']['initialAttributedText']['text'][0][3][0]['c'][1] # {'0': {'0': 5, '2': [1, '9月14日核酸检测名单'], '3': 0}, '1': {'0': 1, '3': 1},
    doc_bodys = []
    doc_flush_list = [
        "doc_data['collab_client_vars']['initialAttributedText']['text'][0][4][0]['c'][1]",
        "doc_data['collab_client_vars']['initialAttributedText']['text'][0][3][0]['c'][1]",
        "doc_data['collab_client_vars']['initialAttributedText']['text'][0][2][0]['c'][1]",
        "doc_data['collab_client_vars']['initialAttributedText']['text'][0][5][0]['c'][1]"
    ]
    for i in doc_flush_list:
        try:
            doc_bodys = eval(i)
            doc_maxcol = int(doc_data['collab_client_vars']['maxCol'])
            doc_title = doc_data['title']
            break
        except:
            pass

    # 进行清洗数据 拿到班级的index，然后加上doc_maxcol，等于一系列的匹配
    banji_str = str(doc_bodys)[500:2000]
    banji_index = re.search("班级", banji_str).start()
    head_index = int(re.findall("\d*\d", banji_str[banji_index-28:banji_index-20])[0]) + doc_maxcol
    # 判断清洗
    student_list = []
    student = {}
    index = 0
    for i in doc_bodys:
            if int(i) < head_index:
                pass
            elif (int(i) - head_index) % doc_maxcol == 0:
                try:
                    student["class"] = doc_bodys[i]['2'][1]
                except:
                    break
                index += 1
            elif (int(i) - head_index - 1) % doc_maxcol == 0:
                student['name'] = doc_bodys[i]['2'][1]
                index += 1
            elif (int(i) - head_index - 3) % doc_maxcol == 0:
                student["xuehao"] = doc_bodys[i]['2'][1]
                index += 1
            elif (int(i) - head_index - 6) % doc_maxcol == 0:
                try:
                    if "是" == doc_bodys[i]['2'][1]:
                        student["status"] = "已完成"
                    elif "" == doc_bodys[i]['2'][1]:
                        student["status"] = "未完成"
                    else:
                        student["status"] = "填写有误"
                except:
                    student["status"] = "未完成"
                finally:
                    index += 1

            if index == 4:
                student['send'] = False
                student_list.append(student)
                student = {}
                index = 0
            else:
                pass

    end_student_list = []
    true_size = 0
    # 在所有班级中筛选出来需要而班级
    for i in student_list:
        if i['class'] == class_name:
            if i['status'] == "已完成":
                true_size += 1
            end_student_list.append(i)

    # 处理返回数据
    return_data = {
        'status': 200,
        'doc_title': doc_title,
        'doc_url': doc_url,
        'class_name': class_name,
        'count_size': {'true_size': true_size, 'false_size': len(end_student_list) - true_size},
        'students': end_student_list
    }

    return return_data


if __name__ == '__main__':
    flush_data = flushData(open("doc_res.json", "rb").read())
    print(flush_data)
