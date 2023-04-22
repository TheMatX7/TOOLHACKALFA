import os
import sys
import webbrowser
from platform import system
from traceback import print_exc
from typing import Callable
from typing import List
from typing import Tuple


def clear_screen():
    os.system("cls" if system() == "Windows" else "clear")


def validate_input(ip, val_range):
    val_range = val_range or []
    try:
        ip = int(ip)
        if ip in val_range:
            return ip
    except Exception:
        return None
    return None


class HackingTool(object):
    # About the HackingTool
    TITLE: str = ""  # used to show info in the menu
    DESCRIPTION: str = ""

    INSTALL_COMMANDS: List[str] = []
    INSTALLATION_DIR: str = ""

    UNINSTALL_COMMANDS: List[str] = []

    RUN_COMMANDS: List[str] = []

    OPTIONS: List[Tuple[str, Callable]] = []

    PROJECT_URL: str = ""

    def __init__(self, options = None, installable: bool = True,
                 runnable: bool = True):
        options = options or []
        if isinstance(options, list):
            self.OPTIONS = []
            if installable:
                self.OPTIONS.append(('Install', self.install))
            if runnable:
                self.OPTIONS.append(('Run', self.run))
            self.OPTIONS.extend(options)
        else:
            raise Exception(
                "options must be a list of (option_name, option_fn) tuples")

    def show_info(self):
        desc = self.DESCRIPTION
        if self.PROJECT_URL:
            desc += '\n\t[*] '
            desc += self.PROJECT_URL
        os.system(f'echo "{desc}"|boxes -d boy | lolcat')

    def show_options(self, parent = None):
        clear_screen()
        self.show_info()
        for index, option in enumerate(self.OPTIONS):
            print(f"[{index + 1}] {option[0]}")
        if self.PROJECT_URL:
            print(f"[{98}] STRONA PROJEKTU")
        print(f"[{99}] WROC DO {parent.TITLE if parent is not None else 'WYJSCIE'}")
        option_index = input("WYBEIRZ : ").strip()
        try:
            option_index = int(option_index)
            if option_index - 1 in range(len(self.OPTIONS)):
                ret_code = self.OPTIONS[option_index - 1][1]()
                if ret_code != 99:
                    input("\n\nNacisnij ENTER aby kontynuowac:").strip()
            elif option_index == 98:
                self.show_project_page()
            elif option_index == 99:
                if parent is None:
                    sys.exit()
                return 99
        except (TypeError, ValueError):
            print("Wprowadz prawidlowa opcje")
            input("\n\nNacisnij ENTER aby kontynuowac:").strip()
        except Exception:
            print_exc()
            input("\n\nNacisnij ENTER aby kontynuowac:").strip()
        return self.show_options(parent = parent)

    def before_install(self):
        pass

    def install(self):
        self.before_install()
        if isinstance(self.INSTALL_COMMANDS, (list, tuple)):
            for INSTALL_COMMAND in self.INSTALL_COMMANDS:
                os.system(INSTALL_COMMAND)
            self.after_install()

    def after_install(self):
        print("Instalacja sie udala!")

    def before_uninstall(self) -> bool:
        """ Ask for confirmation from the user and return """
        return True

    def uninstall(self):
        if self.before_uninstall():
            if isinstance(self.UNINSTALL_COMMANDS, (list, tuple)):
                for UNINSTALL_COMMAND in self.UNINSTALL_COMMANDS:
                    os.system(UNINSTALL_COMMAND)
            self.after_uninstall()

    def after_uninstall(self):
        pass

    def before_run(self):
        pass

    def run(self):
        self.before_run()
        if isinstance(self.RUN_COMMANDS, (list, tuple)):
            for RUN_COMMAND in self.RUN_COMMANDS:
                os.system(RUN_COMMAND)
            self.after_run()

    def after_run(self):
        pass

    def is_installed(self, dir_to_check = None):
        print("Unimplemented: DO NOT USE")
        return "?"

    def show_project_page(self):
        webbrowser.open_new_tab(self.PROJECT_URL)


class HackingToolsCollection(object):
    TITLE: str = ""  # used to show info in the menu
    DESCRIPTION: str = ""
    TOOLS = []  # type: List[Any[HackingTool, HackingToolsCollection]]

    def __init__(self):
        pass

    def show_info(self):
        os.system("figlet -f standard -c {} | lolcat".format(self.TITLE))
        # os.system(f'echo "{self.DESCRIPTION}"|boxes -d boy | lolcat')
        # print(self.DESCRIPTION)

    def show_options(self, parent = None):
        clear_screen()
        self.show_info()
        for index, tool in enumerate(self.TOOLS):
            print(f"[{index} {tool.TITLE}")
        print(f"[{99}] Wroc do {parent.TITLE if parent is not None else 'Wyjscie'}")
        tool_index = input("Wybierz narzedzie aby kontynuowac: ").strip()
        try:
            tool_index = int(tool_index)
            if tool_index in range(len(self.TOOLS)):
                ret_code = self.TOOLS[tool_index].show_options(parent = self)
                if ret_code != 99:
                    input("\n\nNacisnij ENTER aby kontynuowac:").strip()
            elif tool_index == 99:
                if parent is None:
                    sys.exit()
                return 99
        except (TypeError, ValueError):
            print("Wprowadz prawidlowa opcje")
            input("\n\nNacisnij ENTER aby kontynuowac:").strip()
        except Exception:
            print_exc()
            input("\n\nNacisnij ENTER aby kontynuowac:").strip()
        return self.show_options(parent = parent)
