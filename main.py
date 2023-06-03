import PySimpleGUI as Gui
import json
import uuid
import os

DATA_DIRECTORY = 'data\\'


class Content:
    """Class for content"""

    def __init__(self, data: dict):
        # TODO verify the integrity of data given the type
        if len(data) != 0:
            self.type = 1
            keys = list(data.keys())
            keys.remove('type')
            self.entry = keys[0]
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
            self.id = str(uuid.uuid4())
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
        return {'version': self.version, 'id': self.id, 'name': self.name, 'contents': contents}


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
            self.id = str(uuid.uuid4())
            self.name = ''
            self.sheets = []
        # sub data
        self.keys_edit_sheets = ['-EDIT_SHEET_' + self.sheets[i].id + '-' for i in range(len(self.sheets))]
        self.keys_export_sheets = ['-EXPORT_SHEET_' + self.sheets[i].id + '-' for i in range(len(self.sheets))]
        self.keys_delete_sheets = ['-DELETE_SHEET_' + self.sheets[i].id + '-' for i in range(len(self.sheets))]

    def get_sheet_from_key_edit(self, key: str) -> Sheet:
        for sheet in self.sheets:
            if key == '-EDIT_SHEET_' + sheet.id + '-':
                return sheet
        return Sheet({})

    def get_sheet_from_key_export(self, key: str) -> Sheet:
        for sheet in self.sheets:
            if key == '-EXPORT_SHEET_' + sheet.id + '-':
                return sheet
        return Sheet({})

    def get_sheet_from_key_delete(self, key: str) -> Sheet:
        for sheet in self.sheets:
            if key == '-DELETE_SHEET_' + sheet.id + '-':
                return sheet
        return Sheet({})

    def add_sheet(self, sheet: Sheet):
        for i in range(len(self.sheets)):
            if sheet.id == self.sheets[i].id:
                self.sheets[i] = sheet
        if sheet not in self.sheets:
            self.sheets.append(sheet)
        if len(self.sheets) != len(self.keys_edit_sheets):
            self.keys_edit_sheets = ['-EDIT_SHEET_' + self.sheets[i].id + '-' for i in range(len(self.sheets))]
        if len(self.sheets) != len(self.keys_export_sheets):
            self.keys_export_sheets = ['-EXPORT_SHEET_' + self.sheets[i].id + '-' for i in range(len(self.sheets))]
        if len(self.sheets) != len(self.keys_delete_sheets):
            self.keys_delete_sheets = ['-DELETE_SHEET_' + self.sheets[i].id + '-' for i in range(len(self.sheets))]

    def delete_sheet(self, sheet: Sheet):
        for i in range(len(self.sheets)):
            if sheet.id == self.sheets[i].id:
                self.sheets.pop(i)
        if len(self.sheets) != len(self.keys_edit_sheets):
            self.keys_edit_sheets = ['-EDIT_SHEET_' + self.sheets[i].id + '-' for i in range(len(self.sheets))]
        if len(self.sheets) != len(self.keys_export_sheets):
            self.keys_export_sheets = ['-EXPORT_SHEET_' + self.sheets[i].id + '-' for i in range(len(self.sheets))]
        if len(self.sheets) != len(self.keys_delete_sheets):
            self.keys_delete_sheets = ['-DELETE_SHEET_' + self.sheets[i].id + '-' for i in range(len(self.sheets))]

    def extract(self) -> dict:
        sheets = [sheet.extract() for sheet in self.sheets]
        return {'version': self.version, 'id': self.id, 'name': self.name, 'sheets': sheets}


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
        self.keys_edit_projects = ['-EDIT_PROJECT_' + self.projects[i].id + '-' for i in range(len(self.projects))]
        self.keys_export_projects = ['-EXPORT_PROJECT_' + self.projects[i].id + '-' for i in range(len(self.projects))]
        self.keys_delete_projects = ['-DELETE_PROJECT_' + self.projects[i].id + '-' for i in range(len(self.projects))]

    def get_project_from_key_edit(self, key: str) -> Project:
        for project in self.projects:
            if key == '-EDIT_PROJECT_' + project.id + '-':
                return project
        return Project({})

    def get_project_from_key_export(self, key: str) -> Project:
        for project in self.projects:
            if key == '-EXPORT_PROJECT_' + project.id + '-':
                return project
        return Project({})

    def get_project_from_key_delete(self, key: str) -> Project:
        for project in self.projects:
            if key == '-DELETE_PROJECT_' + project.id + '-':
                return project
        return Project({})

    def add_project(self, project: Project):
        for i in range(len(self.projects)):
            if project.id == self.projects[i].id:
                self.projects[i] = project
        if project not in self.projects:
            self.projects.append(project)
        if len(self.projects) != len(self.keys_edit_projects):
            self.keys_edit_projects = ['-EDIT_PROJECT_' + self.projects[i].id + '-' for i in range(len(self.projects))]
        if len(self.projects) != len(self.keys_export_projects):
            self.keys_export_projects = ['-EXPORT_PROJECT_' + self.projects[i].id + '-' for i in
                                         range(len(self.projects))]
        if len(self.projects) != len(self.keys_delete_projects):
            self.keys_delete_projects = ['-DELETE_PROJECT_' + self.projects[i].id + '-' for i in
                                         range(len(self.projects))]

    def delete_project(self, project: Project):
        for i in range(len(self.projects)):
            if project.id == self.projects[i].id:
                self.projects.pop(i)
        if len(self.projects) != len(self.keys_edit_projects):
            self.keys_edit_projects = ['-EDIT_PROJECT_' + self.projects[i].id + '-' for i in range(len(self.projects))]
        if len(self.projects) != len(self.keys_delete_projects):
            self.keys_export_projects = ['-EXPORT_PROJECT_' + self.projects[i].id + '-' for i in
                                         range(len(self.projects))]
        if len(self.projects) != len(self.keys_delete_projects):
            self.keys_delete_projects = ['-DELETE_PROJECT_' + self.projects[i].id + '-' for i in
                                         range(len(self.projects))]

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


def save_project(project: Project):
    name = "P[" + project.name + "]_" + project.id
    with open(DATA_DIRECTORY + name + '.json', 'x') as project_file:
        json.dump(project.extract(), project_file)


def save_sheet(sheet: Sheet):
    name = "S[" + sheet.name + "]_" + sheet.id
    with open(DATA_DIRECTORY + name + '.json', 'x') as sheet_file:
        json.dump(sheet.extract(), sheet_file)


def generate_main_window(app: Application) -> Gui.Window:
    column_layout = []
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
    else:
        for i in range(len(app.projects)):
            column_layout.append([
                Gui.Text(app.projects[i].name),
                Gui.Push(),
                Gui.Button('Edit', key='-EDIT_PROJECT_' + app.projects[i].id + '-'),
                Gui.Button('Export', key='-EXPORT_PROJECT_' + app.projects[i].id + '-'),
                Gui.Button('Delete', key='-DELETE_PROJECT_' + app.projects[i].id + '-')
            ])
        layout.append([Gui.Column(column_layout, size=(500, 150), expand_x=True, expand_y=True, scrollable=True,
                                  vertical_scroll_only=True)])
        layout.append([
            Gui.HorizontalSeparator()
        ])
        layout.append([
            Gui.Push(),
            Gui.FileBrowse('Import', enable_events=True, key='-IMPORT_PROJECT-', target='-IMPORT_PROJECT-',
                           file_types=(('JSON', '.json'),))
        ])
    return Gui.Window('Story Sheet', layout, size=(500, 275), resizable=True)


def generate_project_window(project: Project) -> Gui.Window:
    column_layout = []
    layout = [
        [
            Gui.Input(default_text=project.name, key='-INPUT_NAME_PROJECT-'),
            Gui.Push(),
            Gui.FileBrowse('Import', enable_events=True, key='-IMPORT_SHEET-', target='-IMPORT_SHEET-',
                           file_types=(('JSON', '.json'),)),
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
    else:
        for i in range(len(project.sheets)):
            column_layout.append([
                Gui.Text(project.sheets[i].name),
                Gui.Push(),
                Gui.Button('Edit', key='-EDIT_SHEET_' + project.sheets[i].id + '-'),
                Gui.Button('Export', key='-EXPORT_SHEET_' + project.sheets[i].id + '-'),
                Gui.Button('Delete', key='-DELETE_SHEET_' + project.sheets[i].id + '-')
            ])
        layout.append([Gui.Column(column_layout, size=(500, 150), expand_x=True, expand_y=True, scrollable=True,
                                  vertical_scroll_only=True)])
    layout.append([
        Gui.HorizontalSeparator()
    ])
    layout.append([
        Gui.Button('Save', key='-SAVE_PROJECT-'),
        Gui.Push(),
        Gui.Button('Close', key='-CLOSE-', tooltip='Data are not saved')
    ])
    return Gui.Window('Project', layout, size=(500, 300), resizable=True)


def generate_sheet_window(sheet: Sheet) -> Gui.Window:
    column_layout = []
    layout = [
        [
            Gui.Input(default_text=sheet.name, key='-INPUT_NAME_SHEET-')
        ],
        [
            Gui.HorizontalSeparator()
        ]
    ]
    if len(sheet.contents) == 0:
        sheet.add_content(Content({'type': 1, 'Nickname': ''}))
        sheet.add_content(Content({'type': 1, 'Nickname Origin': ''}))
        sheet.add_content(Content({'type': 1, 'Age': ''}))
        sheet.add_content(Content({'type': 1, 'Gender': ''}))
        sheet.add_content(Content({'type': 1, 'Date of Birth': ''}))
        sheet.add_content(Content({'type': 1, 'Place of Birth': ''}))
        sheet.add_content(Content({'type': 1, 'Ethnicity/Race/Species': ''}))
        sheet.add_content(Content({'type': 1, 'Occupation/Job': ''}))
        sheet.add_content(Content({'type': 1, 'Job Rank/Position': ''}))
    for i in range(len(sheet.contents)):
        column_layout.append([
            Gui.Text(sheet.contents[i].entry),
            Gui.Push(),
            Gui.Input(sheet.contents[i].content, key='-INPUT_1_' + str(i) + '-')
        ])
    layout.append([Gui.Column(column_layout, size=(500, 150), expand_x=True, expand_y=True, scrollable=True,
                              vertical_scroll_only=True)])
    layout.append([
        Gui.HorizontalSeparator()
    ])
    layout.append([
        Gui.Button('Save', key='-SAVE_SHEET-'),
        Gui.Push(),
        Gui.Button('Close', key='-CLOSE-', tooltip='Data may not be saved')
    ])
    return Gui.Window('Sheet', layout, size=(500, 300), resizable=True)


if __name__ == '__main__':
    # Initialisation
    application = init()
    window = generate_main_window(application)
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
                window = generate_main_window(application)
            elif current_window == 2:
                window.close()
                current_window = 1
                window = generate_project_window(current_project)

        if event == '-NEW_PROJECT-':
            window.close()
            current_window = 1
            current_project = Project({})
            window = generate_project_window(current_project)

        if event == '-NEW_SHEET-':
            window.close()
            current_window = 2
            current_sheet = Sheet({})
            window = generate_sheet_window(current_sheet)

        if event == '-SAVE_PROJECT-':
            # save date in current_project
            current_project.name = values['-INPUT_NAME_PROJECT-']
            # save project in application
            application.add_project(current_project)

        if event == '-SAVE_SHEET-':
            # save data in current_sheet
            current_sheet.name = values['-INPUT_NAME_SHEET-']
            # TODO for multiple type of content, split on '_' and match [1] for type
            for j in range(len(current_sheet.contents)):
                current_sheet.contents[j].content = values['-INPUT_1_' + str(j) + '-']
            # save sheet in current_project
            current_project.add_sheet(current_sheet)

        if event in application.keys_edit_projects:
            window.close()
            current_window = 1
            current_project = application.get_project_from_key_edit(event)
            window = generate_project_window(current_project)

        if event in application.keys_export_projects:
            current_window = 0
            export_project = application.get_project_from_key_export(event)
            save_project(export_project)

        if event in application.keys_delete_projects:
            window.close()
            current_window = 0
            delete_project = application.get_project_from_key_delete(event)
            application.delete_project(delete_project)
            window = generate_main_window(application)

        if event in current_project.keys_edit_sheets:
            window.close()
            current_window = 2
            current_sheet = current_project.get_sheet_from_key_edit(event)
            window = generate_sheet_window(current_sheet)

        if event in current_project.keys_export_sheets:
            current_window = 1
            export_sheet = current_project.get_sheet_from_key_export(event)
            save_sheet(export_sheet)

        if event in current_project.keys_delete_sheets:
            window.close()
            current_window = 1
            delete_sheet = current_project.get_sheet_from_key_delete(event)
            current_project.delete_sheet(delete_sheet)
            window = generate_project_window(current_project)

        if event == '-IMPORT_PROJECT-':
            project_path = values['-IMPORT_PROJECT-']
            window.close()
            current_window = 1
            with open(project_path) as import_project_file:
                project_data = json.load(import_project_file)
                current_project = Project(project_data)
            window = generate_project_window(current_project)

        if event == '-IMPORT_SHEET-':
            sheet_path = values['-IMPORT_SHEET-']
            window.close()
            current_window = 2
            with open(sheet_path) as import_sheet_file:
                sheet_data = json.load(import_sheet_file)
                current_sheet = Sheet(sheet_data)
            window = generate_sheet_window(current_sheet)

    window.close()
