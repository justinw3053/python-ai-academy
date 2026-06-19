import os
from flask import Flask, jsonify, send_from_directory, request, Response
import backend.state_manager as state_manager
import backend.llm_bridge as llm_bridge
import backend.content_engine as content_engine

def create_app(test_config=None):
    # create and configure the app, pointing static to the frontend folder
    app = Flask(__name__, instance_relative_config=True, static_folder="../frontend", static_url_path="")

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.after_request
    def add_security_headers(response):
        response.headers['Cross-Origin-Opener-Policy'] = 'same-origin'
        response.headers['Cross-Origin-Embedder-Policy'] = 'require-corp'
        return response

    @app.route('/')
    def index():
        return app.send_static_file('index.html')

    @app.route('/api/health')
    def health():
        return jsonify({"status": "ok"})

    @app.route('/api/lessons')
    def lessons():
        return jsonify(content_engine.list_lessons())

    @app.route('/api/lessons/<lesson_id>')
    def lesson_detail(lesson_id):
        content = content_engine.get_lesson_content(lesson_id)
        if content is None:
            return jsonify({"error": "Lesson not found"}), 404
        return jsonify(content)
        
    @app.route('/api/track', methods=['POST'])
    def track():
        data = request.json
        if not data or 'lesson' not in data:
            return jsonify({"error": "Bad Request"}), 400
            
        success = state_manager.update_progress(data['lesson'])
        return jsonify({"status": "updated", "success": success})

    @app.route('/api/chat', methods=['POST'])
    def chat():
        data = request.json
        if not data or 'message' not in data:
            return jsonify({"error": "Bad Request"}), 400
            
        message = data['message']
        context = data.get('context', '')
        lesson_id = data.get('lessonId', '')
        
        return Response(llm_bridge.stream_chat(message, context, lesson_id), mimetype='text/event-stream')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(threaded=True, host='127.0.0.1', port=5000)
