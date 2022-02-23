"""
@FILE_NAME : 教务系统抢课_pytyut版
-*- coding : utf-8 -*-
@Author : Zhaokugua
@Time : 2022/2/23 20:15
"""
from pytyut import Pytyut
import os


# 验证是否选上课了
def check_class(user, pid, kxh, kch):
    res_json = user.get_chosen_course_list()
    for info in res_json['rows']:
        if info['Pid'] == pid:
            if info['Kch'] == kch:
                if info['Kxh'] == kxh:
                    return '验证选课成功！', info['Id']
                else:
                    return '诶呀，选错课了！', info['Id']
    return '没有找到对应的选课记录！', info['Id'] if res_json['rows'] else ''


if __name__ == '__main__':
    print('###### 教务系统选课v1.0.0  Based on Pytyut v0.7 beta######\n欢迎使用选课系统。建议连接校园网或校园网VPN后使用。')
    print('###### 登录部分 ######')
    Pytyut.node_link = Pytyut.auto_node_chose(debug=True)
    user_id = input('请输入学号：')
    pass_word = input('请输入密码：')
    user = Pytyut(user_id, pass_word)
    user.login(debug=True)
    print('###### 获取可选课的列表 ######')
    page_list = user.get_xq_page_list()
    print('获取到课程列表：')
    set_i = 0
    for item in page_list['rows']:
        set_i += 1
        print(set_i, '\t', item['Describe'], '\t', item['Begintime'], '\t', item['Endtime'], '\t', item['Id'])
    select_num = int(input('请输入要选的课的代号：'))
    class_id = page_list['rows'][select_num - 1]['Id']
    print('已选择：', page_list['rows'][select_num - 1]['Describe'], '\t', class_id)
    print('###### 获取选课的详细信息 ######')
    print('正在获取课程详情...')
    class_list = user.get_xk_kc_list(pid=class_id)
    for i in range(int(class_list['total'])):
        class_info = class_list['rows'][i]
        if class_info['Sfybm'] == '1':
            class_info['Sfybm'] = '【已选】'
        elif class_info['Sfybm'] == '0':
            class_info['Sfybm'] = '（未选）'

        # 判断两种选课条件
        if class_info.get('Xmsm'):
            print(i + 1, '\t',
                  class_info['Kxh'], class_info['Xmsm'], '\t',
                  class_info['Skjs'], '\t',
                  str(int(class_info['Ybrs']))+'/' + str(int(class_info['Bkskrl'])), '\t',
                  class_info['Sfybm']
                  )
        else:
            print(i + 1, '\t',
                  class_info['Kch'], '\t',
                  '学分：' + class_info['Xf'], '\t',
                  str(class_info['Ybrs']) + '/' + str(class_info['Bkskrl']), '\t',
                  class_info['Sfybm'], '\t', class_info['Kcm'].replace('\n', ''),
                  )
    choice_id = int(input('请输入要选的或者退的课的代号(0退出)：'))
    # 判断选项，并智能判断是选课还是退课
    if choice_id:
        choice_id = choice_id - 1
        # 这里写一段选择的函数
        class_json_info = {
            'xsxkList[0][Kch]': class_list['rows'][choice_id]['Kch'],
            'xsxkList[0][Kcm]': class_list['rows'][choice_id]['Kcm'],
            'xsxkList[0][Kxh]': class_list['rows'][choice_id]['Kxh'],
            'xsxkList[0][Pid]': class_id,
            'xsxkList[0][Bkskrl]': int(class_list['rows'][choice_id]['Bkskrl']),
            'xsxkList[0][Xf]': class_list['rows'][choice_id]['Xf'],
        }
        # 判断选没选
        if class_list['rows'][choice_id]['Sfybm'] == '（未选）':
            print('正在选课...')
            info1 = user.choose_course(class_json_info)
            print(info1['message'])
            # 判断两种选课条件
            if class_list['rows'][choice_id].get('Xmsm'):
                print('已选择：', class_list['rows'][choice_id]['Kxh'], class_list['rows'][choice_id]['Xmsm'], '\t',
                      class_list['rows'][choice_id]['Skjs'])
            else:
                print('已选择：', class_list['rows'][choice_id]['Kch'], class_list['rows'][choice_id]['Kcm'], '\t',
                      '学分：' + class_list['rows'][choice_id]['Xf'])
            # 验证结果
            print('正在验证选课是否成功...')
            print(check_class(user, class_id, class_list['rows'][choice_id]['Kxh'], class_list['rows'][choice_id]['Kch'])[0])
        elif class_list['rows'][choice_id]['Sfybm'] == '【已选】':
            choice = input('检测到已选择，是否退课？(1：是 0：退出)：')
            if choice == '1':
                big_id = check_class(user, class_id, class_list['rows'][choice_id]['Kxh'], class_list['rows'][choice_id]['Kch'])[1]
                info2 = user.remove_course(class_json_info, course_Id=big_id)
                print(info2['message'])
                print('')
            else:
                print('欢迎下次使用！')
                os.system('pause')
                exit(0)
    else:
        pass
    print('欢迎下次使用！')
    os.system('pause')


