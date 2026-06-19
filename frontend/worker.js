// worker.js
importScripts('./pyodide/pyodide.js');
let pyodideReadyPromise;
let inputBuffer = null;
let inputView = null;
async function loadPyodideAndPackages() {
  self.pyodide = await loadPyodide({indexURL: './pyodide/'});
  self.js_sync_input = function(promptText) {
      postMessage({ type: 'input_request', prompt: promptText });
      Atomics.wait(inputView, 0, 0);
      const strLen = inputView[1];
      const decoder = new TextDecoder();
      const stringBytes = new Uint8Array(inputBuffer, 8, strLen);
      const result = decoder.decode(stringBytes);
      inputView[0] = 0;
      return result;
  };
  await self.pyodide.runPythonAsync(`
import sys\nimport io\nimport builtins\nimport js\nimport ast\nimport types\nimport json
class CustomStdout(io.StringIO):\n    def write(self, string):\n        if string:\n            js.postMessage(json.dumps({"type": "stdout", "message": string}))\n        return super().write(string)
sys.stdout = CustomStdout()\nsys.stderr = CustomStdout()
def custom_input(prompt=""):\n    print(prompt, end="")\n    res = js.js_sync_input(prompt)\n    print(res)\n    return res
builtins.input = custom_input
def validate_ast(source_code, required_nodes):\n    if not required_nodes:\n        return True\n    try:\n        tree = ast.parse(source_code)\n    except SyntaxError as e:\n        raise ValueError(f"Syntax Error: {e}")\n    found_nodes = {type(node).__name__ for node in ast.walk(tree)}\n    for req in required_nodes:\n        if req not in found_nodes:\n            raise ValueError(f"Anti-Cheat: Required structure '{req}' missing.")\n    return True
tracker_mock = types.ModuleType('tracker')
exec("""
import js\nimport json
def update_progress(lesson):
    js.eval(f'''
        const xhr = new XMLHttpRequest();
        xhr.open("POST", "/api/track", false);
        xhr.setRequestHeader("Content-Type", "application/json");
        xhr.send(JSON.stringify({{lesson: "{lesson}"}}));
    ''')
""", tracker_mock.__dict__)
sys.modules["tracker"] = tracker_mock
_student_globals = {}
  `);
}
pyodideReadyPromise = loadPyodideAndPackages();
self.onmessage = async (event) => {
  await pyodideReadyPromise;
  if (event.data.type === 'init_buffer') {
      inputBuffer = event.data.buffer;
      inputView = new Int32Array(inputBuffer);
  } else if (event.data.type === 'run_code') {
      try {
          self.pyodide.globals.set('js_code', event.data.code);
          let reqs = event.data.required_ast || [];
          self.pyodide.globals.set('js_ast_reqs', reqs);
          await self.pyodide.runPythonAsync(`
validate_ast(js_code, list(js_ast_reqs))
_student_globals.clear()\n_student_globals['__builtins__'] = __builtins__\nexec(js_code, _student_globals)`);
          self.postMessage({type: 'execution_success'});
      } catch (e) { self.postMessage({type: 'execution_error', error: e.message}); }
  }
};
