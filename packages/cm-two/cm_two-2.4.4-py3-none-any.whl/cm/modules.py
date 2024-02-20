﻿import tkinter.filedialog
import traceback

from cm.terminal import Terminal
from tkinter import *
from gtki_module_treeview.main import CurrentTreeview, NotificationTreeview, \
    HistroryTreeview
from cm.widgets.dropDownCalendar import MyDateEntry
from cm.widgets.drop_down_combobox import AutocompleteCombobox, AutocompleteComboboxCarNumber
import datetime
from cm.styles import color_solutions as cs
from cm.styles import fonts
from cm.styles import element_sizes as el_sizes
from gtki_module_exex.main import CreateExcelActs


class SysNot(Terminal):
    """ Окно уведомлений"""

    def __init__(self, root, settings, operator, can):
        Terminal.__init__(self, root, settings, operator, can)
        self.name = 'SysNot'
        self.buttons = settings.toolBarBtns
        self.tar = NotificationTreeview(self.root, operator, height=35)
        self.tar.createTree()
        self.tree = self.tar.get_tree()
        self.btn_name = self.settings.notifBtn

    def drawing(self):
        Terminal.drawing(self)
        self.drawWin('maincanv', 'sysNot')
        self.drawTree()
        self.buttons_creation(tagname='winBtn')

    def destroyBlockImg(self, mode='total'):
        Terminal.destroyBlockImg(self, mode)
        self.drawTree()

    def drawTree(self):
        # self.tar.fillTree(info)
        self.can.create_window(self.w / 1.9, self.h / 1.95, window=self.tree,
                               tag='tree')

    def openWin(self):
        Terminal.openWin(self)
        self.root.bind('<Escape>',
                       lambda event: self.operator.mainPage.openWin())

class Statistic(Terminal):
    """ Окно статистики """

    def __init__(self, root, settings, operator, can):
        Terminal.__init__(self, root, settings, operator, can)
        self.btns_height = self.h / 4.99
        self.records_amount = 0
        self.uncount_records = []
        self.name = 'Statistic'
        self.buttons = settings.statBtns
        # self.font = '"Montserrat SemiBold" 14'
        self.history = {}
        self.chosenType = ''
        self.chosenContragent = ''
        self.choosenCat = ''
        self.typePopup = ...
        self.carnums = []
        self.filterColNA = '#2F8989'
        self.filterColA = '#44C8C8'
        self.tree = self.create_tree()
        self.posOptionMenus()
        self.calendarsDrawn = False
        self.btn_name = self.settings.statisticBtn
        self.weight_sum = 0
        self.changed_record = None

    def create_tree(self):
        self.tar = HistroryTreeview(self.root, self.operator, height=28)
        self.tar.createTree()
        self.tree = self.tar.get_tree()
        self.tree.bind("<Double-Button-1>", self.OnDoubleClick)
        return self.tree

    def rebind_btns_after_orup_close(self):
        self.tree.bind("<Double-Button-1>", self.OnDoubleClick)


    def excel_creator(self):
        file_name = self.get_excel_file_path()
        data_list = self.generate_excel_content()
        self.form_excel(file_name, data_list)

    def generate_excel_content(self):
        items = self.tree.get_children()
        data_list = []
        for item in items:
            record_id = self.tree.item(item, 'text')
            data = self.tree.item(item, 'values')
            data = list(data)
            data.insert(0, record_id)
            data_list.append(data)
        return data_list

    def get_excel_file_path(self):
        name = tkinter.filedialog.asksaveasfilename(defaultextension='.xlsx',
                                                    filetypes=[("Excel files",
                                                                "*.xls *.xlsx")])
        return name

    def form_excel(self, file_name, data_list):
        inst = CreateExcelActs(file_name, data_list, self.amount_weight)
        inst.create_document()

    def OnDoubleClick(self, event):
        ''' Реакция на дабл-клик по заезду '''
        item = self.tree.selection()[0]
        self.chosenStr = self.tree.item(item, "values")
        self.record_id = self.tree.selection()[0]
        self.draw_change_records(self.chosenStr, item)

    def draw_change_records(self, string, record_id):
        self.parsed_string = self.parse_string(string)
        self.orupState = True
        btnsname = 'record_change_btns'
        record_info = self.history[int(record_id)]
        self.initBlockImg('record_change_win', btnsname=btnsname,
                          hide_widgets=self.statisticInteractiveWidgets)
        self.posEntrys(
            carnum=self.parsed_string["car_number"],
            trashtype=self.parsed_string["trash_type"],
            trashcat=self.parsed_string["trash_cat"],
            contragent=self.parsed_string["carrier"],
            client=self.parsed_string['client'],
            notes=self.parsed_string['notes'],
            polygon=self.operator.get_polygon_platform_repr(record_info['id']),
            object=self.operator.get_pol_object_repr(record_info['object_id']),
            spec_protocols=False,
            call_method='manual',
        )
        self.root.bind('<Return>', lambda event: self.change_record())
        self.root.bind('<Escape>',
                       lambda event: self.destroyORUP(mode="decline"))
        self.root.bind("<Double-Button-1>",
                       lambda event: self.clear_optionmenu(event))
        self.unbindArrows()

    def mark_changed_rec(self):
        if not self.changed_record:
            return
        try:
            self.tree.selection_set(self.changed_record)
            self.tree.see(self.changed_record)
        except:
            print(traceback.format_exc())
            pass

    def destroyORUP(self, mode=None):
        super().destroyORUP(mode)

    def parse_string(self, string):
        # Парсит выбранную строку из окна статистики и возвращает словарь с элементами
        parsed = {}
        parsed["car_number"] = string[0]
        parsed["carrier"] = string[2]
        parsed["trash_cat"] = string[6]
        parsed["trash_type"] = string[7]
        parsed["notes"] = string[10]
        parsed['client'] = string[1]
        return parsed

    def change_record(self):
        self.changed_record = self.tree.selection()
        info = self.get_orup_entry_reprs()
        self.try_upd_record(info['carnum'], info['carrier'], info['trash_cat'],
                            info['trash_type'], info['comm'],
                            info['polygon_platform'], info['client'],
                            info['polygon_object'])

    def try_upd_record(self, car_number, carrier, trash_cat, trash_type,
                       comment, polygon, client, pol_object):
        self.car_protocol = self.operator.fetch_car_protocol(car_number)
        data_dict = {}
        data_dict['car_number'] = car_number
        data_dict['chosen_trash_cat'] = trash_cat
        data_dict['type_name'] = trash_type
        data_dict['carrier_name'] = carrier
        data_dict['client_name'] = client
        data_dict['sqlshell'] = object
        data_dict['photo_object'] = self.settings.redbg[3]
        data_dict['client'] = client
        data_dict['comment'] = comment
        data_dict['platform_name'] = self.platform_choose_var.get()
        data_dict['object_name'] = self.objectOm.get()
        response = self.operator.orup_error_manager.check_orup_errors(
            orup='brutto',
            xpos=self.settings.redbg[1],
            ypos=self.settings.redbg[2],
            **data_dict)
        if not response:
            auto_id = self.operator.get_auto_id(car_number)
            carrier_id = self.operator.get_client_id(carrier)
            trash_cat_id = self.operator.get_trash_cat_id(trash_cat)
            trash_type_id = self.operator.get_trash_type_id(trash_type)
            polygon_id = self.operator.get_polygon_platform_id(polygon)
            client_id = self.operator.get_client_id(client)
            pol_object_id = self.operator.get_polygon_object_id(pol_object)
            self.operator.ar_qdk.change_opened_record(record_id=self.record_id,
                                                      auto_id=auto_id,
                                                      carrier=carrier_id,
                                                      trash_cat_id=trash_cat_id,
                                                      trash_type_id=trash_type_id,
                                                      comment=comment,
                                                      car_number=car_number,
                                                      polygon=polygon_id,
                                                      client=client_id,
                                                      pol_object=pol_object_id)
            self.destroyORUP()
            self.upd_statistic_tree()

    def upd_statistic_tree(self):
        """ Обновить таблицу статистики """
        self.get_history()
        self.draw_stat_tree()

    def draw_add_comm(self):
        btnsname = 'addCommBtns'
        self.add_comm_text = self.getText(h=5, w=42, bg=cs.orup_bg_color)
        self.initBlockImg(name='addComm', btnsname=btnsname,
                          seconds=('second'),
                          hide_widgets=self.statisticInteractiveWidgets)
        self.can.create_window(self.w / 2, self.h / 2.05,
                               window=self.add_comm_text, tag='blockimg')
        self.root.bind('<Return>', lambda event: self.add_comm())
        self.root.bind('<Escape>',
                       lambda event: self.destroyBlockImg(mode="total"))

    def add_comm(self):
        comment = self.add_comm_text.get("1.0", 'end-1c')
        self.operator.ar_qdk.add_comment(record_id=self.record_id,
                                         comment=comment)
        self.destroyBlockImg()
        self.upd_statistic_tree()

    def posOptionMenus(self):
        self.placeTypeOm()
        self.placeCatOm(bg=self.filterColNA)
        self.placeContragentCombo()
        self.placePoligonOm()
        self.placeObjectOm()
        self.placeCarnumCombo()
        self.placeClientsOm()

        self.statisticInteractiveWidgets = [self.stat_page_polygon_combobox,
                                            self.trashTypeOm, self.trashCatOm,
                                            self.carriers_stat_om,
                                            self.stat_page_carnum_cb,
                                            self.clientsOm,
                                            self.stat_page_pol_object_combobox]
        self.hide_widgets(self.statisticInteractiveWidgets)

    def abortFiltres(self):
        """ Сбросить все фильтры на значения по умолчанию
        """
        for combobox in self.statisticInteractiveWidgets:
            if isinstance(combobox, AutocompleteCombobox):
                combobox.set_default_value()
        self.startCal.set_date(datetime.datetime.today())
        self.endCal.set_date(datetime.datetime.today())
        self.upd_statistic_tree()
        self.changed_record = None

    def placePoligonOm(self):
        listname = ['площадка'] + self.operator.get_polygon_platforms_reprs()
        self.poligonVar = StringVar()
        self.stat_page_polygon_combobox = AutocompleteCombobox(self.root,
                                                               textvariable=self.poligonVar,
                                                               default_value=
                                                               listname[0])
        self.configure_combobox(self.stat_page_polygon_combobox)
        self.stat_page_polygon_combobox.set_completion_list(listname)
        self.stat_page_polygon_combobox.config(width=8, height=30,
                                               font=fonts.statistic_filtres)
        self.can.create_window(self.w / 2.475 - 100, self.btns_height,
                               window=self.stat_page_polygon_combobox,
                               tags=('filter', 'typeCombobox'))

    def placeObjectOm(self):
        listname = ['объект'] + self.operator.get_pol_objects_reprs()
        self.pol_object_var = StringVar()
        self.stat_page_pol_object_combobox = AutocompleteCombobox(self.root,
                                                                  textvariable=self.pol_object_var,
                                                                  default_value=
                                                                  listname[0])
        self.configure_combobox(self.stat_page_pol_object_combobox)
        self.stat_page_pol_object_combobox.set_completion_list(listname)
        self.stat_page_pol_object_combobox.config(width=16, height=36,
                                                  font=fonts.statistic_filtres)
        self.can.create_window(self.w / 1.91 - 30, self.h / 3.85,
                               window=self.stat_page_pol_object_combobox,
                               tags=('filter', 'typeCombobox'))

    def placeTypeOm(self):
        listname = ['вид груза'] + self.operator.get_trash_types_reprs()
        self.stat_page_trash_type_var = StringVar()
        self.trashTypeOm = AutocompleteCombobox(self.root,
                                                textvariable=self.stat_page_trash_type_var,
                                                default_value=listname[0])
        self.configure_combobox(self.trashTypeOm)
        self.trashTypeOm.set_completion_list(listname)
        self.trashTypeOm.config(width=9, height=30,
                                font=fonts.statistic_filtres)
        self.can.create_window(self.w / 3.435 - 40, self.btns_height,
                               window=self.trashTypeOm,
                               tags=('filter', 'typeCombobox'))

    def placeCatOm(self, bg, deffvalue='кат. груза'):
        listname = ['кат. груза'] + self.operator.get_trash_cats_reprs()
        self.stat_page_trash_cat_var = StringVar()
        self.trashCatOm = AutocompleteCombobox(self.root,
                                               textvariable=self.stat_page_trash_cat_var,
                                               default_value=listname[0])
        self.trashCatOm.set_completion_list(listname)
        self.trashCatOm.config(width=9, height=30,
                               font=fonts.statistic_filtres)
        self.can.create_window(self.w / 5.45, self.btns_height,
                               window=self.trashCatOm,
                               tags=('filter', 'catOm'))
        self.configure_combobox(self.trashCatOm)

    def placeClientsOm(self):
        #listname = ['клиенты'] + self.operator.get_clients_reprs()
        self.stat_page_clients_var = StringVar()
        self.clientsOm = AutocompleteCombobox(self.root,
                                              textvariable=self.stat_page_clients_var,
                                              default_value='Клиенты')
        self.configure_combobox(self.clientsOm)
        self.full_clients()
        self.clientsOm['style'] = 'orup.TCombobox'
        #self.clientsOm.set_completion_list(listname)
        self.clientsOm.config(width=23, height=int(self.h / 40),
                              font=fonts.statistic_filtres)
        self.can.create_window(self.w / 1.278 - 60, self.btns_height,
                               window=self.clientsOm,
                               tags=('filter', 'typeCombobox'))
    def full_clients(self):
        self.clientsOm.set_completion_list(self.operator.get_clients_reprs())

    def full_carriers(self):
        self.carriers_stat_om.set_completion_list(self.operator.get_clients_reprs())

    def placeContragentCombo(self):
        #carriers = ['перевозчики'] + self.operator.get_clients_reprs()
        self.stat_page_carrier_var = StringVar()
        self.carriers_stat_om = AutocompleteCombobox(self.root,
                                                    textvariable=self.stat_page_carrier_var,
                                                    default_value='Перевозчики')
        self.configure_combobox(self.carriers_stat_om)
        self.full_carriers()
        self.carriers_stat_om.config(width=25, height=int(self.h / 40),
                                    font=fonts.statistic_filtres)
        self.can.create_window(self.w / 1.91 - 70, self.btns_height,
                               window=self.carriers_stat_om,
                               tags=('filter', 'stat_page_carrier_var'))

    def placeCarnumCombo(self):
        listname = ['гос.номер'] + self.operator.get_auto_reprs()
        self.stat_page_carnum_cb = AutocompleteComboboxCarNumber(self.root,
                                                        default_value=listname[
                                                            0])
        self.stat_page_carnum_cb.set_completion_list(listname)
        self.configure_combobox(self.stat_page_carnum_cb)
        self.stat_page_carnum_cb.config(width=11, height=20,
                                        font=fonts.statistic_filtres)
        self.can.create_window(self.w / 1.53 - 50, self.btns_height,
                               window=self.stat_page_carnum_cb,
                               tags=('stat_page_carnum_cb', 'filter'))

    def place_amount_info(self, weight, amount, tag='amount_weight'):
        """ Разместить итоговую информацию (количество взвешиваний (amount), тоннаж (weigh) )"""
        if self.operator.current == 'Statistic' and self.blockImgDrawn == False:
            self.can.delete(tag)
            weight = self.formatWeight(weight)
            self.amount_weight = 'ИТОГО: {} ({} взвешиваний)'.format(weight,
                                                                     amount)
            self.can.create_text(self.w / 2, self.h / 1.113,
                                 text=self.amount_weight,
                                 font=fonts.general_text_font, tags=(tag, 'statusel'),
                                 fill=self.textcolor, anchor='s',
                                 justify='center')

    def place_uncount_records(self, uncount_records,):
        self.can.delete('amount_weight')
        uncount_records.sort()
        if uncount_records:
            amount_weight_nc = f'\nНекоторые акты {tuple(uncount_records)} ' \
                               f'были отменены.\n'
            self.can.create_text(self.w / 2, self.h / 1.062,
                                 text=amount_weight_nc,
                                 font=self.font, tags=('amount_weight', 'statusel'),
                                 fill=self.textcolor, anchor='s',
                                 justify='center')

    def formatWeight(self, weight):
        weight = str(weight)
        if len(weight) < 4:
            ed = 'кг'
        else:
            weight = int(weight) / 1000
            ed = 'тонн'
        return f"{weight} {ed}"

    def placeText(self, text, xpos, ypos, tag='maincanv', color='black',
                  font='deff', anchor='center'):
        if font == 'deff': font = self.font
        xpos = int(xpos)
        ypos = int(ypos)
        self.can.create_text(xpos, ypos, text=text, font=self.font, tag=tag,
                             fill=color, anchor=anchor)

    def placeCalendars(self):
        self.startCal = MyDateEntry(self.root, date_pattern='dd/mm/yy')
        self.startCal.config(width=7, font=fonts.statistic_calendars)
        self.endCal = MyDateEntry(self.root, date_pattern='dd/mm/yy')
        self.endCal.config(width=7, font=fonts.statistic_calendars)
        # self.startCal['style'] = 'stat.TCombobox'
        # self.endCal['style'] = 'stat.TCombobox'
        self.startCal['style'] = 'orup.TCombobox'
        self.endCal['style'] = 'orup.TCombobox'

        self.can.create_window(self.w / 3.86, self.h / 3.85,
                               window=self.startCal,
                               tags=('statCal'))
        self.can.create_window(self.w / 2.75, self.h / 3.85,
                               window=self.endCal,
                               tags=('statCal'))
        self.statisticInteractiveWidgets.append(self.startCal)
        self.statisticInteractiveWidgets.append(self.endCal)
        self.calendarsDrawn = True

    def drawing(self):
        Terminal.drawing(self)
        self.drawWin('maincanv', 'statisticwin')
        self.hiden_widgets += self.buttons_creation(tagname='winBtn')
        if not self.calendarsDrawn:
            self.placeCalendars()
        self.get_history()
        self.draw_stat_tree()
        self.show_widgets(self.statisticInteractiveWidgets)

    def get_history(self):
        """ Запрашивает истоию заездов у GCore """
        trash_cat = self.operator.get_trash_cat_id(
            self.stat_page_trash_cat_var.get())
        trash_type = self.operator.get_trash_type_id(
            self.stat_page_trash_type_var.get())
        carrier = self.operator.get_client_id(self.stat_page_carrier_var.get())
        auto = self.operator.get_auto_id(self.stat_page_carnum_cb.get())
        platform_id = self.operator.get_polygon_platform_id(
            self.stat_page_polygon_combobox.get())
        pol_object_id = self.operator.get_polygon_object_id(
            self.stat_page_pol_object_combobox.get())
        client = self.operator.get_client_id(self.stat_page_clients_var.get())
        self.operator.ar_qdk.get_history(
            time_start=self.startCal.get_date(),
            time_end=self.endCal.get_date(),
            trash_cat=trash_cat,
            trash_type=trash_type,
            carrier=carrier, auto_id=auto,
            polygon_object_id=pol_object_id,
            client=client, platform_id=platform_id
        )

    def draw_stat_tree(self, tree=None):
        self.can.delete('tree')
        if not tree:
            tree = self.tree
        try:
            self.tar.sortId(tree, '#0', reverse=True)
        except TypeError:
            pass
        self.can.create_window(self.w / 1.9, self.h / 1.7,
                               window=tree,
                               tag='tree')


    def openWin(self):
        Terminal.openWin(self)
        self.changed_record = None
        self.root.bind("<Double-Button-1>",
                       lambda event: self.clear_optionmenu(event))
        self.root.bind('<Escape>',
                       lambda event: self.operator.mainPage.openWin())

    def page_close_operations(self):
        self.changed_record = None
        self.hide_widgets(self.statisticInteractiveWidgets)
        self.root.unbind("<Button-1>")
        self.can.delete('amount_weight', 'statusel', 'tree')

    def initBlockImg(self, name, btnsname=None, slice='shadow', mode='new',
                     seconds=[], hide_widgets=[], **kwargs):
        Terminal.initBlockImg(self, name, btnsname,
                              hide_widgets=self.statisticInteractiveWidgets)


class AuthWin(Terminal):
    '''Окно авторизации'''

    def __init__(self, root, settings, operator, can):
        Terminal.__init__(self, root, settings, operator, can)
        self.name = 'AuthWin'
        self.buttons = settings.authBtns
        self.s = settings
        self.r = root
        self.currentUser = 'Андрей'
        self.font = '"Montserrat Regular" 14'

    def send_auth_command(self):
        """ Отправить команду на авторизацию """
        pw = self.auth_page_password_entry.get()
        login = self.auth_page_login_var.get()
        self.operator.ar_qdk.try_auth_user(username=login, password=pw)
        self.currentUser = login

    def createPasswordEntry(self):
        var = StringVar(self.r)
        bullet = '\u2022'
        pwEntry = Entry(self.r, border=0,
                        width=
                        el_sizes.entrys['authwin.password'][self.screensize][
                            'width'], show=bullet,
                        textvariable=var, bg=cs.auth_background_color,
                        font=self.font, fg='#BABABA',
                        insertbackground='#BABABA', highlightthickness=0)
        pwEntry.bind("<Button-1>", self.on_click)
        pwEntry.bind("<BackSpace>", self.on_click)

        return pwEntry

    def on_click(self, event):
        event.widget.delete(0, END)
        self.auth_page_password_entry.config(show='\u2022')

    def incorrect_login_act(self):
        self.auth_page_password_entry.config(show="", highlightthickness=1,
                                             highlightcolor='red')
        self.auth_page_password_entry.delete(0, END)
        self.auth_page_password_entry.insert(END, 'Неправильный пароль!')

    def get_login_type_cb(self):
        self.auth_page_login_var = StringVar()
        self.usersComboBox = AutocompleteCombobox(self.root,
                                                  textvariable=self.auth_page_login_var)
        self.usersComboBox['style'] = 'authwin.TCombobox'
        self.configure_combobox(self.usersComboBox)
        self.usersComboBox.set_completion_list(self.operator.get_users_reprs())
        self.usersComboBox.set("")
        self.usersComboBox.config(
            width=el_sizes.comboboxes['authwin.login'][self.screensize][
                'width'],
            height=el_sizes.comboboxes['authwin.login'][self.screensize][
                'height'],
            font=self.font)
        self.usersComboBox.bind('<Return>',
                                lambda event: self.send_auth_command())
        return self.usersComboBox

    def rebinding(self):
        self.usersComboBox.unbind('<Return>')
        self.auth_page_password_entry.unbind('<Return>')
        self.bindArrows()

    def drawing(self):
        Terminal.drawing(self)
        self.auth_page_password_entry = self.createPasswordEntry()
        self.auth_page_password_entry.bind('<Return>', lambda
            event: self.send_auth_command())
        self.usersChooseMenu = self.get_login_type_cb()
        self.can.create_window(self.s.w / 2, self.s.h / 1.61,
                               window=self.auth_page_password_entry,
                               tags=('maincanv', 'pw_win'))
        self.can.create_window(self.s.w / 2, self.s.h / 1.96,
                               window=self.usersChooseMenu, tag='maincanv')
        self.drawSlices(mode=self.name)
        self.buttons_creation(tagname='winBtn')

    def openWin(self):
        Terminal.openWin(self)
        self.drawWin('maincanv', 'start_background', 'login', 'password')
        self.can.delete('toolbar')
        self.can.delete('clockel')
        self.can.itemconfigure('btn', state='hidden')
        self.auth_page_password_entry.config(show='\u2022',
                                             highlightthickness=0)

    def page_close_operations(self):
        self.can.itemconfigure('btn', state='normal')
        self.can.close('tree')


class MainPage(Terminal):
    def __init__(self, root, settings, operator, can):
        Terminal.__init__(self, root, settings, operator, can)
        self.name = 'MainPage'
        self.buttons = settings.gateBtns + settings.manual_gate_control_btn
        self.count = 0
        self.orupState = False
        self.errorShown = False
        self.chosenTrashCat = 'deff'
        self.tree = self.create_tree()
        self.win_widgets.append(self.tree)
        self.btn_name = self.settings.mainLogoBtn
        self.make_abort_unactive()

    def create_tree(self):
        self.tar = CurrentTreeview(self.root, self.operator, height=18)
        self.tar.createTree()
        self.tree = self.tar.get_tree()
        self.tree.bind("<Double-Button-1>", self.OnDoubleClick)
        return self.tree

    def rebind_btns_after_orup_close(self):
        self.tree.bind("<Double-Button-1>", self.OnDoubleClick)

    def create_abort_round_btn(self):
        self.can.create_window(self.settings.abort_round[0][1],
                               self.settings.abort_round[0][2],
                               window=self.abort_round_btn,
                               tag='winBtn')

    def make_abort_active(self):
        btn = self.abort_round_btn
        btn['state'] = 'normal'

    def make_abort_unactive(self):
        btn = self.abort_round_btn
        btn['state'] = 'disabled'

    def drawMainTree(self):
        self.operator.ar_qdk.get_unfinished_records()
        self.can.create_window(self.w / 1.495, self.h / 2.8, window=self.tree,
                               tag='tree')
        #self.tar.sortId(self.tree, '#0', reverse=True)

    def drawing(self):
        Terminal.drawing(self)
        self.operator.ar_qdk.get_status()
        self.drawMainTree()
        self.drawWin('win', 'road', 'order', 'currentEvents',
                     'entry_gate_base', 'exit_gate_base')
        self.hiden_widgets += self.buttons_creation(tagname='winBtn')

    def drawRegWin(self):
        self.draw_block_win(self, 'regwin')

    def destroyBlockImg(self, mode='total'):
        Terminal.destroyBlockImg(self, mode)
        self.drawMainTree()

    def updateTree(self):
        self.operator.ar_qdk.get_unfinished_records()

    def OnDoubleClick(self, event):
        """ Реакция на дабл-клик по текущему заезду """
        self.record_id = self.tree.selection()[0]
        self.chosenStr = self.tree.item(self.record_id, "values")
        if self.chosenStr[2] == '-':
            self.draw_rec_close_win()
        else:
            self.draw_cancel_tare()

    def draw_rec_close_win(self):
        btnsname = 'closeRecBtns'
        self.initBlockImg(name='ensureCloseRec', btnsname=btnsname,
                          seconds=('second'),
                          hide_widgets=self.win_widgets)
        self.root.bind('<Return>', lambda event: self.operator.close_record(
            self.record_id))
        self.root.bind('<Escape>',
                       lambda event: self.destroyBlockImg(mode="total"))

    def draw_cancel_tare(self):
        btnsname = 'cancel_tare_btns'
        self.initBlockImg(name='cancel_tare', btnsname=btnsname,
                          seconds=('second'),
                          hide_widgets=self.win_widgets)
        self.root.bind('<Escape>',
                       lambda event: self.destroyBlockImg(mode="total"))

    def page_close_operations(self):
        self.can.delete('win', 'statusel', 'tree')
        self.operator.turn_cams(False)
        # self.hide_widgets(self.abort_round_btn)
        self.unbindArrows()

    def openWin(self):
        Terminal.openWin(self)
        #cams_zoom = [cam['name']+cam['zoom'] for cam in self.operator.cameras_info]
        if not self.cam_zoom:
            self.hide_zoomed_cam(True)
        self.operator.turn_cams(True)
        self.operator.ar_qdk.execute_method("get_gates_states")
        self.bindArrows()
        self.operator.draw_road_anim()
        self.draw_gate_arrows()
        self.draw_weight()
        if not self.operator.main_btns_drawn:
            self.create_main_buttons()
            self.operator.main_btns_drawn = True
        self.create_abort_round_btn()


class ManualGateControl(Terminal):
    def __init__(self, root, settings, operator, can):
        Terminal.__init__(self, root, settings, operator, can)
        self.name = 'ManualGateControl'
        self.buttons = self.settings.auto_gate_control_btn + self.settings.manual_open_internal_gate_btn + self.settings.manual_close_internal_gate_btn + \
                       self.settings.manual_open_external_gate_btn + self.settings.manual_close_external_gate_btn + self.settings.null_weight_btn
        self.btn_name = self.settings.mainLogoBtn
        self.external_gate_state = 'close'
        self.enternal_gate_state = 'close'

    def drawing(self):
        Terminal.drawing(self)
        self.drawWin('maincanv', 'road', 'manual_control_info_bar',
                     'entry_gate_base', 'exit_gate_base')
        self.hiden_widgets += self.buttons_creation(tagname='winBtn')

    def openWin(self):
        Terminal.openWin(self)
        self.operator.draw_road_anim()
        self.draw_gate_arrows()
        self.draw_weight()
        self.operator.turn_cams(True, 'cad_gross')
        self.operator.turn_cams(True, 'auto_exit')
        self.root.bind('<Escape>',
                       lambda event: self.operator.mainPage.openWin())

    def page_close_operations(self):
        self.root.unbind("Escape")
        self.can.delete('win', 'statusel', 'tree')
        self.operator.turn_cams(False)

