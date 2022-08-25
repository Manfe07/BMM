from flask import Blueprint, render_template, Flask, request, jsonify, redirect, url_for, session, flash
import statistics.datahandler as datahandler
import cashRegister.datahandler as cashRegister_datahandler
from pprint import pprint


def addButtons(buttonList : dict):
    buttonList['2'].append({
        'text' : "Statistik",
        'class' : "btn btn-warning",
        'site' : 'statistics.overview'
    })
    return buttonList


statistics = Blueprint('statistics', __name__,
                        template_folder='templates')


@statistics.route('/', methods=['GET'])
@statistics.route('/uebersicht', methods=['GET'])
def overview():
    if session.get("logged_in") and session.get("permission") >= 2:
        data = {}
        data["artikel"] = datahandler.getOrderOverview()
        data["biermeter"] = cashRegister_datahandler.get_List_By_Date()
        return render_template("statistics/overview.html", data = data)
    else:
        return redirect(url_for('user.login'))