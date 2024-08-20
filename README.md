# Send to Cavalry

Use [Sublime Text](https://www.sublimetext.com) as an external script editor for [Cavalry](https://cavalry.scenegroup.co). Execute scripts directly from Sublime Text. Set expressions to JavaScript layers or update text in Text Shapes.

For the _Visual Studio Code_ editor, see the [Stallion](https://github.com/scenery-io/stallion) extension.

## Installation

Download and unzip the archive: [sublime-send-to-cavalry.zip](https://github.com/yevgenymakarov/sublime-send-to-cavalry/releases/latest/download/sublime-send-to-cavalry.zip).

It contains two files, `Receiver.js` and `Send to Cavalry.sublime-package`, which you need to install.

### Cavalry Script

Copy the `Receiver.js` file to the `Scripts` directory, which you can find using the Cavalry menu item `Help → Show Scripts Folder`.

### Sublime Text Package

Copy the `Send to Cavalry.sublime-package` file to the `Installed Packages` directory, which you can find using the Sublime Text menu item `Preferences → Browse Packages…` and then going one level higher.

## Usage

In Cavalry, use the `Scripts → Receiver` menu item to start the server. The `Receiver.js` script window needs to be open in Cavalry to receive data and perform actions.

Open the **Command Palette** via the Sublime Text menu item `Tools → Command Palette…` and type _Send to Cavalry_ to find the plugin commands. These commands are also presented in the right-click context menu.

### Select the Action

Select the type of action you want to perform, your choice will be saved for the current tab, and the current setting will be displayed in the status bar. The default action is "Send to Selected Layers". Available options:

- **Send to Layer.** Sets the text to the specified layer. Use the "Copy Layer Id" item of the layer context menu in Cavalry to get the desired layer identifier.
- **Send to Selected Layers.** Sets the text to the currently selected layers in Cavalry. Unsupported layers will be ignored.
- **Create a New Layer.** Creates a new layer of the specified type with the current text.
- **Execute.** Executes the script in Cavalry.
- **Run File Script.** Saves the script to a temporary file and runs it in Cavalry, this option is required for UI scripts. It will run the current file directly if it is saved.

### Send a Text to Cavalry

Call the "Send to Cavalry" command to send a text and perform the selected or default action. You can send only highlighted text using the "Send to Cavalry (Selection)" command.

The default keyboard shortcut for the "Send to Cavalry" command is `cmd/ctrl + shift + c`.

## Customization

### Key Bindings

Use the menu item `Preferences → Key Bindings` to add custom key bindings. See the `Context.sublime-menu` file in this repository for possible commands and arguments.

### Unzipped Package Installation

Download the source code archive. Unzip the archive and copy the folder to the `Packages` directory, which you can find using the menu item `Preferences → Browse Packages…`.

## Notes

**Supported layer types:**

- Text Shape
- JavaScript Utility
- JavaScript Shape
- JavaScript Deformer
- JavaScript Modifier
- JavaScript Emitter
- SkSL Shader

The server address and port `localhost:8080` are hard-coded, see **Unzipped Package Installation** to change the source files.
