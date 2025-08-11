import importlib
import time
import pyperclip
import configparser
import os
import argparse
import logging
import sys
import keyboard
import inspect

VERBOSITY_MAP = {
    "silent": logging.CRITICAL + 1,
    "default": logging.WARNING,
    "verbose": logging.INFO,
    "trace": logging.DEBUG
}

def parse_args():
    parser = argparse.ArgumentParser(description="Adapti-Clip: Smart Clipboard Management")

    verbosity_group = parser.add_mutually_exclusive_group()
    verbosity_group.add_argument(
        "-s", "--silent",
        action="store_const", const="silent", dest="verbosity",
        help="Suppress all output except fatal errors"
    )
    verbosity_group.add_argument(
        "-v", "--verbose",
        action="store_const", const="verbose", dest="verbosity",
        help="Show detailed output"
    )
    verbosity_group.add_argument(
        "-t", "--trace",
        action="store_const", const="trace", dest="verbosity",
        help="Show all debug info"
    )

    parser.set_defaults(verbosity="default")

    return parser.parse_args()

def configure_logging(level_name):
    level = VERBOSITY_MAP[level_name]
    logging.basicConfig(
        level=level,
        format="%(asctime)s - [%(levelname)s] - %(message)s",
        stream=sys.stdout
    )

PLUGINS = []
CONFIG = None
HOTKEYS = []
PLUGINS_ON_KEYPRESS = {}

last_content = None
replaced_content = None

def load_config():
    if not os.path.exists("config.ini"):
        open("config.ini", "a").close()
    global CONFIG
    CONFIG = configparser.ConfigParser()
    CONFIG.read("config.ini")

    if not CONFIG.has_section("APP"):
        CONFIG.add_section("APP")
        logging.info("Created 'APP' section in config.ini")

    with open("config.ini", "w") as configfile:
        CONFIG.write(configfile)

class SafeConfig():
    def __init__(self, config, config_path):
        self.config = config
        self.config_path = config_path
        self.caller_class = None

    def create_section(self, class_name=None):
        if class_name is None:
            caller = inspect.stack()[1]
            self.caller_class = caller[0].f_locals["self"].__class__.__name__
            class_name = str(self.caller_class)

        if not os.path.exists(self.config_path):
            open(self.config_path, "a").close()
        
        if not self.config.has_section(class_name):
            self.config.add_section(class_name)
        
        with open(self.config_path, "w") as configfile:
            self.config.write(configfile)

    def read(self, key):
        caller = inspect.stack()[1]
        self.caller_class = caller[0].f_locals["self"].__class__.__name__
        
        if not os.path.exists(self.config_path):
            open(self.config_path, "a").close()

        if not self.config.has_section(self.caller_class):
            self.create_section(self.caller_class)

        value = self.config.get(self.caller_class, key)
        return value

    def write(self, key, value):
        caller = inspect.stack()[1]
        self.caller_class = caller[0].f_locals["self"].__class__.__name__

        if not self.config.has_section(self.caller_class):
            self.create_section(self.caller_class)
        self.config.set(self.caller_class, key, value)

        with open(self.config_path, "w") as configfile:
            self.config.write(configfile)

def import_plugins():
    global PLUGINS
    global PLUGINS_ON_KEYPRESS
    global CONFIG
    logging.debug("Importing plugins...")
    safe = SafeConfig(CONFIG, "config.ini")
    for file in os.listdir("plugins"):
        if file.endswith(".py"):
            module_name = file[:-3]
            module_path = f"plugins.{module_name}"

            try:
                module = importlib.import_module(module_path)
                for attr_name in dir(module):
                    attr = getattr(module, attr_name)
                    if isinstance(attr, type):
                        if CONFIG.get(str(attr.__name__), "on_keypress", fallback='false') == 'true':
                            key = CONFIG.get(str(attr.__name__), "hotkey", fallback=None)
                            PLUGINS_ON_KEYPRESS[attr(safe)] = key
                            continue
                        PLUGINS.append(attr(safe))
            except Exception as e:
                logging.error(f"Error importing plugin {module_name}: {e}")
    logging.debug(f"Always on Plugins: {[plug.__class__.__name__ for plug in PLUGINS]}, Plugins On Key Press: {[plug.__class__.__name__ for plug in PLUGINS_ON_KEYPRESS]}")
    logging.debug(f"Total plugins loaded: {len(PLUGINS) + len(PLUGINS_ON_KEYPRESS)}")

    logging.debug("Loaded plugins:")
    for plugin in PLUGINS:
        logging.debug(f" • {plugin.__class__.__name__}")


def check_for_matiching_plugins(text):
    global PLUGINS
    matching_plugins = [plugin for plugin in PLUGINS if plugin.detect(text)]
    if len(matching_plugins) > 1:
        logging.warning(f"Multiple plugins matched for text: {text}. Using first match: {matching_plugins[0].__class__.__name__}")
        logging.warning("Matching plugins:")
        for plugin in matching_plugins:
            logging.warning(f" • {plugin.__class__.__name__}")
    return matching_plugins

def process_text(text):
    global replaced_content
    global PLUGINS
    matching_plugins = check_for_matiching_plugins(text)
    if matching_plugins:
        replaced_content = matching_plugins[0].convert(text)
        return replaced_content
    return text


def check_clipboard():
    global last_content
    global replaced_content
    content = pyperclip.paste()

    if content != last_content and content != replaced_content:
        last_content = content
        return content
    return None


class hotkeys():
    def __init__(self):
        global HOTKEYS
        global PLUGINS_ON_KEYPRESS
        self.plugins_on_keypress = PLUGINS_ON_KEYPRESS
        self.hotkeys = HOTKEYS
        pass

    def add_hotkey(self, key, callback):
        self.hotkeys.append(key)
        keyboard.add_hotkey(key, callback)
        return True
    
    def remove_hotkey(self, key):
        if key in self.hotkeys:
            self.hotkeys.remove(key)
            keyboard.remove_hotkey(key)
            return True
        return False

    def on_key_press(self, plugin, text):
        logging.debug(f"Hotkey pressed for plugin: {plugin.__class__.__name__}")
        if plugin.detect(text):
            logging.debug(f"Plugin {plugin.__class__.__name__} detected text.")
            res = plugin.convert(text)
            if res:
                pyperclip.copy(res)

    def set_from_config(self):
        for plugin, key in self.plugins_on_keypress.items():
            if key:
                self.add_hotkey(key, lambda p=plugin, t=pyperclip.paste(): self.on_key_press(p, t))


if __name__ == "__main__":
    args = parse_args()
    configure_logging(args.verbosity)
    load_config()
    import_plugins()
    hotkeys().set_from_config()

    logging.debug("Starting clipboard monitoring...")

    while True:
        new_content = check_clipboard()
        if new_content:
            logging.info(f"New clipboard content detected: {new_content}")
            processed_content = process_text(new_content)
            if processed_content != new_content:
                logging.debug(f"Processed content: {processed_content}")
                pyperclip.copy(processed_content)
                logging.info(f"Clipboard updated with processed content")
            else:
                logging.debug("No changes made to the clipboard content.")

        try:
            time.sleep(0.8)
        except KeyboardInterrupt:
            logging.info("Clipboard monitoring stopped.")
            break