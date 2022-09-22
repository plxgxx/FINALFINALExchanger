import os
from celery import Celery
import datetime
import models
import database

app = Celery('celery_worker', broker=os.environ.get('RABBIT_CONNECTION_STR'))




@app.task
def task1(user_id, currency_name1, currency_name2, amount1, OperType, fee, transaction_id):
    date_now = datetime.datetime.now().strftime("%Y-%m-%d")

    database.init_db()
    transaction_record = models.TransactionQueue.query.filter_by(transaction_id=str(transaction_id)).first()

    user_balance1 = models.Account.query.filter_by(CurrencyName=currency_name1, User_id=user_id).first()
    act_currency1 = models.Currency.query.filter_by(CurrencyName=currency_name1, Date=date_now).first()
    act_currency2 = models.Currency.query.filter_by(CurrencyName=currency_name2, Date=date_now).first()

    needed_exchanger_balance = (amount1 * act_currency1.NameToUSDPrice / act_currency2.NameToUSDPrice)

    if act_currency2.Amount >= needed_exchanger_balance:
        if user_balance1.balance >= amount1:
            new_userbalance1 = user_balance1.balance - amount1
            models.Account.query.filter_by(User_id=user_id, CurrencyName=currency_name1).update(dict(balance=new_userbalance1))

            user_balance2 = models.Account.query.filter_by(CurrencyName=currency_name2, User_id=user_id).first()
            if user_balance2 is None:
                created_balance = models.Account(User_id=user_id, balance=needed_exchanger_balance,
                                          CurrencyName=currency_name2)
                database.db_session.add(created_balance)
            elif user_balance2 is not None:
                new_userbalance2 = user_balance2.balance + needed_exchanger_balance
                user_balance2.balance = new_userbalance2

            new_exchangerbalance2 = "{:.2f}".format(act_currency2.Amount - needed_exchanger_balance)
            act_currency2.Amount = new_exchangerbalance2

            new_exchangerbalance1 = act_currency1.Amount + amount1
            act_currency1.Amount = new_exchangerbalance1

            balance_value1 = user_balance1.balance
            balance_value2 = user_balance2.balance
            successfultransac = models.Transac(User=user_id, OperationType=OperType,
                                        AmountofGivenCurrency=amount1,
                                        CurrencyTypeofGivingOper=currency_name1,
                                        CurrencyTypeofRecievingOper=currency_name2,
                                        DateTime=date_now, AmountofRecievedCurrency=needed_exchanger_balance,
                                        Fee=fee, BalanceofGivingOper=balance_value1,
                                        BalanceofRecievingOper=balance_value2)
            database.db_session.add(successfultransac)
            transaction_record.status = 'done'
            database.db_session.add(transaction_record)
            database.db_session.commit()
            return "Successful transaction!"
        else:
            transaction_record.status = 'error'
            database.db_session.add(transaction_record)
            database.db_session.commit()
            return "Not enough funds on user balance"
    else:
        return "Not enough funds in exchanger"
        transaction_record.status = 'error'
        database.db_session.add(transaction_record)
        database.db_session.commit()