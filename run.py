# import the necessary packages

from app import create_app 

# instantiate the app run method
app = create_app()


@app.cli.command()
def deploy():
    app.run(debug=True)