from kivyauth.google_auth import initialize_google, login_google, logout_google
from kivy.core.text import LabelBase
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDIconButton, MDTextButton
from kivymd.uix.textfield import MDTextField
import kivymd.uix.navigationdrawer
import kivymd.uix.transition.transition
from kivymd.uix.toolbar import MDTopAppBar, MDBottomAppBar
from datetime import date
from datetime import datetime
from kivymd.uix.behaviors import FakeRectangularElevationBehavior
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.screen import MDScreen
from kivymd.theming import ThemeManager
from kivymd.uix.pickers import MDDatePicker, MDColorPicker
from kivymd.uix.dialog import MDDialog
from kivymd.uix.navigationdrawer import MDNavigationDrawerHeader, MDNavigationDrawerItem, MDNavigationDrawerDivider, MDNavigationDrawer, MDNavigationDrawerLabel, MDNavigationLayout, MDNavigationDrawerMenu
from kivymd.uix.list import OneLineAvatarIconListItem, IRightBodyTouch, MDList, TwoLineAvatarIconListItem, ILeftBody, OneLineIconListItem, IconLeftWidget
from kivy.uix.scrollview import ScrollView
from kivymd.uix.card import MDCard
from kivymd.uix.imagelist import MDSmartTile
from database import Database

db = Database()

Window.size = (470,700)

class Main(Screen):
    pass

class LogIn(Screen):
    pass

class LogIn_Student(Screen):
    pass

class LogIn_Staff(Screen):
    pass

class LogIn_Organization(Screen):
    pass

class SignUp(Screen):
    pass

class SignUp_Student(Screen):
    pass

class SignUp_Staff(Screen):
    pass

class SignUp_Organization(Screen):
    pass

class Home(Screen):
    pass

class Task(Screen):
    pass

class Theme(Screen):
    pass

class YourContainer(IRightBodyTouch, MDBoxLayout):
    adaptive_width = True

class DialogContent(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ids.date_text.text = datetime.now().strftime("%A %d %B %Y")
    
    def show_date_pick(self):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_save)
        date_dialog.open()

    def on_save(self, instance, value, date_range):
        date = value.strftime("%A %d %B %Y")
        self.ids.date_text.text = str(date)

class TimeTableTask(FakeRectangularElevationBehavior):
    pass

class ListItemWithCheckbox(TwoLineAvatarIconListItem):
    def __init__(self, pk=None, **kwargs):
        super().__init__(**kwargs)
        self.pk = pk

    def mark(self, check, the_list_item):
        if check.active == True:
            the_list_item.text = '[s]' + the_list_item.text + '[/s]'
            db.mark_task_as_complete(the_list_item.pk)
        else:
            the_list_item.text = str(db.mark_task_as_incomplete(the_list_item.pk))
    
    def delete_item(self, the_list_item):
        self.parent.remove_widget(the_list_item)
        db.delete_task(the_list_item.pk)

class LeftCheckBox(ILeftBody, MDCheckbox):
    pass

class Success(MDNavigationLayout):
    pass

class TimeTable(MDApp):
    task_list_dialog = None
    def build(self):
        # self.theme_cls.theme_style = "Dark"
        # screen_manager = ScreenManager()
        # client_id = open("client_id.txt")
        # client_secret = open("client_secret.txt")
        # initialize_google(self.after_login, self.error_listener, client_id.read(), client_secret.read())
        # screen_manager.add_widget(Builder.load_file("main.kv"))
        # screen_manager.add_widget(Builder.load_file("signup.kv"))
        # screen_manager.add_widget(Builder.load_file("signup_student.kv"))
        # screen_manager.add_widget(Builder.load_file("home.kv"))
        # screen_manager.add_widget(Builder.load_file("signup_staff.kv"))
        # screen_manager.add_widget(Builder.load_file("signup_organization.kv"))
        # screen_manager.add_widget(Builder.load_file("login_student.kv"))
        # screen_manager.add_widget(Builder.load_file("login_staff.kv"))
        # screen_manager.add_widget(Builder.load_file("login.kv"))
        # screen_manager.add_widget(Builder.load_file("login_organization.kv"))
        # screen_manager.add_widget(Builder.load_file("theme.kv"))
     
        # return screen_manager

        return Builder.load_file('home.kv')
    
    def verify_data(self, uname, email, password):
        from firebase import firebase

        firebase = firebase.FirebaseApplication("https://timetable-scheduling-app-default-rtdb.firebaseio.com/", None)

        result = firebase.get('timetable-scheduling-app-default-rtdb/Users', '')

        for i in result.keys():
                if result[i]['Email'] == email:
                    if result[i]['Password'] == password:
                        print(email + "Logged In")
                    else:
                        print(email + "Password Incorrect")

    def send_data(self, uname, email, password):
        from firebase import firebase

        firebase = firebase.FirebaseApplication("https://timetable-scheduling-app-default-rtdb.firebaseio.com/", None)

        data = {
            'Username': uname,
            'Email': email,
            'Password': password
        }
        firebase.post('timetable-scheduling-app-default-rtdb/Users', data)
                

    def after_login(self, name, email, photo_url):
        self.root.ids.label.test = f"Logged in as {name}"
        self.root.transition.direction = "left"
        self.root.current = "home"

    def error_listener(self):
        print("Login Failed")

    def login(self):
        login_google()
        
    def logout(self):
        logout_google()
    
    def after_logout(self):
        self.root.ids.label.test = "Logged out"
        self.root.transition.direction = "right"
        self.root.current = "main"

    def navigation_draw(self):
        print("Navigation")

    # def toggle_nav_drawer(self):
    #     self.toggle_state(True)
    def Date(self):
        super().__init__()
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_save)
        date_dialog.open()

    def on_save(self, instance, date, date_range):
        print(date)
    
    def check(self, checkbox, value):
        if value:
            self.theme_cls.theme_style = "Dark"
        else:
            self.theme_cls.theme_style = "Light"
    
    def show_task_dialog(self):
        if not self.task_list_dialog:
            self.task_list_dialog = MDDialog(
                title="Task List",
                type="custom",
                content_cls = DialogContent()
            )
            self.task_list_dialog.open()

    def adding_tasks(self, task, task_date):
        print(task.text, task_date)
        created_task = db.create_task(task.text, task_date)
        work = self.root.get_screen("task")
        work.ids['container'].add_widget(ListItemWithCheckbox(pk = created_task[0], text = '[b]' + created_task[1] + '[/b]', 
                                                                   secondary_text = created_task[2]))
        task.text = ''

    def close_dialog(self, *args):
        self.task_list_dialog.dismiss()

    def show_themepicker(self):
        picker = MDColorPicker()
        picker.open()    

    def on_start(self):
        '''This is to load the saved tasks and add them to the MDList widget'''
        completed_tasks, incompleted_tasks = db.get_tasks()

        if incompleted_tasks != []:
            for task in incompleted_tasks:
                add_task = ListItemWithCheckbox(pk=task[0], text=task[1], secondary_text = task[2])
                work = self.root.get_screen("task")
                work.ids['container'].add_widget(add_task)

        if completed_tasks != []:
            for task in completed_tasks:
                add_task = ListItemWithCheckbox(pk = task[0], text = "[s]" + task[1] + "[/s]", secondary_text = task[2])
                add_task.ids.check.active = True
                work = self.root.get_screen("task")
                work.ids['container'].add_widget(add_task)        

if __name__ == '__main__':
    app = TimeTable()
    app.run()

# Client ID: 316921396244-ni59da3g2cb7j7pun1opi1qnosuoi1u6.apps.googleusercontent.com
# Client Secret: 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

