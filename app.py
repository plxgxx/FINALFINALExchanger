import datetime
import os
import uuid

from flask import Flask, request, session, render_template
import models
from models import User, Transac, Review, Deposit, Currency, Account
import database
import sqlalchemy
from celery_worker import task1


app = Flask(__name__)
app.secret_key = 'ag0df9g-09s0-f9-a09d-09a-s0d'
date_now = datetime.datetime.now().strftime("%d-%m-%Y")










# homepage
@app.route("/")
def Homepage():
    return "<p>Hello! This is the homepage</p>"


@app.route('/currency/list', methods=['GET'])#Works
def Currency_List():
    database.init_db()
    result = Currency.query.all()
    return [itm.to_dict() for itm in result]


# 2page
@app.route('/currency/<currency_name>', methods=['GET'])#Works
def currency_info(currency_name):
    database.init_db()
    res = Currency.query.filter_by(CurrencyName=currency_name)
    return [itm.to_dict() for itm in res]



# 5page
@app.route('/user', methods=['GET', 'POST'])#works
def get_user_info():
    database.init_db()
    if request.method == 'GET':
        user_id = session.get('user_id')
        if user_id is None:
            return '''
            <html>
            <form method="post"> 
  <div class="container">
    <label for="uname"><b>User id</b></label>
    <input type="text" placeholder="Enter User id" name="uname" required>

    <label for="psw"><b>Password</b></label>
    <input type="password" placeholder="Enter Password" name="psw" required>

    <button type="submit">Login</button>
  </div>
</form>
            </html>
            '''
        else:
            result = models.Account.query.filter_by(User_id = user_id).all()
            if len(result) == 0:
                return "No such user!"
            return [itm.to_dict() for itm in result]
    if request.method == 'POST':
        user_id = request.form.get('uname')
        user_password = request.form.get('psw')
        user_info = models.User.query.filter_by(id=user_id, password=user_password).first()
        if user_info:
            session['user_id'] = user_id
            return "Succsess"
        else:
            return "Error"



@app.route('/currency/<currency_name>/rating', methods = ['GET', 'POST'])#works
def add_currency_rating(currency_name):
    database.init_db()
    if request.method == 'POST':
        request_data = request.get_json()
        rating = request_data['Rating']
        comment = request_data['Comment']
        rating_piece = Review(CurrencyName=currency_name, Rating=rating, Comment=comment)
        database.db_session.add(rating_piece)
        database.db_session.commit()
        return "ok!"
    else:
        all_ratings = Review.query.all()
        currency_rating = dict(
            database.db_session.query(
                sqlalchemy.func.avg(models.Review.Rating).label('rate')
            ).filter(
                models.Review.CurrencyName == currency_name
            ).first()
        )['rate']
        rate_history = [itm.to_dict() for itm in all_ratings]
        return {"Rate_History": rate_history, "average": currency_rating, "currency_name": currency_name}


@app.get('/currency/trade/<currency_name1>x<currency_name2>')#Works
def init_transac(currency_name1, currency_name2):
    if session.get('user_id') is not None:
        return '''
                <html>
                <form method="post"> 
      <div class="container">
        <label for="uname"><b>Amount of Currency</b></label>
        <input type="text" placeholder="Enter Value" name="amount1" required>
       
        <button type="submit">Submit</button>
      </div>
    </form>
                </html>
                '''
    else:
        return "Login required"
@app.post('/currency/trade/<currency_name1>x<currency_name2>')#Works
def exchange(currency_name1, currency_name2):
    user_id = session.get('user_id')
    amount1 = float(request.form.get('amount1'))
    OperType = "Transfer"
    fee = 0



    transaction_id = str(uuid.uuid4())
    database.init_db()
    transaction_queue_record = models.TransactionQueue(transaction_id=str(transaction_id), status="in queue")
    database.db_session.add(transaction_queue_record)
    database.db_session.commit()



    task_obj = task1.apply_async(args=[user_id, currency_name1, currency_name2, amount1, OperType, fee, transaction_id])
    return {'task id': str(task_obj)}





if __name__ == '__main__':
    app.run(host='0.0.0.0')
