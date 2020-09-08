from flask import Flask

from helloworld.settings import (
    TEMPLATES_DIR,
    PROJECT_HOST,
    PROJECT_PORT,
    PROJECT_SECRET,
)
from helloworld.routes import (
    index,
    login,
    login_callback,
    logout,
    show_measurement_list,
    show_measurement_summary,
    show_ggo_list,
    show_ggo_summary,
    show_environment_declaration,
)


# -- Flask setup -------------------------------------------------------------

app = Flask(
    import_name='ProjectOriginHelloWorld',
    template_folder=TEMPLATES_DIR,
)

app.secret_key = PROJECT_SECRET
app.config['SESSION_COOKIE_NAME'] = 'session'


# -- Routes setup ------------------------------------------------------------

app.add_url_rule(
    rule='/',
    endpoint='index',
    view_func=index,
    methods=['GET', 'POST'],
)

app.add_url_rule(
    rule='/login',
    endpoint='login',
    view_func=login,
    methods=['GET', 'POST'],
)

app.add_url_rule(
    rule='/login/callback',
    endpoint='login-callback',
    view_func=login_callback,
    methods=['GET'],
)

app.add_url_rule(
    rule='/logout',
    endpoint='logout',
    view_func=logout,
    methods=['GET'],
)

app.add_url_rule(
    rule='/measurement-list',
    endpoint='measurement-list',
    view_func=show_measurement_list,
    methods=['GET'],
)

app.add_url_rule(
    rule='/measurement-summary',
    endpoint='measurement-summary',
    view_func=show_measurement_summary,
    methods=['GET'],
)

app.add_url_rule(
    rule='/ggo-list',
    endpoint='ggo-list',
    view_func=show_ggo_list,
    methods=['GET'],
)

app.add_url_rule(
    rule='/ggo-summary',
    endpoint='ggo-summary',
    view_func=show_ggo_summary,
    methods=['GET'],
)

app.add_url_rule(
    rule='/environment-declaration',
    endpoint='environment-declaration',
    view_func=show_environment_declaration,
    methods=['GET'],
)


if __name__ == '__main__':
    app.run(host=PROJECT_HOST, port=PROJECT_PORT)
