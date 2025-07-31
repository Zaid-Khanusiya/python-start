from flask import Flask,redirect,url_for,request,render_template
app = Flask(__name__)
upload_path = '/Users/-----------/Zaid/Downloads/Python Office/upload_files/'

@app.route('/')
def home():
    return "Hello, World! This is my Flask made site. This is the home page of my website."

@app.route('/user/<username>')
def show_user(username):
    return f'Hello {username}!'

@app.route('/post/<int:id>')
def show_post(id):
    return f'This post has the id {id}'

@app.route('/skills')
def skills():
    return """<h2>My skills are:</h2>
        <p>1) Python</p>
        <p>2) MySQL & MongoDB</p>
        <p>3) Flask, Django & FastAPI</p>
    """

@app.route('/contact')
def contact():
    return "<h2>Contact me at:</h2><h3>zaid.k@example.com</h3>"

@app.route("/hello/<username>")
def greet_user(username):
    return f"<h1>Hello, {username.capitalize()}!</h1>"

@app.route("/login", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form["name"]
        return redirect(url_for("greet_user", username=name))
    else:
        return render_template("login.html")
    
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file.filename == '':
            return "Please Select File!"
        file.save(upload_path + file.filename)
        return 'File uploaded!'
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(port=5001,debug=True)