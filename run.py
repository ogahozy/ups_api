# import the necessary packages

from app import create_app,db
from app.model import User, Task

# instantiate the app run method
app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Task': Task}


@app.cli.command()
def deploy():
    app.run(debug=False)