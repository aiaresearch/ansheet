import numpy as np
import math
from collections import defaultdict

input_num_number=10
input_id_number=8
layer_type=0
input_data={'words_result': [{'chars': [{'char': '0', 'location': {'top': 75, 'left': 106, 'width': 21, 'height': 39}}], 'words': '0', 'location': {'top': 71, 'left': 59, 'width': 115, 'height': 46}}, {'chars': [{'char': '0', 'location': {'top': 67, 'left': 441, 'width': 26, 'height': 51}}, {'char': '0', 'location': {'top': 67, 'left': 616, 'width': 26, 'height': 51}}, {'char': '0', 'location': {'top': 67, 'left': 784, 'width': 26, 'height': 51}}, {'char': '0', 'location': {'top': 67, 'left': 951, 'width': 26, 'height': 51}}, {'char': '0', 'location': {'top': 67, 'left': 1119, 'width': 26, 'height': 51}}], 'words': '00000', 'location': {'top': 67, 'left': 396, 'width': 797, 'height': 51}}, {'chars': [{'char': '0', 'location': {'top': 70, 'left': 1463, 'width': 20, 'height': 38}}], 'words': '0', 'location': {'top': 67, 'left': 1417, 'width': 114, 'height': 44}}, {'chars': [{'char': '1', 'location': {'top': 153, 'left': 102, 'width': 27, 'height': 51}}, {'char': '1', 'location': {'top': 152, 'left': 279, 'width': 27, 'height': 51}}, {'char': '1', 'location': {'top': 151, 'left': 449, 'width': 27, 'height': 50}}, {'char': '1', 'location': {'top': 149, 'left': 618, 'width': 27, 'height': 51}}, {'char': '1', 'location': {'top': 148, 'left': 788, 'width': 27, 'height': 51}}], 'words': '11111', 'location': {'top': 148, 'left': 57, 'width': 797, 'height': 56}}, {'chars': [{'char': '1', 'location': {'top': 149, 'left': 1124, 'width': 25, 'height': 46}}, {'char': '1', 'location': {'top': 149, 'left': 1294, 'width': 25, 'height': 46}}, {'char': '1', 'location': {'top': 149, 'left': 1465, 'width': 24, 'height': 46}}], 'words': '111', 'location': {'top': 149, 'left': 1078, 'width': 455, 'height': 46}}, {'chars': [{'char': '2', 'location': {'top': 232, 'left': 275, 'width': 29, 'height': 57}}], 'words': '2', 'location': {'top': 232, 'left': 59, 'width': 288, 'height': 57}}, {'chars': [{'char': '2', 'location': {'top': 237, 'left': 617, 'width': 21, 'height': 39}}, {'char': '1', 'location': {'top': 237, 'left': 655, 'width': 21, 'height': 39}}], 'words': '21', 'location': {'top': 233, 'left': 570, 'width': 114, 'height': 46}}, {'chars': [{'char': '2', 'location': {'top': 230, 'left': 956, 'width': 25, 'height': 47}}, {'char': '2', 'location': {'top': 230, 'left': 1124, 'width': 25, 'height': 47}}, {'char': '1', 'location': {'top': 230, 'left': 1214, 'width': 25, 'height': 47}}, {'char': '2', 'location': {'top': 230, 'left': 1290, 'width': 25, 'height': 47}}, {'char': '2', 'location': {'top': 230, 'left': 1465, 'width': 25, 'height': 47}}], 'words': '22122', 'location': {'top': 230, 'left': 907, 'width': 626, 'height': 47}}, {'chars': [{'char': '3', 'location': {'top': 317, 'left': 107, 'width': 25, 'height': 47}}, {'char': '3', 'location': {'top': 317, 'left': 275, 'width': 25, 'height': 47}}, {'char': '3', 'location': {'top': 317, 'left': 449, 'width': 25, 'height': 47}}], 'words': '333', 'location': {'top': 317, 'left': 58, 'width': 458, 'height': 47}}, {'chars': [{'char': '3', 'location': {'top': 312, 'left': 789, 'width': 25, 'height': 49}}, {'char': '3', 'location': {'top': 312, 'left': 952, 'width': 25, 'height': 49}}, {'char': '3', 'location': {'top': 312, 'left': 1124, 'width': 25, 'height': 49}}, {'char': '3', 'location': {'top': 312, 'left': 1294, 'width': 26, 'height': 49}}, {'char': '3', 'location': {'top': 312, 'left': 1466, 'width': 25, 'height': 49}}], 'words': '33333', 'location': {'top': 312, 'left': 740, 'width': 794, 'height': 50}}, {'chars': [{'char': '4', 'location': {'top': 388, 'left': 108, 'width': 30, 'height': 58}}, {'char': '4', 'location': {'top': 388, 'left': 276, 'width': 30, 'height': 58}}, {'char': '4', 'location': {'top': 388, 'left': 447, 'width': 30, 'height': 58}}, {'char': '4', 'location': {'top': 388, 'left': 621, 'width': 31, 'height': 58}}, {'char': '4', 'location': {'top': 388, 'left': 789, 'width': 31, 'height': 58}}, {'char': '4', 'location': {'top': 388, 'left': 957, 'width': 31, 'height': 58}}], 'words': '444444', 'location': {'top': 388, 'left': 59, 'width': 1072, 'height': 58}}, {'chars': [{'char': '4', 'location': {'top': 395, 'left': 1294, 'width': 25, 'height': 46}}, {'char': '4', 'location': {'top': 395, 'left': 1464, 'width': 25, 'height': 46}}], 'words': '44', 'location': {'top': 395, 'left': 1248, 'width': 285, 'height': 46}}, {'chars': [{'char': '5', 'location': {'top': 475, 'left': 107, 'width': 28, 'height': 55}}, {'char': '5', 'location': {'top': 475, 'left': 275, 'width': 28, 'height': 55}}, {'char': '5', 'location': {'top': 475, 'left': 448, 'width': 28, 'height': 55}}, {'char': '5', 'location': {'top': 475, 'left': 614, 'width': 29, 'height': 55}}, {'char': '5', 'location': {'top': 475, 'left': 789, 'width': 29, 'height': 55}}, {'char': '5', 'location': {'top': 475, 'left': 956, 'width': 28, 'height': 55}}, {'char': '5', 'location': {'top': 475, 'left': 1121, 'width': 29, 'height': 55}}, {'char': '5', 'location': {'top': 475, 'left': 1297, 'width': 28, 'height': 55}}, {'char': '5', 'location': {'top': 475, 'left': 1463, 'width': 29, 'height': 55}}], 'words': '555555555', 'location': {'top': 475, 'left': 60, 'width': 1476, 'height': 55}}, {'chars': [{'char': '6', 'location': {'top': 560, 'left': 105, 'width': 27, 'height': 52}}, {'char': '6', 'location': {'top': 560, 'left': 277, 'width': 26, 'height': 52}}, {'char': '6', 'location': {'top': 560, 'left': 448, 'width': 27, 'height': 52}}, {'char': '6', 'location': {'top': 560, 'left': 620, 'width': 27, 'height': 52}}, {'char': '6', 'location': {'top': 560, 'left': 783, 'width': 27, 'height': 52}}, {'char': '6', 'location': {'top': 560, 'left': 954, 'width': 27, 'height': 52}}, {'char': '6', 'location': {'top': 560, 'left': 1126, 'width': 27, 'height': 52}}, {'char': '6', 'location': {'top': 560, 'left': 1298, 'width': 26, 'height': 52}}, {'char': '6', 'location': {'top': 560, 'left': 1469, 'width': 27, 'height': 52}}], 'words': '666666666', 'location': {'top': 560, 'left': 61, 'width': 1477, 'height': 52}}, {'chars': [{'char': '7', 'location': {'top': 640, 'left': 107, 'width': 28, 'height': 54}}, {'char': '7', 'location': {'top': 640, 'left': 278, 'width': 27, 'height': 54}}, {'char': '7', 'location': {'top': 640, 'left': 448, 'width': 28, 'height': 54}}, {'char': '7', 'location': {'top': 640, 'left': 620, 'width': 28, 'height': 54}}, {'char': '7', 'location': {'top': 640, 'left': 791, 'width': 28, 'height': 54}}, {'char': '7', 'location': {'top': 640, 'left': 954, 'width': 28, 'height': 54}}, {'char': '7', 'location': {'top': 640, 'left': 1125, 'width': 28, 'height': 54}}, {'char': '7', 'location': {'top': 640, 'left': 1296, 'width': 28, 'height': 54}}, {'char': '7', 'location': {'top': 640, 'left': 1467, 'width': 28, 'height': 54}}], 'words': '777777777', 'location': {'top': 640, 'left': 61, 'width': 1479, 'height': 54}}, {'chars': [{'char': '8', 'location': {'top': 724, 'left': 105, 'width': 27, 'height': 52}}, {'char': '8', 'location': {'top': 724, 'left': 277, 'width': 26, 'height': 52}}, {'char': '8', 'location': {'top': 724, 'left': 448, 'width': 27, 'height': 52}}, {'char': '8', 'location': {'top': 724, 'left': 620, 'width': 27, 'height': 52}}, {'char': '8', 'location': {'top': 724, 'left': 791, 'width': 27, 'height': 52}}, {'char': '3', 'location': {'top': 724, 'left': 832, 'width': 27, 'height': 52}}, {'char': '8', 'location': {'top': 724, 'left': 954, 'width': 27, 'height': 52}}, {'char': '8', 'location': {'top': 724, 'left': 1126, 'width': 27, 'height': 52}}, {'char': '3', 'location': {'top': 724, 'left': 1167, 'width': 26, 'height': 52}}, {'char': '8', 'location': {'top': 724, 'left': 1297, 'width': 27, 'height': 52}}, {'char': '8', 'location': {'top': 724, 'left': 1469, 'width': 27, 'height': 52}}], 'words': '88888388388', 'location': {'top': 724, 'left': 61, 'width': 1480, 'height': 52}}, {'chars': [{'char': '9', 'location': {'top': 805, 'left': 108, 'width': 27, 'height': 53}}, {'char': '9', 'location': {'top': 805, 'left': 275, 'width': 27, 'height': 53}}, {'char': '9', 'location': {'top': 805, 'left': 451, 'width': 27, 'height': 53}}, {'char': '9', 'location': {'top': 805, 'left': 617, 'width': 28, 'height': 53}}, {'char': '9', 'location': {'top': 805, 'left': 785, 'width': 28, 'height': 53}}, {'char': '9', 'location': {'top': 805, 'left': 961, 'width': 27, 'height': 53}}, {'char': '9', 'location': {'top': 805, 'left': 1128, 'width': 27, 'height': 53}}, {'char': '9', 'location': {'top': 805, 'left': 1296, 'width': 27, 'height': 53}}, {'char': '9', 'location': {'top': 805, 'left': 1472, 'width': 27, 'height': 53}}], 'words': '999999999', 'location': {'top': 805, 'left': 62, 'width': 1479, 'height': 53}}], 'words_result_num': 17, 'log_id': 1903826137433507292}
def process_data(input_data,input_id_number):
    # 提取所有字符及其坐标信息
    input_num_number=10
    chars = []
    for word in input_data['words_result']:
        for char in word['chars']:
            loc = char['location']
            chars.append({
                'char': char['char'],
                'top': int(loc['top']-(loc['height'])/2),
                'left': int(loc['left']+(loc['width'])/2),
                'width': loc['width'],
                'height': loc['height']
            })
    # print('chars:',chars)

    # 计算中位数
    widths = [c['width'] for c in chars]
    heights = [c['height'] for c in chars]
    width_median = sorted(widths)[len(widths)//2]
    height_median = sorted(heights)[len(heights)//2]

    # 分组阈值
    top_threshold = 1.2*height_median 
    left_threshold = 1.2*height_median 
    # print(top_threshold,left_threshold,sep=' ')

    # 对top进行分组并替换为平均值
    sorted_tops = sorted({c['top'] for c in chars})
    top_groups = []
    current_group = [sorted_tops[0]]
    for t in sorted_tops[1:]:
        # print(current_group)
        # print(current_group[-1])
        if t - current_group[-1] <= top_threshold:
            current_group.append(t)
        else:
            top_groups.append(current_group)
            current_group = [t]
    top_groups.append(current_group)
    # print('top_groups:',top_groups)
    top_mapping = {t: int(sum(g)/len(g)) for g in top_groups for t in g}
    # print('top_mapping:',top_mapping)

    # 对left进行分组并替换为平均值
    sorted_lefts = sorted({c['left'] for c in chars})
    left_groups = []
    current_group = [sorted_lefts[0]]
    for l in sorted_lefts[1:]:
        if l - current_group[-1] <= left_threshold:
            current_group.append(l)
        else:
            left_groups.append(current_group)
            current_group = [l]
    left_groups.append(current_group)
    # print('left_groups:',left_groups)
    left_mapping = {l: min(g) for g in left_groups for l in g}

    # 应用坐标替换
    for c in chars:
        c['top'] = top_mapping[c['top']]
        c['left'] = left_mapping[c['left']]
        # if c['char']!=

    # 按调整后的坐标分组
    x_groups = defaultdict(list)
    for c in chars:
        x_groups[c['left']].append(c)
    #print('x_groups:',x_groups)

    # 按x坐标排序
    sorted_x = sorted(x_groups.keys())
    if len(sorted_x)!=input_id_number:
        sorted_x=sorted_x[:input_id_number]
    
    # 按调整后的坐标分组
    y_groups = defaultdict(list)
    for c in chars:
        y_groups[c['top']].append(c)
    #print('y_groups:',y_groups)

    # 按y坐标排序
    sorted_y = sorted(y_groups.keys())
    if len(sorted_y)!=input_num_number:
        sorted_y=sorted_y[:input_num_number]

    return sorted_x,sorted_y

    # # 处理每个y组的x坐标
    # final_rows = []
    # top_values = []
    # left_values = []

    # list_demo=list(map(lambda y:sorted(y_groups[y], key=lambda x: x['left']),sorted_y))
    # # print('list_demo:',list_demo)
    # # prevent incorrect recognition e.g. recognizing '[' as '1'

    # for i in range (input_num_number):

    #     correcting_list=sorted({n:l for n,l in enumerate(list(map(lambda x:x['char'],list_demo[i])))}.items(),key=lambda x:x[1])
    #     value=correcting_list[int(input_num_number/2)][1]
    #     re=0
    #     for item in correcting_list:
    #         if item[1] != value:
    #             list_demo[i].pop(int(item[0])-re)
    #             re+=1
    # #print('list_demo_correct:',list_demo)
    # final_list=[]
    # for i in range(input_id_number):
    #     checking_list=sorted({n:l for n,l in enumerate(list(map(lambda lists:lists[i]['left'],list_demo)))}.items(),key=lambda x:x[1])
    #     medium=checking_list[int(input_num_number/2)][1]
    #     print(medium)
    #     while checking_list[-1][1]!=medium or checking_list[-1][1]!=medium:
    #         if checking_list[-1][1] != medium:
    #             fault_idx=checking_list[-1][0]
    #             list_demo[fault_idx].insert(i,{'char':str(i),'left':int(medium)})

    #         elif checking_list[0][1] != medium:
    #             fault_idx=checking_list[0][0]
    #             list_demo[fault_idx].insert(i,{'char':str(i),'left':int(medium)})
    #         checking_list=sorted({n:l for n,l in enumerate(list(map(lambda lists:lists[i]['left'],list_demo)))}.items(),key=lambda x:x[1])
    #     final_list.append(checking_list)
    # print(final_list)

