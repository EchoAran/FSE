from flask import Flask, redirect, render_template, request, url_for
from app.game import *
import os


def create_app():
    app = Flask(__name__, template_folder='../templates', static_folder='../static')

    @app.before_request
    def ensure_state():
        if not hasattr(app, 'state'):
            state, warning = load_state()
            app.state = state
            app.warning = warning

    @app.route('/')
    def index():
        return render_template('index.html', state=app.state, warning=app.warning, levels=LEVELS)

    @app.route('/move/<direction>', methods=['POST'])
    def move(direction):
        app.warning = None
        app.state, err = apply_move(app.state, direction)
        if err:
            app.warning = err
        save_state(app.state)
        return redirect(url_for('index'))

    @app.route('/undo', methods=['POST'])
    def do_undo():
        app.state, err = undo(app.state)
        app.warning = err
        save_state(app.state)
        return redirect(url_for('index'))

    @app.route('/restart', methods=['POST'])
    def do_restart():
        app.state = restart(app.state)
        app.warning = None
        save_state(app.state)
        return redirect(url_for('index'))

    @app.route('/hint')
    def hint():
        app.warning = app.state['hint']
        return redirect(url_for('index'))

    @app.route('/progress')
    def progress():
        return render_template('progress.html', state=app.state)

    @app.route('/export', methods=['POST'])
    def export():
        detailed = request.form.get('detailed') == '1'
        try:
            path = export_stats(app.state, detailed=detailed)
            app.warning = f'Stats exported successfully to {path}'
        except Exception as e:
            app.warning = f'Stats export failed: {e}. The game continues normally.'
        return redirect(url_for('progress'))

    @app.route('/update-check')
    def update_check():
        if os.environ.get('QHEADACHE_UPDATE_AVAILABLE') == '1':
            app.warning = 'An important update is available. You can dismiss this and continue playing.'
        else:
            app.warning = 'Update check could not connect. Try again later.'
        return redirect(url_for('index'))

    return app
