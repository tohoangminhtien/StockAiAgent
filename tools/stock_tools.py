from agno.tools import tool
from vnstock import Listing
from rapidfuzz import distance


@tool
def check_symbol(input_symbol: str = None, input_company_name: str = None) -> str:
    # =========================
    # Validate input
    # =========================
    if bool(input_symbol) == bool(input_company_name):
        return "Please provide either input_symbol OR input_company_name (not both)."

    listing = Listing(source="KBS")
    df = listing.all_symbols()

    df["symbol"] = df["symbol"].astype(str).str.upper()
    df["organ_name"] = df["organ_name"].astype(str)

    symbol_to_name = dict(zip(df["symbol"], df["organ_name"]))
    name_to_symbol = dict(zip(df["organ_name"], df["symbol"]))

    # =========================
    # 🔍 SEARCH BY SYMBOL
    # =========================
    if input_symbol:
        normalized = input_symbol.strip().upper()

        # Exact match
        if normalized in symbol_to_name:
            return f"{normalized} stock code is valid."

        scored = []
        for sym in symbol_to_name:
            dist = distance.Levenshtein.distance(normalized, sym)

            # prefix boost
            bonus = 0
            if sym[:2] == normalized[:2]:
                bonus = -1
            elif sym[0] == normalized[0]:
                bonus = -0.5

            score = dist + bonus
            scored.append((sym, score))

        top = sorted(scored, key=lambda x: x[1])[:5]

        return "Symbol not found. Did you mean:\n" + "\n".join(
            f"{sym} - {symbol_to_name[sym]}" for sym, _ in top
        )

    # =========================
    # 🔍 SEARCH BY COMPANY NAME
    # =========================
    if input_company_name:
        query = input_company_name.strip().lower()

        scored = []
        for name in name_to_symbol:
            dist = distance.Levenshtein.distance(query, name.lower())
            scored.append((name, dist))

        top = sorted(scored, key=lambda x: x[1])[:5]

        return "Company not found. Did you mean:\n" + "\n".join(
            f"{name_to_symbol[name]} - {name}" for name, _ in top
        )


# @tool
# def get_stock_price(symbol: Optional[str] = None, date: Optional[str] = None):
#     """Tool to look up stock information of a certain symbol object.

#     Args:
#         symbol: stock code symbol
#         date: date to look up, format YYYY-MM-DD
#     """
#     stock = Vnstock().stock(symbol=symbol, source="TCBS")
#     df = stock.quote.history(start="2025-01-01", end=date)
#     return df[df["time"] == date]


# @tool
# def company_infomation(symbol: Optional[str] = None):
#     """
#     Retrieve company information based on the given stock symbol.

#     Args:
#         symbol: The stock symbol of the company.
#     """
#     company = Vnstock().stock(symbol=symbol, source="TCBS").company
#     return str(company.overview()) + "/n" + str(company.profile())


# @tool
# def get_today():
#     """
#     Get the current date.

#     Returns:
#         date: Today's date in the format YYYY-MM-DD.
#     """
#     return date.today()


# # def company_shareholders(symbol: Optional[str] = None):
# #     '''
# #     Retrieve shareholder information for a given company.

# #     Args:
# #         symbol: The stock symbol of the company.
# #     '''
# #     company = Vnstock().stock(symbol=symbol, source='TCBS').company
# #     return company.shareholders()


# # def company_subsidiaries(symbol: Optional[str] = None):
# #     '''
# #     Retrieve subsidiaries information for a given company.

# #     Args:
# #         symbol: The stock symbol of the company.
# #     '''
# #     company = Vnstock().stock(symbol=symbol, source='TCBS').company
# #     return company.subsidiaries()


# @tool
# def predict_tomorrow(symbol: str):
#     """
#     Predict the next day's stock price of a given company.

#     Args:
#         symbol (str): The company's stock symbol.
#     """
#     return predict_stock(symbol)


# @tool
# def fallback_tool() -> str:
#     """
#     This tool is used when no other tools are applicable.
#     It returns a default response indicating that the agent cannot answer.
#     """
#     return "I don't know"
