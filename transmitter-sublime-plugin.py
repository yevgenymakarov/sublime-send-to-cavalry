import sublime
import sublime_plugin
import re
import tempfile
import json
import urllib

url = "http://localhost:8080/post"

default_action_list = {
    "set_to_layer_id": "Set the text to the specified layer",
    "set_to_selected_layers": "Set the text to the selected layers",
    "create_new_layer_type": "Set the text to a new layer of the specified type",
    "execute_script": "Execute the script in Cavalry",
    "run_file_script_path": "Run the script saved to a temporary file"
}

supported_layers = {
    "textShape": "Text Shape",
    "javaScript": "JavaScript Utility",
    "javaScriptShape": "JavaScript Shape",
    "javaScriptDeformer": "JavaScript Deformer",
    "javaScriptModifier": "JavaScript Modifier",
    "javaScriptEmitter": "JavaScript Emitter",
    "skslShader": "SkSL Shader"
}

create_layer_list_items = [(value, key) for key, value in supported_layers.items()]


class SendToCavalryCommand(sublime_plugin.TextCommand):
    def run(self, edit, use_selection=False, action=None, layer_type=None, layer_id=None):
        if use_selection is True:
            text = self.view.substr(self.view.sel()[0])
        else:
            text = self.view.substr(sublime.Region(0, self.view.size()))

        action = action or self.view.settings().get("default_action") or "set_to_selected_layers"

        data = {"action": action, "text": text, "source": "sendToCavalryScript"}

        if action == "set_to_layer_id":
            data.update({
                "layer_id": layer_id or self.view.settings().get("cavalry_layer_id")
            })
        elif action == "create_new_layer_type":
            data.update({
                "layer_type": layer_type or self.view.settings().get("cavalry_layer_type")
            })
        elif action == "run_file_script_path":
            is_dirty = self.view.is_dirty()
            file_name = self.view.file_name()

            if use_selection is True or is_dirty or not file_name:
                try:
                    with tempfile.NamedTemporaryFile(mode="wt", encoding="utf-8", prefix="", suffix=".js", delete=False) as f:
                        file_name = f.name
                        f.write("(function () {\n" + text + "\n})()")
                except Exception:
                    sublime.status_message("Can't create a temporary file")
                    return

            data.update({
                "text": "",
                "script_path": file_name
            })

        data = json.dumps(data)

        try:
            with urllib.request.urlopen(url, data.encode(), timeout=2) as r:
                sublime.status_message(r.read().decode())
        except urllib.error.URLError:
            sublime.status_message("Can't connect to Cavalry")

    def is_enabled(self, use_selection=False):
        if use_selection is True:
            text = self.view.substr(self.view.sel()[0])
            return text.strip() != ""
        return True


class SendToCavalrySetDefaultActionCommand(sublime_plugin.TextCommand):
    def run(self, edit, default_action):
        if default_action == "set_to_selected_layers":
            text = "Selected layers"
        elif default_action == "execute_script":
            text = "Execute"
        elif default_action == "run_file_script_path":
            text = "Run file script"
        else:
            text = default_action

        self.view.settings().set("default_action", default_action)
        self.view.set_status("view_status", text)
        sublime.status_message(default_action_list[default_action])


class SendToCavalrySetLayerIdInputHandler(sublime_plugin.TextInputHandler):
    def name(self):
        return "text"

    def placeholder(self):
        return "Layer identifier (or an empty string to reset)"

    def initial_text(self):
        text = sublime.get_clipboard()
        return text.strip() if self.validate(text) else ""

    def preview(self, text):
        if text.strip() == "":
            return ""

        match = re.fullmatch(r'(\w+)(#\d+)', text.strip())

        if match and match.group(1) in supported_layers:
            return sublime.Html("Set the destination to <b>" + supported_layers[match.group(1)] + "</b> layer " + match.group(2))

        return sublime.Html("<i>Invalid identifier or unsupported layer type</i>")

    def validate(self, text):
        match = re.fullmatch(r'(\w+)#\d+', text.strip())

        if text.strip() == "" or match and match.group(1) in supported_layers:
            return True

        return False


class SendToCavalrySetLayerIdCommand(sublime_plugin.TextCommand):
    def run(self, edit, text):
        layer_id = text.strip()
        default_action = "set_to_layer_id" if layer_id else "set_to_selected_layers"

        self.view.settings().set("default_action", default_action)
        self.view.settings().set("cavalry_layer_id", layer_id)
        self.view.set_status("view_status", layer_id)
        sublime.status_message(default_action_list[default_action])

    def input_description(self):
        return "Send to Layer"

    def input(self, args):
        return SendToCavalrySetLayerIdInputHandler()


class SendToCavalrySetLayerTypeInputHandler(sublime_plugin.ListInputHandler):
    def name(self):
        return "layer_type"

    def placeholder(self):
        return "Type of layer to create"

    def list_items(self):
        return create_layer_list_items


class SendToCavalrySetLayerTypeCommand(sublime_plugin.TextCommand):
    def run(self, edit, layer_type):
        self.view.settings().set("default_action", "create_new_layer_type")
        self.view.settings().set("cavalry_layer_type", layer_type)
        self.view.set_status("view_status", layer_type)
        sublime.status_message(default_action_list["create_new_layer_type"])

    def input_description(self):
        return "Create a Layer"

    def input(self, args):
        return SendToCavalrySetLayerTypeInputHandler()
