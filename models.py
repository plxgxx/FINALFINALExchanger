from sqlalchemy import Column, Integer, String, REAL
from database import Base




class User(Base):
    __tablename__ = 'user'
    login = Column(String(50), nullable = False)
    id = Column(Integer, primary_key = True, nullable = False)
    password = Column(String(20), nullable = False)

    def __repr__(self):
        return '<User %r>' %self.login
    def to_dict(self):
        return {
            'login': self.login,
            'id': self.id,
            'password': self.password
        }

class Transac(Base):
    __tablename__ = 'transaction'
    id = Column(Integer, primary_key = True, nullable = False)
    User = Column(String(50), nullable = False)
    OperationType = Column(String(20), nullable = False)
    AmountofGivenCurrency = Column(REAL, nullable = False)
    CurrencyTypeofGivingOper = Column(String(50), nullable = False)
    CurrencyTypeofRecievingOper = Column(String(50), nullable = False)
    DateTime = Column(String(10), nullable = False)
    AmountofRecievedCurrency = Column(REAL, nullable=False)
    Fee = Column(REAL, nullable=False)
    BalanceofGivingOper = Column(Integer, nullable=False)
    BalanceofRecievingOper = Column(Integer, nullable=False)

    def __repr__(self):
        return '<Transac %r>' % self.id

    def to_dict(self):
        return {
            'id': self.id,
            'User': self.User,
            'OperationType': self.OperationType,
            'AmountofGivenCurrency': self.AmountofGivenCurrency,
            'CurrencyTypeofGivingOper': self.CurrencyTypeofGivingOper,
            'CurrencyTypeofRecievingOper': self.CurrencyTypeofRecievingOper,
            'DateTime': self.DateTime,
            'AmountofRecievedCurrency': self.AmountofRecievedCurrency,
            'Fee': self.Fee,
            'BalanceofGivingOper': self.BalanceofGivingOper,
            'BalanceofRecievingOper': self.BalanceofRecievingOper
        }

class Review(Base):
    __tablename__ = 'reviews'
    id = Column(Integer, primary_key = True, nullable = False)
    CurrencyName = Column(String(20), nullable = False)
    Rating = Column(REAL,nullable = False)
    Comment = Column(String(100))

    def __repr__(self):
        return '<Review %r>' % self.id

    def to_dict(self):
        return {
            'id': self.id,
            'CurrencyName': self.CurrencyName,
            'Rating': self.Rating,
            'Comment': self.Comment
        }

class Deposit(Base):
    __tablename__ = 'deposits'
    DateofOpening = Column(String(10), nullable = False)
    DateofClosing = Column(String(10))
    DepositBalance = Column(Integer,nullable = False)
    InterestRate = Column(REAL, nullable = False)
    TermsofDeposit = Column(String, nullable = False)
    id = Column(String, primary_key=True, nullable = False)
    def __repr__(self):
        return '<Deposit %r>' % self.id


    def to_dict(self):
        return {
            'DateofOpening': self.DateofOpening,
            'DateofClosing': self.DateofClosing,
            'DepositBalance': self.DepositBalance,
            'InterestRate': self.InterestRate,
            'TermsofDeposit': self.TermsofDeposit,
            'id': self.id
        }

class Currency(Base):
    __tablename__ = 'currencys'
    CurrencyName = Column(String(15),nullable = False)
    NameToUSDPrice = Column(REAL,nullable = False)
    Amount  = Column(REAL, nullable = False)
    Date = Column(String(10), nullable = False)
    id = Column(Integer, primary_key = True, nullable = False)

    def __repr__(self):
        return '<Currency %r>' % self.CurrencyName

    def to_dict(self):
        return {
            'CurrencyName': self.CurrencyName,
            'NameToUSDPrice': self.CurrencyName,
            'Amount': self.Amount,
            'Date': self.Date
        }
class Account(Base):
    __tablename__ = 'accounts'
    User_id = Column(Integer, nullable = False)
    id = Column(Integer, primary_key = True, nullable = False)
    balance = Column(REAL, nullable = False)
    CurrencyName = Column(String(15), nullable = False)

    def __repr__(self):
        return '<Account %r>' % self.id

    def to_dict(self):
        return {
            'User_id': self.User_id,
            'id': self.id,
            'balance': self.balance,
            'CurrencyName': self.CurrencyName
        }

class TransactionQueue(Base):
    __tablename__ = 'Transaction_Queue'
    id = Column(Integer, primary_key = True, nullable = False)
    transaction_id = Column(String(50), nullable = False)
    status = Column(String(50), nullable = False)
