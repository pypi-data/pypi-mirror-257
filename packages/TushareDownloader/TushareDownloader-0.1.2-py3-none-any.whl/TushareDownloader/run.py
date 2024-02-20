"""
Run methods

run daily_run() to update daily data
run weekly_run() to update weekly data
run yearly_run() to update yearly data
run first_time_run() to update all data for the first time
"""

from .download import download_trading_calendar, download_stock_list
from .download import (update_stock_daily,
                       update_stock_weekly,
                       update_stock_monthly,
                       update_adj_factor,
                       update_cash_flow,
                       update_balance_sheet,
                       update_income_statement)



def daily_run() -> None:
    """Run daily update"""
    update_stock_daily()
    update_stock_weekly()
    update_stock_monthly()
    update_adj_factor()


def weekly_run() -> None:
    """Run weekly update"""
    update_cash_flow()
    update_balance_sheet()
    update_income_statement()


def yearly_run() -> None:
    """Run yearly update"""
    download_trading_calendar()
    download_stock_list()


def first_time_run() -> None:
    """Run first time update"""
    download_trading_calendar()
    download_stock_list()
    daily_run()
    weekly_run()
    yearly_run()
