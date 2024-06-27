"""This program creates a webpage that has at least 3 pages for the user to navigate"""
from flask import Flask, render_template, request, flash, send_from_directory
from passlib.hash import sha256_crypt
app = Flask(__name__, static_folder='C:\\Users\\jaden\\PycharmProjects\\Jaden_Russell_Lab7\\static')
app.secret_key = "Secret Flask Key"


def check_acc(user, p_word):
    """checks the username, then the password associated for validity"""
    with open('User_Accounts.txt', encoding='utf-8') as file:
        for line in file:
            if user == line.strip():
                line = file.readline()
                if sha256_crypt.verify(p_word, line.strip()):
                    return True
    return False


def check_pass(password):
    """checks the complexity of the password and returns
    a boolean"""
    l_req = 0
    u_req = 0
    d_req = 0
    s_req = 0
    special_char = '!@#$%^&*()?/\\}{[]-_+=`~;:.,><'
    if len(password) >= 8:
        for letter in password:
            if letter.isdigit():
                d_req += 1
            elif letter.islower():
                l_req += 1
            elif letter.isupper():
                u_req += 1
            elif letter in special_char:
                s_req += 1
        if s_req > 0 and u_req > 0 and l_req > 0 and d_req > 0:
            return True
    return False


def check_reg(name):
    """checks the file for the same registered username
    and returns a boolean"""
    with open('User_Accounts.txt', encoding='utf-8') as file:
        for line in file:
            if name == line.strip():
                return True
    return False


@app.route('/', methods=['POST', 'GET'])
def main():
    """Maps the URL '/' to the main function, and builds the webpage
        using the Register_Page template"""
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if not username:
            error = 'Please enter your Username.'
        elif not password:
            error = 'Please enter your Password.'
        elif check_reg(username):
            error = 'You are already registered.'
        elif not check_pass(password):
            error = 'Your password should be more complex.'
        else:
            with open('User_Accounts.txt', "a", encoding='utf-8') as file:
                file.write(username)
                file.write('\n')
                file.write(sha256_crypt.hash(password))
                file.write('\n')
            flash('Your account was successfully created!')
    return render_template('Register_Page.html', error=error)


@app.route('/User_Login', methods=['POST', 'GET'])
def login():
    """Maps the URL '/User_Login' to the login function, and builds the webpage
    using the User_Login template"""
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if not username:
            error = 'Please enter your Username.'
        elif not password:
            error = 'Please enter your Password.'
        elif not check_reg(username):
            error = 'You are not a registered user.'
        elif not check_acc(username, password):
            error = 'Your username and password do not match your account.'
        else:
            return render_template('Title_Page.html')
    return render_template('User_Login.html', error=error)


@app.route('/video-game-genres.svg', methods=['GET'])
def title_img():
    """creates a route for the image in the title page"""
    return send_from_directory("static", "video-game-genres.svg")


@app.route('/stardew-sim.jpg', methods=['GET'])
def sim_img():
    """creates a route for the image in the simulation page"""
    return send_from_directory("static", "stardew-sim.jpg")


@app.route('/livealive-rpg.jpg', methods=['GET'])
def rpg_img():
    """creates a route for the image in the rpg page"""
    return send_from_directory("static", "livealive-rpg.jpg")


@app.route('/villagersheroes-mmo.jpg', methods=['GET'])
def mmo_img():
    """creates a route for the image in the mmo page"""
    return send_from_directory("static", "villagersheroes-mmo.jpg")


@app.route('/Title_Page')
def title():
    """Maps the URL '/Title_Page' to the title function, and builds the webpage
    using the Title_Page template"""
    return render_template('Title_Page.html')


@app.route('/RPG_Page')
def rpg():
    """Maps the URL '/RPG_Page' to the rpg function, and builds the webpage
    using the RPG_Page template"""
    return render_template('RPG_Page.html')


@app.route('/Simulation_Page')
def sim():
    """Maps the URL '/Simulation_Page' to the sim function, and builds
    the webpage using the Simulation_Page template"""
    return render_template('Simulation_Page.html')


@app.route('/MMO_Page')
def mmo():
    """Maps the URL '/MMO_Page' to the mmo function, and builds
        the webpage using the MMO_Page template"""
    return render_template('MMO_Page.html')


if __name__ == '__main__':
    app.run()
