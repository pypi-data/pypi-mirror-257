# -*- coding: utf-8 -*-
#********************************************************************************
#Copyright © 2023 Wcq
#File Name: plotGui.py
#Author: Wcq
#Email: wcq-062821@163.com
#Created: 2023-11-23 19:18:29 
#Last Update: 2024-02-20 11:39:20
#         By: Wcq
#Description: 
#********************************************************************************

import os
import dearpygui.dearpygui as dpg
from time import sleep
import re
import json
import threading
from pathlib import Path

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def read_json_from_file (infile):
    with open(infile, 'r') as fpr:
        data = json.load(fpr)
        # logging.info(f'''data :  {data }''')
    return  data

def write_json_to_file (outfile, jsonData):
    with open(outfile, 'w', encoding='utf-8') as fpw:
        # ensure_ascii=False 确保可以写入中文  indent=4  格式化输出
        fpw.write(json.dumps(jsonData, ensure_ascii=False, indent=4, separators=(',', ':')))

my_window = None
def update_data (x_data1, y_data1):
    global my_window
    if my_window is not None:
        my_window.update_datas(x_data1, y_data1)
        return True
    else:
        return False

def run_window(label, xdata, ydata, freq):
    global my_window
    my_window = Window(label, xdata, ydata, freq)
    my_window.run_render()


class YON:
    ''' 弹出yes or no 窗口 '''
    def __init__(self):
        self.ycb = None
        self.ncb = None
        with dpg.window(label="warning", width=600, height=200, tag="modal_id", show=False):
            dpg.add_text(f"yes or no", color=[255,0,0],  tag='yes_or_no_test')
            dpg.add_separator()
            with dpg.group(horizontal=True):
                dpg.add_button(label="YES", width=75, callback=self.yes_callback)
                dpg.add_button(label="NO", width=75, callback=self.no_callback)
        
    def yes_callback(self):
        dpg.configure_item("modal_id", show=False)
        if self.ycb:
            self.ycb()

    def no_callback(self):
        dpg.configure_item("modal_id", show=False)
        if self.ncb:
            self.ncb()

    def yes_or_no(self, msg, ycb=None, ncb=None):
        '''
        ycb: 点击YES 时的回调函数
        ncb: 点击 NO 时的回调函数
        '''
        self.ycb = ycb
        self.ncb = ncb
        dpg.set_value('yes_or_no_test', msg)    
        dpg.configure_item("modal_id", show=True)

class Alert:
    ''' 弹出msg 窗口 '''
    def __init__(self, window_inst, main_width, main_height):
        width = 600
        height = 130
        pos_x = (main_width - width)//2
        pos_y = (main_height - height)//2
        self.window_inst = window_inst
        with dpg.window(label="warning", width=width, height=height, pos=(pos_x, pos_y), tag="tag_alert_id", show=False):
            dpg.add_text(f"demo", color=[255,0,0],  tag='tag_alert_msg')
            with dpg.table(header_row=False):
                dpg.add_table_column()
                dpg.add_table_column()
                dpg.add_table_column()
                with dpg.table_row():
                    dpg.add_text(default_value='')
                    dpg.add_button(label="确定", width=-1, callback=self.yes_callback)
                    dpg.add_text(default_value='')
        
    def yes_callback(self):
        dpg.configure_item("tag_alert_id", show=False)
        # self.window_inst.disable_all_components(True)

    def alert_msg(self, title, msg):
        '''
        title: 窗口标题
        msg: 显示的信息
        '''
        dpg.configure_item('tag_alert_id', label=title)
        dpg.configure_item('tag_alert_msg', default_value=msg)
        dpg.configure_item("tag_alert_id", show=True)
        # self.window_inst.disable_all_components(False)

class Window:
    '''
    xDataList : 时间轴
    dataDictList : 一个列表字典, e.g :  {"a [Nm/s]": [1, 2, 3, 4, 5], "b 3[Nm/s]":[2, 3, 4, 5, 6], "c a":[3, 4, 5, 6, 7]}
    字典的key 由名字 + ' ' + 单位, 组成
    freq => 更新的频率, 默认执行100 次run 才更新一次图表
    '''
    ratios = 1
    tab_id = 'my_tab_0'   # 默认打开第一个标签
    active_plots = f'main_plot_tag_0'
    tab_plot_dict = {}
    last_active_item = None
    window_width = 1400
    window_height = 900
    stop_sim = False
    exit_flag = False
    axis_timer = None
    unicode_file_name = 'unicode.txt'
    all_chinese_used_list = ''
    refresh_plot = True
    def __init__(self, label, xDataList, dataDictList, freq=100):
        self.x_data = xDataList
        # self.dictList = dataDictList.copy()
        self.dictList = dataDictList
        self.freq = freq

        self.auto_fix_x = True
        self.auto_fix_y = True

        self.group_dict_list = []
        self.group_list = []
        while (len(self.dictList) > 0):
            d = self.get_same_group_dict(self.dictList)
            if d:
                self.group_dict_list.append(d)
            else:
                break

        dpg.create_context()
        self.yon = YON()
        self.alert = Alert(self, self.window_width, self.window_height)
        dpg.create_viewport(title=label, width=self.window_width, height=self.window_height)
        with dpg.window(label=label, on_close=self.plot_close, height=200, width=200, tag="primary_window"):
            self.set_font()
            column = 2 
            num_group_in_picture = 4     # 一个 tab 可以显示几张图片
            # num_group_in_picture = 2     # 一个 tab 可以显示几张图片
            group_len = len(self.group_list)
            tabs = (group_len + (num_group_in_picture - 1)) // num_group_in_picture
            logging.debug(f'''tabs :  {tabs}''')
            dpg.add_checkbox(label='refresh_plot', default_value=self.refresh_plot, callback=self.refresh_plot_callback)
            with dpg.tab_bar(callback=self.tab_bar_callback, tag='tag_plot_tab_bar'):
                for t in range(tabs):
                    with dpg.tab(label=f"{t}", tag=f'my_tab_{t}'):
                        tab_name = self.layout_main_plot(t, self.group_dict_list, self.group_list[t*num_group_in_picture:(t+1)*num_group_in_picture], column)
                        dpg.set_item_label(f'my_tab_{t}', tab_name[:-1])
                        self.tab_plot_dict[tab_name[:-1]] = t
            
            self.set_key_handler()
                        
        dpg.set_primary_window("primary_window", True)

    def refresh_plot_callback (self, sender, app_data, user_data):
        ''''''
        self.refresh_plot = app_data
        
    def tab_bar_callback (self, sender, app_data, user_data):
        label = dpg.get_item_label(app_data)
        self.tab_id = app_data
        self.active_plots = f'main_plot_tag_{self.tab_plot_dict[label]}'

    def get_all_subplots(self, parent_id):
        subplots = []
        children = dpg.get_item_children(parent_id, slot=1)  # slot=1 表示我们关注的是内容，而不是标题栏或菜单等
        for child_id in children:
            if dpg.get_item_info(child_id)["type"] == "mvAppItemType::mvPlot":
                subplots.append(child_id)
        return subplots

    def find_axis_ids (self, plot_id):
        # 获取plot的所有子项
        axis_id = []
        children = dpg.get_item_children(plot_id, slot=1)
        for child_id in children:
            if dpg.get_item_info(child_id)["type"] == 'mvAppItemType::mvPlotAxis':
                axis_id.append(child_id)
        return axis_id

    def remove_all_axis_limits (self):
        '''移除所有x 轴的限制, 避免鼠标无法拖动图像'''
        subp = self.get_all_subplots(self.active_plots)
        axi_label = dpg.get_item_label(subp[0])
        axis_ids = self.find_axis_ids(subp[0])
        x_axis_id = axis_ids[0]
        y_axis_id = axis_ids[1]
        dpg.set_axis_limits_auto(x_axis_id)

    def _event_handler(self, sender, data):
        type=dpg.get_item_info(sender)["type"]
        if type=="mvAppItemType::mvKeyReleaseHandler":
            label = dpg.get_item_label(sender)
            logging.debug(f'label : {label} release')
            if self.last_active_item == "plot":
                if label in ['up', 'down', 'left', 'right', 'space', 'A']:
                    subp = self.get_all_subplots(self.active_plots)
                    axi_label = dpg.get_item_label(subp[0])
                    axis_ids = self.find_axis_ids(subp[0])
                    x_axis_id = axis_ids[0]
                    y_axis_id = axis_ids[1]
                    [x_min, x_max] = dpg.get_axis_limits(x_axis_id)

                if self.axis_timer and self.axis_timer.is_alive():
                    self.axis_timer.cancel()
                self.axis_timer = threading.Timer(1, self.remove_all_axis_limits)
                self.axis_timer.start()

                if label == 'A':
                    # 移除所有x 轴的限制, 否则鼠标无法拖动图像
                    dpg.set_axis_limits_auto(x_axis_id)
                elif label == 'up':
                    # 图像放大2 倍, 缩小 x 轴范围  
                    quarter_window_len = (x_max - x_min) / 4
                    new_x_min = x_min + quarter_window_len
                    new_x_max = x_max - quarter_window_len
                    dpg.set_axis_limits(x_axis_id, new_x_min, new_x_max)

                elif label == 'down':
                    # 图像缩小2 倍, 放大 x 轴范围 
                    half_window_len = (x_max - x_min) / 2
                    new_x_min = x_min - half_window_len
                    new_x_max = x_max + half_window_len
                    dpg.set_axis_limits(x_axis_id, new_x_min, new_x_max)

                elif label == 'left':
                    # 图像左移
                    move_windows_len = (x_max - x_min) / 4
                    new_x_min = x_min + move_windows_len
                    new_x_max = x_max + move_windows_len
                    dpg.set_axis_limits(x_axis_id, new_x_min, new_x_max)
                elif label == 'right':
                    # 图像右移
                    move_windows_len = (x_max - x_min) / 4
                    new_x_min = x_min - move_windows_len
                    new_x_max = x_max - move_windows_len
                    dpg.set_axis_limits(x_axis_id, new_x_min, new_x_max)
                elif label == 'space':
                    # 空格键全屏
                    for k, v in self.dictList.items():
                        k = re.sub(r'\s+', ' ', k)
                        name_uint = k.strip().split(' ')
                        group_name = name_uint[2]
                        if len(v) > 1:
                            dpg.fit_axis_data(f'tag_x_axis_{group_name}')
                            dpg.fit_axis_data(f'tag_y_axis_{group_name}')
        elif type=="mvAppItemType::mvMouseMoveHandler":
            logging.debug(f"Mouse pos: {data}")
            if data[0] >= 0 and data[0] <= self.window_width and data[1] >= 0 and data[1] <= self.window_height:
                # 鼠标在界面中
                tab_y_pos = dpg.get_item_pos('my_tab_0')[1]
                if data[1] > tab_y_pos:
                    self.last_active_item = "plot"
                else:
                    self.last_active_item = None
            else:
                self.last_active_item = None


    def set_key_handler (self):
        ''''''
        with dpg.handler_registry(show=True, tag="plot_keyboard_handler"):
            ka_release = dpg.add_key_release_handler(label='A', key=dpg.mvKey_A)
            kup_release = dpg.add_key_release_handler(label='up', key=dpg.mvKey_Up)
            kdown_release = dpg.add_key_release_handler(label='down', key=dpg.mvKey_Down)
            kleft_release = dpg.add_key_release_handler(label='left', key=dpg.mvKey_Left)
            kright_release = dpg.add_key_release_handler(label='right', key=dpg.mvKey_Right)
            kspace_release = dpg.add_key_release_handler(label='space', key=dpg.mvKey_Spacebar)
            m_move = dpg.add_mouse_move_handler()

        for handler in dpg.get_item_children("plot_keyboard_handler", 1):
            dpg.set_item_callback(handler, self._event_handler)

    def stop_sim_callback (self):
        ''''''
        self.stop_sim = True

    def _help(self, message, id=None):
        ''' 延时0.5 秒再提示, 当控件处于激活状态时, 不显示提示 '''
        if id is None:
            id = dpg.last_item()
        with dpg.tooltip(id, delay=0.5, hide_on_activity=True):
            dpg.add_text(message, color=[0, 255, 0])

    def set_font (self):
        ''' 设置全局字体 支持显示中文和特殊符号 '''
        font_path = str(Path(__file__).resolve().with_name("sarasa-mono-sc-regular.ttf"))
        # font_path = "/home/wcq/.local/share/fonts/sarasa-mono-sc-regular.ttf"
        # font_path = "/home/user/.local/share/fonts/sarasa-mono-sc-regular.ttf"
        current_file_path = str(Path(__file__))
        unicode_file = str(Path(__file__).resolve().with_name(self.unicode_file_name))
        if self.all_chinese_used_list == '':
            # 打包前每次运行都会更新 unicode.txt 打包后只读unicode.txt
            if os.path.exists(current_file_path):
                self.all_chinese_used_list = self.extract_chinese_text(current_file_path)
                with open(unicode_file,'w' ,  encoding='utf-8') as fpw:
                    fpw.write(self.all_chinese_used_list)
            with open(unicode_file, 'r',  encoding='utf-8') as fpr:
                self.all_chinese_used_list = fpr.read()
        self.all_chinese_used_list += "，。："
        with dpg.font_registry():
            with dpg.font(font_path, 20) as self.default_font:  # 增加中文编码范围，防止问号
                self.add_custom_chinese_unicode(self.all_chinese_used_list)
                dpg.add_font_range_hint(dpg.mvFontRangeHint_Chinese_Simplified_Common)
                # dpg.add_font_range_hint(dpg.mvFontRangeHint_Chinese_Full)   # 这个会影响启动速度
                dpg.bind_font(self.default_font)

    def set_all_chinese_font (self):
        font_path = str(Path(__file__).resolve().with_name("sarasa-mono-sc-regular.ttf"))
        with dpg.font_registry():
            with dpg.font(font_path, 20) as default_font:  # 增加中文编码范围，防止问号
                dpg.add_font_range_hint(dpg.mvFontRangeHint_Default)
                # dpg.add_font_range_hint(dpg.mvFontRangeHint_Chinese_Simplified_Common)
                dpg.add_font_range_hint(dpg.mvFontRangeHint_Chinese_Full)   # 这个会影响启动速度
                dpg.add_font_range(0x1, 0x400)
                dpg.bind_font(default_font)
                # dpg.bind_item_font(b2, second_font)

    def extract_chinese_text(self, file_path):
        ''' 从文件中提取出中文和部分特殊字符 '''
        logging.info(f'''file_path : {file_path}''')
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        # chinese_text = re.findall('[\u4e00-\u9fa5]+', content)   # chinese unicode
        # chinese_text += re.findall('[\u0300-\u0400]+', content)  # special symbol
        chinese_text = re.findall('[\u0300-\uffff]+', content)     # all
        chinese_list = set()
        for string in chinese_text:
            for c in string:
                chinese_list.add(c)
        chinese_list = list(chinese_list)
        chinese_string = ''.join(chinese_list)
        return chinese_string

    def add_custom_chinese_unicode(self, s):
        '''
        由于加载所有中文Unicode 会很慢, 所以直接只加载需要的即可
        '''
        unicode_list = set()
        for c in s:
            unicode_list.add(ord(c))
        unicode_list = list(unicode_list)
        dpg.add_font_chars(unicode_list)

    def layout_main_plot (self, t, d, group_l, column=1, width=-1, height=-1):
        '''
        显示大图的区域
        d => 传入的字典
        group_l => 要显示的组列表
        return => 返回由组名组成的tab_name 用来设置 tab 的label
        '''
        row = (len(group_l) + column - 1) // column
        tab_name = ""
        plot_tag = f'main_plot_tag_{t}'
        with dpg.subplots(row, column, label=f'main_subplots_{t}', width=width, height=height, tag=plot_tag):
            dpg.add_plot_legend()
            for group in group_l:
                with dpg.plot(label=group):
                    dpg. add_plot_axis(dpg.mvXAxis,                        tag=f'tag_x_axis_{group}')
                    with dpg.plot_axis(dpg.mvYAxis, label=f'tag_y_axis_{group}', tag=f'tag_y_axis_{group}') as y_axis:
                        for item in self.group_dict_list:
                            for (group_name, group_datas) in item.items():
                                if group_name == group:
                                    tab_name += group_name + '-'
                                    for d in group_datas:
                                        for (k, v) in d.items():
                                            k = re.sub(r'\s+', ' ', k)
                                            name_uint = k.strip().split(' ')
                                            name = name_uint[0]
                                            uint = name_uint[1]
                                            group_name = name_uint[2]
                                            dpg.add_line_series(x=list(self.x_data), y=list(v), label=f'{name}', tag=f'tag_realtime_subplots_{name}')
                                    else:
                                        # 画完图再把纵轴改成单位, 横轴改成时间
                                        dpg.set_item_label(f'tag_y_axis_{group}', f'{uint}')
                                        dpg.set_item_label(f'tag_x_axis_{group}', 'time/s')

        dpg.configure_item(plot_tag, link_all_x=True)
        # dpg.configure_item(plot_tag, link_all_y=True)
        self._add_config_options(plot_tag, 7, 
                                    "no_align", "link_rows", "link_columns",
                                    "link_all_x", "link_all_y", "auto_fix_x", "auto_fix_y", before=plot_tag)
        return tab_name

    def _config(self, sender, keyword, user_data):

        widget_type = dpg.get_item_type(sender)
        items = user_data

        if widget_type == "mvAppItemType::mvRadioButton":
            value = True

        else:
            keyword = dpg.get_item_label(sender)
            value = dpg.get_value(sender)

        if keyword == 'auto_fix_x':
            self.auto_fix_x = value
        elif keyword == 'auto_fix_y':
            self.auto_fix_y = value
        else:
            if isinstance(user_data, list):
                for item in items:
                    dpg.configure_item(item, **{keyword: value})
            else:
                dpg.configure_item(items, **{keyword: value})

    def _add_config_options(self, item, columns, *names, **kwargs):

        if columns == 1:
            if 'before' in kwargs:
                for name in names:
                    dpg.add_checkbox(label=name, callback=self._config, user_data=item, before=kwargs['before'], default_value=dpg.get_item_configuration(item)[name])
            else:
                for name in names:
                    dpg.add_checkbox(label=name, callback=self._config, user_data=item, default_value=dpg.get_item_configuration(item)[name])

        else:
            if 'before' in kwargs:
                dpg.push_container_stack(dpg.add_table(header_row=False, before=kwargs['before']))
            else:
                dpg.push_container_stack(dpg.add_table(header_row=False))

            for i in range(columns):
                dpg.add_table_column()
            for i in range((len(names) + (columns - 1))//columns):
                with dpg.table_row():
                    for j in range(columns):
                        try:
                            default_value = dpg.get_item_configuration(item)[names[i*columns + j]]
                        except:
                            default_value = True
                        if (i*columns + j) >= len(names): 
                            break
                        dpg.add_checkbox(label=names[i*columns + j], 
                                            callback=self._config, user_data=item, 
                                            default_value=default_value)
            dpg.pop_container_stack()
    

    def get_same_group_dict (self, d):
        data = {}
        obj_group = None
        for i, (k, v) in enumerate(d.items()):
            k = re.sub(r'\s+', ' ', k)
            name_uint = k.strip().split(' ')
            name = name_uint[0]
            uint = name_uint[1]
            group_name = name_uint[2]
            if group_name not in self.group_list:
                if obj_group:
                    # 当前正在处理一个组, 忽略该组
                    continue
                if len(v) > 1:
                    self.group_list.append(group_name)
                    obj_group = group_name
                    data[obj_group] = []
                    data[obj_group].append({k:v})
            elif group_name == obj_group:
                if len(v) > 1:
                    data[obj_group].append({k:v})
        if obj_group is None:
            return False
        else:
            return data

    def plot_close (self):
        ''' 点击关闭按键时调用 '''
        pass

    def update_datas (self, xDataList, dataDictList):
        self.x_data = xDataList
        self.dictList = dataDictList

    def update_plot (self, x_data=None, dictData=None):
        ''' 刷新所有plot ,包括没有显示的 '''
        if x_data is None:
            x_data = self.x_data
        if dictData is None:
            dictData = self.dictList
        for i, (k, v) in enumerate(dictData.items()):
            k = re.sub(r'\s+', ' ', k)
            name_uint = k.strip().split(' ')
            name = name_uint[0]
            group_name = name_uint[2]
            if len(v) > 1:
                dpg.set_value(f'tag_realtime_subplots_{name}', [list(x_data), list(v)]) # deque causes unexpected crash of program?
                if self.auto_fix_x:
                    dpg.fit_axis_data(f'tag_x_axis_{group_name}')
                if self.auto_fix_y:
                    dpg.fit_axis_data(f'tag_y_axis_{group_name}')

    def run_render (self):
        ''' 数据有变化并且达到时间条件并且允许刷新时才刷新 '''
        dpg.setup_dearpygui()
        dpg.show_viewport()
        # dpg.start_dearpygui()
        # dpg.destroy_context()
        # return

        cnt = 0
        # below replaces, start_dearpygui()
        logging.info('run_render')
        # print_process_and_thread_id()
        logging.info(f'''len(self.x_data) :  {len(self.x_data)}''')
        first_key = next(iter(self.dictList))
        first_value = self.dictList[first_key]
        dict_lens = len(first_value)
        logging.info(f'''len(y_data) :  {dict_lens}''')
        self.pre_refresh_len = 0
        while dpg.is_dearpygui_running():
            # insert here any code you would like to run in the render loop
            # you can manually stop by using stop_dearpygui()
            cnt += 1
            if self.refresh_plot and (cnt % self.freq == 0):
                logging.debug("this will run every frame %d"%cnt)
                if self.dictList:
                    first_key = next(iter(self.dictList))
                    first_value = self.dictList[first_key]
                    dict_lens = len(first_value)
                else:
                    dict_lens = 0
                x_len = len(self.x_data)
                if (x_len == dict_lens):
                    if self.pre_refresh_len != x_len:
                        self.update_plot(self.x_data, self.dictList)
                        self.pre_refresh_len = x_len
                        logging.info(f'self.pre_refresh_len : {self.pre_refresh_len}')
                else:
                    logging.info(f'''len(self.x_data) :  {x_len}''')
                    logging.info(f'''len(y_data) :  {dict_lens}''')
            
            dpg.render_dearpygui_frame()

            if self.exit_flag is True:
                logging.info('exit dearpygui')
                break
            sleep(0.2)
            # sleep(0.03)
        dpg.destroy_context()

if __name__ == '__main__':
    datas = read_json_from_file('data.hjson')
    # datas = read_json_from_file('data.hjson')
    dict_datas = {}
    for k, v in datas.items():
        dict_datas[f'{k}'] = []
        for item in v:
            dict_datas[f'{k}'].append(item)
            # if len(dict_datas[f'{k}']) > 5:
            #     break
    x = dict_datas.pop('time')
    # my_window = Window('demo', x, a)
    # x = [1, 2, 3, 4, 5, 6]
    my_window = Window('Demo', x, dict_datas, freq=1)
    my_window.run_render()
    
    

