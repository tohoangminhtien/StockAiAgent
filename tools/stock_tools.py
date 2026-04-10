import sys
from langchain.tools import StructuredTool
import inspect
from typing import Optional
from vnstock import Vnstock
from rapidfuzz import process, fuzz
from datetime import date
from tools.train_model import predict_stock


def check_symbol(user_input: str):
    '''
    Checks if the given stock symbol exists. 

    If the symbol is correct, it returns a confirmation message. 
    Otherwise, it suggests up to 5 similar company names with their stock codes.
    Args:
        user_input: stock code symbol
    '''
    stock = Vnstock().stock(source='VCI')
    symbol = stock.listing.all_symbols()['ticker'].tolist()
    if user_input in symbol:
        return f"{user_input} stock code correct"
    else:
        name = stock.listing.all_symbols()['organ_name'].tolist()
        matches = process.extract(user_input, name, scorer=fuzz.ratio, limit=5)
        s = ""
        for i in matches:
            s += f"{i[0]} {symbol[name.index(i[0])]}\n"
        return s


def get_stock_price(symbol: Optional[str] = None, date: Optional[str] = None):
    '''Tool to look up stock information of a certain symbol object.

    Args:
        symbol: stock code symbol
        date: date to look up, format YYYY-MM-DD
    '''
    stock = Vnstock().stock(symbol=symbol, source='TCBS')
    df = stock.quote.history(start="2025-01-01", end=date)
    return df[df['time'] == date]


def company_infomation(symbol: Optional[str] = None):
    '''
    Retrieve company information based on the given stock symbol.

    Args:
        symbol: The stock symbol of the company.
    '''
    company = Vnstock().stock(symbol=symbol, source='TCBS').company
    return str(company.overview()) + '/n' + str(company.profile())


def get_today():
    '''
    Get the current date.

    Returns:
        date: Today's date in the format YYYY-MM-DD.
    '''
    return date.today()


# def company_shareholders(symbol: Optional[str] = None):
#     '''
#     Retrieve shareholder information for a given company.

#     Args:
#         symbol: The stock symbol of the company.
#     '''
#     company = Vnstock().stock(symbol=symbol, source='TCBS').company
#     return company.shareholders()


# def company_subsidiaries(symbol: Optional[str] = None):
#     '''
#     Retrieve subsidiaries information for a given company.

#     Args:
#         symbol: The stock symbol of the company.
#     '''
#     company = Vnstock().stock(symbol=symbol, source='TCBS').company
#     return company.subsidiaries()


def predict_tomorrow(symbol: str):
    '''
    Predict the next day's stock price of a given company.

    Args:
        symbol (str): The company's stock symbol.
    '''
    return predict_stock(symbol)


def fallback_tool() -> str:
    """
    This tool is used when no other tools are applicable.
    It returns a default response indicating that the agent cannot answer.
    """
    return "I don't know"


def get_tools():
    tools = []
    current_module = sys.modules[__name__]

    for name, func in inspect.getmembers(current_module, inspect.isfunction):
        if func.__module__ == __name__ and name != "get_tools":
            tools.append(StructuredTool.from_function(func))

    return tools
