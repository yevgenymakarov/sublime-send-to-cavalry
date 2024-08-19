const host = "localhost";
const port = 8080;

const supported = [
  "textShape",
  "javaScript",
  "javaScriptShape",
  "javaScriptDeformer",
  "javaScriptModifier",
  "javaScriptEmitter",
  "skslShader"
];

function setTextToLayer(layer, type, text) {
  switch (type) {
    case "javaScript":
    case "javaScriptDeformer":
    case "javaScriptEmitter":
    case "javaScriptModifier":
      api.set(layer, {"expression": text});
      break;
    case "javaScriptShape":
      api.set(layer, {"generator.expression": text});
      break;
    case "skslShader":
      api.set(layer, {"code": text});
      break;
    case "textShape":
      api.set(layer, {"text": text});
      break;
    default:
      console.error("Unsupported layer type");
  }
}

function performAction(data) {
  switch (data.action) {
    case "default":
    case "set_to_selected_layers": {
      let selection = api.getSelection();
      selection.forEach(function (layer) {
        let type = api.getLayerType(layer);
        if (supported.includes(type)) {
          setTextToLayer(layer, type, data.text);
        }
      });
      break;
    }
    case "set_to_layer_id": {
      let layer = data.layer_id;
      if (api.layerExists(layer)) {
        setTextToLayer(layer, api.getLayerType(layer), data.text);
      } else {
        console.warn("Layer " + layer + " does not exist");
      }
      break;
    }
    case "create_new_layer_type": {
      let layer = api.create(data.layer_type);
      setTextToLayer(layer, data.layer_type, data.text);
      console.log("Created Layer: " + layer);
      break;
    }
    case "execute_script": {
      api.exec("sendToCavalryScript", "(function () {\n" + data.text + "\n})()");
      break;
    }
    case "run_file_script_path": {
      if (api.filePathExists(data.script_path)) {
        ui.runFileScript(data.script_path);
      } else {
        console.error("Script file not found: " + data.script_path);
      }
      break;
    }
    default: {
      console.error("Unknown action requested");
    }
  }
}

function Callbacks() {
  this.onPost = function () {
    while (server.postCount()) {
      let post = server.getNextPost();
      let data = JSON.parse(post.result);

      if (data.source === "sendToCavalryScript") {
        performAction(data);
      } else {
        console.error("Received data from an unknown source");
      }
    }
  }
}

let server = new api.WebServer();
let callback_object = new Callbacks();

server.listen(host, port);
server.addCallbackObject(callback_object);
server.setHighFrequency();

let label = new ui.Label("Server is running…");
label.setAlignment(1);

ui.showContextMenuOnRightClick();
ui.addMenuItem({
  name: "Open GitHub Page",
  onMouseRelease: function () {
    api.openURL("https://github.com/yevgenymakarov/sublime-send-to-cavalry");
  }
});

ui.add(label);
ui.setTitle("Receiver");
ui.show();
