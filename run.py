# import the necessary packages

from app import create_app,db
from flask_migrate import Migrate, upgrade
from app.model import Users, Task

# instantiate the app run method
app = create_app()
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Users': Users, 'Task': Task}

@app.cli.command()
def deploy():
    """Run deployment tasks."""
    # migrate database to latest revision
    upgrade()
