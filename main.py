import PySimpleGUI as Gui
import json
import uuid
import os

DATA_DIRECTORY = 'data\\'


class Content:
    def __init__(self, data: dict):
        if len(data) != 0:
            self.type = 1
            self.entry = 'name'
            self.content = data[self.entry]
        else:
            self.type = 1
            self.entry = 'name'
            self.content = ''

    def extract(self) -> dict:
        return {self.entry: self.content, 'type': self.type}


class Sheet:
    """Class for sheet"""

    def __init__(self, data: dict):
        # data
        if len(data) != 0:
            self.version = data['version']
            self.id = data['id']
            self.name = data['name']
            self.contents = [Content(content) for content in data['contents']]
        else:
            self.version = 0
            self.id = uuid.uuid4()
            self.name = ''
            self.contents = []
        # sub data
        self.keys_contents = ['-INPUT_1_' + str(i) + '-' for i in range(len(self.contents))]

    def add_content(self, content: Content):
        self.contents.append(content)
        if len(self.contents) != len(self.keys_contents):
            self.keys_contents = ['-INPUT_1_' + str(i) + '-' for i in range(len(self.contents))]

    def extract(self) -> dict:
        contents = [content.extract() for content in self.contents]
        return {'version': self.version, 'id': str(self.id), 'name': self.name, 'contents': contents}


class Project:
    """Class for project"""

    def __init__(self, data: dict):
        # data
        if len(data) != 0:
            self.version = data['version']
            self.id = data['id']
            self.name = data['name']
            self.sheets = [Sheet(sheet) for sheet in data['sheets']]
        else:
            self.version = 0
            self.id = uuid.uuid4()
            self.name = ''
            self.sheets = []
        # sub data
        self.keys_sheets = ['-EDIT_SHEET_' + str(self.sheets[i].id) + '-' for i in range(len(self.sheets))]

    def get_sheet_from_key(self, key: str) -> Sheet:
        for project in self.sheets:
            if key == '-EDIT_SHEET_' + str(project.id) + '-':
                return project
        return Sheet({})

    def add_sheet(self, sheet: Sheet):
        for i in range(len(self.sheets)):
            if sheet.id == self.sheets[i]:
                self.sheets[i] = sheet
        if sheet not in self.sheets:
            self.sheets.append(sheet)
        if len(self.sheets) != len(self.keys_sheets):
            self.keys_sheets = ['-EDIT_SHEET_' + str(self.sheets[i].id) + '-' for i in range(len(self.sheets))]

    def extract(self) -> dict:
        sheets = [sheet.extract() for sheet in self.sheets]
        return {'version': self.version, 'id': str(self.id), 'name': self.name, 'sheets': sheets}


class Settings:
    def __init__(self, data: dict):
        if len(data) != 0:
            self.language = data['language']
            self.hotkeys = data['hotkeys']

    def extract(self) -> dict:
        hotkeys = [hotkey for hotkey in self.hotkeys]
        return {'language': self.language, 'hotkeys': hotkeys}


class Application:
    """Global class for the app"""

    def __init__(self, data: dict):
        # data
        if len(data) != 0:
            self.version = data['version']
            self.settings = data['settings']
            self.projects = [Project(project) for project in data['projects']]
        else:
            self.version = 1
            self.settings = {'language': 'FR_fr', 'hotkeys': []}
            self.projects = []
        # sub data
        self.keys_projects = ['-EDIT_PROJECT_' + str(self.projects[i].id) + '-' for i in range(len(self.projects))]

    def get_project_from_key(self, key: str) -> Project:
        for project in self.projects:
            if key == '-EDIT_PROJECT_' + str(project.id) + '-':
                return project
        return Project({})

    def add_project(self, project: Project):
        for i in range(len(self.projects)):
            if project.id == self.projects[i]:
                self.projects[i] = project
        if project not in self.projects:
            self.projects.append(project)
        if len(self.projects) != len(self.keys_projects):
            self.keys_projects = ['-EDIT_PROJECT_' + str(self.projects[i].id) + '-' for i in range(len(self.projects))]

    def extract(self) -> dict:
        projects = [project.extract() for project in self.projects]
        return {'version': self.version, 'projects': projects, 'settings': self.settings}


def init() -> Application:
    # First start
    if not os.path.isdir(DATA_DIRECTORY):
        os.mkdir('data')
    if not os.path.isfile(DATA_DIRECTORY + 'data.json'):
        open(DATA_DIRECTORY + 'data.json', 'x')
        return Application({})
    else:
        with open(DATA_DIRECTORY + 'data.json') as data_file:
            data = json.load(data_file)
        return Application(data)


def save(data: Application) -> None:
    with open(DATA_DIRECTORY + 'data.json', 'w') as data_file:
        json.dump(data.extract(), data_file)


def generate_main_layout(app: Application) -> []:
    layout = [
        [
            Gui.Button('Settings', key='-SETTINGS-'),
            Gui.Push(),
            Gui.Button('New Project', key='-NEW_PROJECT-')
        ],
        [
            Gui.Text('Projects'),
            Gui.HorizontalSeparator()
        ]
    ]
    if len(app.projects) == 0:
        layout.append([Gui.Text('No project')])
    for i in range(len(app.projects)):
        layout.append([
            Gui.Text(app.projects[i].name),
            Gui.Push(),
            Gui.Button('Edit', key='-EDIT_PROJECT_' + str(app.projects[i].id) + '-')
        ])
    return layout


def generate_project_layout(project: Project) -> []:
    layout = [
        [
            Gui.Input(default_text=project.name, key='-INPUT_NAME_PROJECT-'),
            Gui.Push(),
            Gui.Button('New Sheet', key='-NEW_SHEET-')
        ],
        [
            Gui.Text('Sheets'), Gui.HorizontalSeparator()
        ]
    ]
    if len(project.sheets) == 0:
        layout.append([
            Gui.Text('No sheet')
        ])
    for i in range(len(project.sheets)):
        layout.append([
            Gui.Text(project.sheets[i].name),
            Gui.Push(),
            Gui.Button('Edit', key='-EDIT_SHEET_' + str(project.sheets[i].id) + '-')
        ])
    layout.append([
        Gui.HorizontalSeparator()
    ])
    layout.append([
        Gui.Button('Save', key='-SAVE_PROJECT-'),
        Gui.Push(),
        Gui.Button('Close', key='-CLOSE-', tooltip='Data are not saved')
    ])
    return layout


def generate_sheet_layout(sheet: Sheet) -> []:
    # TODO Template to be define
    layout = [
        [
            Gui.Input(default_text=sheet.name, key='-INPUT_NAME_SHEET-')
        ],
        [
            Gui.HorizontalSeparator()
        ]
    ]
    if len(sheet.contents) == 0:
        sheet.add_content(Content({}))
    for i in range(len(sheet.contents)):
        layout.append([
            Gui.Text(sheet.contents[i].entry),
            Gui.Push(),
            Gui.Input(sheet.contents[i].content, key='-INPUT_1_' + str(i) + '-')
        ])
    layout.append([
        Gui.HorizontalSeparator()
    ])
    layout.append([
        Gui.Button('Save', key='-SAVE_SHEET-'),
        Gui.Push(),
        Gui.Button('Close', key='-CLOSE-', tooltip='Data are not saved')
    ])
    return layout


if __name__ == '__main__':
    # Initialisation
    application = init()
    # application = Application({'version': 1, 'projects': [], 'settings': {'language': 'FR_fr', 'hotkeys': []}})
    window = Gui.Window('Story Sheet', generate_main_layout(application))
    current_window = 0
    current_project = Project({})
    current_sheet = Sheet({})

    # Global While
    while True:
        event, values = window.read()

        if event == Gui.WIN_CLOSED or event == '-CLOSE-':
            if current_window == 0:
                save(application)
                break
            elif current_window == 1:
                window.close()
                current_window = 0
                window = Gui.Window('Story Sheet', generate_main_layout(application))
            elif current_window == 2:
                window.close()
                current_window = 1
                window = Gui.Window('Project', generate_project_layout(current_project))

        if event == '-NEW_PROJECT-':
            window.close()
            current_window = 1
            current_project = Project({})
            window = Gui.Window('New Project', generate_project_layout(current_project))

        if event == '-NEW_SHEET-':
            window.close()
            current_window = 2
            current_sheet = Sheet({})
            window = Gui.Window('New Sheet', generate_sheet_layout(current_sheet))

        if event == '-SAVE_PROJECT-':
            # save date in current_project
            current_project.name = values['-INPUT_NAME_PROJECT-']
            # save project in application
            application.add_project(current_project)

        if event == '-SAVE_SHEET-':
            # save data in current_sheet
            current_sheet.name = values['-INPUT_NAME_SHEET-']
            # TODO for multiple type of content, split on '_' and match [1]
            for j in range(len(current_sheet.contents)):
                current_sheet.contents[j].content = values['-INPUT_1_' + str(j) + '-']
            # save sheet in current_project
            current_project.add_sheet(current_sheet)

        if event in application.keys_projects:
            window.close()
            current_window = 1
            current_project = application.get_project_from_key(event)
            window = Gui.Window('Edit Project', generate_project_layout(current_project))

        if event in current_project.keys_sheets:
            window.close()
            current_window = 2
            current_sheet = current_project.get_sheet_from_key(event)
            window = Gui.Window('Edit Sheet', generate_sheet_layout(current_sheet))

    window.close()
