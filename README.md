<h1 align="center">🚀 AdaptiClip</h1>
<p align="center">🗂️ A Clipboard Management Tool With Plugin Support for Automatic Text Conversion (eg., Dates, Times, JSON, etc.).</p>

[![AdaptiClip](https://hackatime-badge.hackclub.com/U091SE37HUN/Adapti-Clip?aliases=AdaptiClip&color=505050&label=AdaptiClip)](https://github.com/nishindudu/AdaptiClip)
[![Visitors](https://api.visitorbadge.io/api/visitors?path=https%3A%2F%2Fgithub.com%2Fnishindudu%2FAdaptiClip&countColor=%23606060&style=flat)](https://visitorbadge.io/status?path=https%3A%2F%2Fgithub.com%2Fnishindudu%2FAdaptiClip)

## ✨ Features
- 🧩 Plugin architecture for easy extensibility
- 📅 Includes plugins for various text formats (dates, times, JSON, etc.)
- ⌨️ Hotkey support for quick access
- ⚙️ Configurable settings via INI file

## 🛠️ Installation
1. 📥 Clone the repository:
    ```bash
    git clone https://github.com/nishindudu/AdaptiClip.git
    ```
2. 📂 Navigate to the project directory:
    ```bash
    cd AdaptiClip
    ```
3. 📦 Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```
4. ▶️ Run the application:
    ```bash
    python app.py
    ```

### Supported Platforms
- **Windows**: Fully supported (Tested)
- **macOS**: Should work (Uses cross platform libraries)
- **Linux**: Should work (Uses cross platform libraries)

> If you have tested on macOS or Linux, please [open an issue](https://github.com/nishindudu/AdaptiClip/issues) or a [submit a pull request](https://github.com/nishindudu/AdaptiClip/pulls) with edits to this documentation!

### 📝 Arguments
You can pass the following arguments to the application:

- `--trace`: 🐞 Enable trace logging
- `--verbose`: 📢 Enable verbose logging
- `--silent`: 🤫 Run the application in silent mode

     Passing `--silent` is recommended for normal use.

## 🚦 Usage
1. 📋 Copy any text to your clipboard.
2. 🔄 The application will automatically convert the text based on the active plugins.
3. ⚡ Use the configured hotkeys for quick access to specific plugins.

### ⌨️ Hotkey Setup
You can configure hotkeys for each plugin in the `config.ini` file.
> <b>📝 NOTE</b><br>
> `config.ini` file will be generated automatically on the first run.

For example (for setting a hotkey for JSON pretty print):

```ini
[JSONPrettyPrint]
on_keypress = true
hotkey = ctrl+alt+j
```

> <b>📝 NOTE</b><br>
> Setting a hotkey will disable auto-conversion for that plugin.

## 🧰 Troubleshooting
If you encounter any issues, please check the following:
- ✅ Ensure that all required packages are installed.
- 🛠️ Verify that the `config.ini` file is correctly configured.
- 🐞 Pass the `--trace` argument to enable trace logging and check the logs for any error messages.
     - 🐛 If you found a bug, please create an [issue](https://github.com/nishindudu/AdaptiClip/issues) on the GitHub repository or create a [pull request](https://github.com/nishindudu/AdaptiClip/pulls) with a fix.

## 🏗️ Creating Plugins
To create a new plugin for AdaptiClip, follow these steps:

1. 📄 Create a new Python file in the `plugins` directory.

2. 🏷️ Define a class and a constructor for your plugin (It should accept the config object).
     ```python
     class MyPlugin():
          def __init__(self, CONFIG): #Should accept the config object
                self.config = CONFIG
                # Initialize your plugin here
     ```

3. 🛠️ Implement the required methods for your plugin in the class.
     ```python
     class MyPlugin():
          def __init__(self, CONFIG): #Should accept the config object
                self.config = CONFIG
                self.config.create_section() # Required only if there are no attributes to set (auto created on setting attributes)

                # If your plugin should only work on hotkeys, set on_keypress = true in the config file
                self.config.write("on_keypress", "true") # Example for hotkey only mode
                self.config.write("hotkey", "ctrl+alt+m") # Define preferred hotkey
                # Set any required attributes

                key = self.config.read("key") # Example for reading a key

                # Initialize your plugin here

          def detect(self, text) -> bool: #Should return a boolean indicating if the text is in the expected format
                # Detect the text format using the config
                return True

          def convert(self, text):
                # Process the text
                return text
     ```
> <b>⚠️ IMPORTANT</b><br>
> `detect` and `convert` methods are **required** for all plugins.

> <b>⚠️ IMPORTANT</b><br>
> All plugins must create a section in the config file.
> If there are no attributes to be set, the section can be empty and can be created by calling `config.create_section()`.

Sample plugins are available in `/plugins` folder.

### ⚙️ Plugin Configuration

- Setting the plugin to hotkey mode
     ```python
     class MyPlugin():
          def __init__(self, CONFIG):
               self.config = CONFIG
               self.config.write("on_keypress", "true") # Setting this will disable auto-conversion
               self.config.write("hotkey", "ctrl+alt+m") # Setting a hotkey is required if your plugin is in hotkey only mode
     ```
     Example ini file:
     ```ini
     [MyPlugin]
     on_keypress = true
     hotkey = ctrl+alt+m
     ```

## 🤝 Contributing
We welcome contributions to AdaptiClip! If you'd like to contribute, please follow these steps:
1. 🍴 Fork the repository.

2. 🌿 Create a new branch for your feature or bug fix.
     ```bash
     git clone https://github.com/yourusername/AdaptiClip.git
     ```

3. ✍️ Make your changes and commit them.

4. 📬 Submit a pull request detailing your changes.

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.