"""This program creates a webpage that has at least 3 pages for the user to navigate"""
from flask import Flask, render_template
app = Flask(__name__)


@app.route('/')
def main():
    """Maps the URL '/' to the main function, and builds the webpage
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
