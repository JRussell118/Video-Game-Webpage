"""This program adds logging for failed user logins, password resetting, and checks
if the passwords match any of the passwords from CommonPasswords.txt"""
import datetime
import socket
from flask import Flask, render_template, request, flash, send_from_directory
from passlib.hash import sha256_crypt
app = Flask(__name__, static_folder='C:\\Users\\jaden\\PycharmProjects\\Jaden_Russell_Lab7\\static')
app.secret_key = "Secret Flask Key"


def log_error():
    """Logs a failed login attempt error into the file"""
    with open('Error_Log.txt', 'a', encoding='utf-8') as file:
        host_ip = socket.gethostbyname(socket.gethostname())
        now_time = datetime.datetime.now()
        file.write(f"Failed Login Attempt on {now_time.strftime('%Y-%m-%d %H:%M:%S')} ")
        file.write(f"IP Address: {host_ip}\n")


def check_acc(user, p_word):
    """checks the username, then the password associated for validity"""
    with open('User_Accounts.txt', encoding='utf-8') as file:
        for line in file:
            if user == line.strip():
                line = file.readline()
                if sha256_crypt.verify(p_word, line.strip()):
                    return True
    return False


def change_pass(user, new_p):
    """Changes the password in old_p in User_Accounts.txt to the
    password in new_p"""
    with open('User_Accounts.txt', "r", encoding='utf-8') as file:
        file_data = file.readlines()
        file_length = len(file_data)
        for line in range(file_length):
            if user == file_data[line].strip():
                file_data[line+1] = sha256_crypt.hash(new_p)
    with open('User_Accounts.txt', "w", encoding='utf-8') as file:
        file.write(''.join(file_data))
        file.write('\n')


def check_pass(p_word):
    """Checks the password in p_word to make sure that it doesn't
    match any of the passwords in CommonPasswords.txt"""
    with open('CommonPassword.txt', "r", encoding='utf-8') as file:
        for line in file:
            if p_word == line.strip():
                return True
    return False


def pass_comp(p_word):
    """checks the complexity of the password and returns
    a boolean"""
    l_req = 0
    u_req = 0
    d_req = 0
    s_req = 0
    special_char = '!@#$%^&*()?/\\}{[]-_+=`~;:.,><'
    if len(p_word) >= 8:
        for letter in p_word:
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
        if not password:
            error = 'Please enter your Username.'
        elif not password:
            error = 'Please enter your Password.'
        elif check_pass(password):
            error = 'Your password is too common to be used securely.'
        elif check_reg(username):
            error = 'You are already registered.'
        elif not pass_comp(password):
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
            log_error()
        elif not password:
            error = 'Please enter your Password.'
            log_error()
        elif not check_reg(username):
            error = 'You are not a registered user.'
            log_error()
        elif not check_acc(username, password):
            error = 'Your username and password do not match your account.'
            log_error()
        else:
            return render_template('Title_Page.html')
    return render_template('User_Login.html', error=error)


@app.route('/Reset_Page', methods=['POST', 'GET'])
def reset():
    """Maps the URL '/User_Login' to the login function, and builds the webpage
    using the User_Login template"""
    error = None
    if request.method == 'POST':
        username = request.form['username']
        old_pass = request.form['old password']
        new_pass = request.form['new password']
        if not username:
            error = 'Please enter your Username.'
        elif not old_pass:
            error = 'Please enter your previous Password.'
        elif not new_pass:
            error = 'Please enter your new Password.'
        elif not check_acc(username, old_pass):
            error = 'Your username and password do not match your account.'
        elif check_pass(new_pass):
            error = 'Your password is too common to be used securely.'
        elif not pass_comp(new_pass):
            error = 'Your password should be more complex.'
        elif new_pass == old_pass:
            error = 'Your new password cannot be the same as your old one.'
        else:
            change_pass(username, new_pass)
            flash('Your password was reset.')
    return render_template('Reset_Page.html', error=error)


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
