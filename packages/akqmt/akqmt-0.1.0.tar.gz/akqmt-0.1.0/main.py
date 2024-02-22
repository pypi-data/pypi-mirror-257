from akqmt import xt_api

pro = xt_api()
temp_df = pro.get_instrument_detail(stock_code="000001.SZ")
print(temp_df)
