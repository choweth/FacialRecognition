from app import app

@app.route('/')
def atHome():
	return "You have reached the home page for the 'I know that face' project!"

