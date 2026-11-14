"""Forecast monthly revenue and order counts using linear trend models."""
import json, numpy as np, pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error,mean_squared_error
from src.config import PROCESSED,get_engine
def _forecast(series):
 y=series.astype(float).to_numpy(); x=np.arange(len(y)).reshape(-1,1); split=max(2,int(len(y)*.8)); model=LinearRegression().fit(x[:split],y[:split]); pred=model.predict(x[split:]); mae=float(mean_absolute_error(y[split:],pred)) if len(pred) else 0.0; rmse=float(np.sqrt(mean_squared_error(y[split:],pred))) if len(pred) else 0.0; final=LinearRegression().fit(x,y); future=final.predict(np.arange(len(y),len(y)+3).reshape(-1,1)); return future,mae,rmse
def main():
 e=get_engine(); df=pd.read_sql("SELECT order_date,order_status,order_id FROM fact_orders",e); df["month"]=pd.to_datetime(df.order_date).dt.to_period("M").astype(str); counts=df[~df.order_status.isin(["cancelled","returned"])].groupby("month").order_id.nunique().sort_index(); items=pd.read_sql("SELECT order_id,line_revenue FROM fact_order_items",e); rev=df.merge(items,on="order_id"); rev=rev[~rev.order_status.isin(["cancelled","returned"])].groupby("month").line_revenue.sum().reindex(counts.index,fill_value=0)
 r,mae_r,rmse_r=_forecast(rev); o,mae_o,rmse_o=_forecast(counts); last=pd.Period(counts.index[-1],freq="M"); months=[str(last+i) for i in range(1,4)]
 out={"method":"Linear trend regression with chronological 80/20 holdout evaluation","monthly_revenue":{"historical":dict(zip(rev.index,rev.round(2).tolist())),"forecast":dict(zip(months,np.maximum(0,r).round(2).tolist())),"mae":mae_r,"rmse":rmse_r},"monthly_orders":{"historical":dict(zip(counts.index,counts.astype(int).tolist())),"forecast":dict(zip(months,np.maximum(0,o).round().astype(int).tolist())),"mae":mae_o,"rmse":rmse_o},"limitations":"Short synthetic history, linear trend cannot capture seasonality or structural changes; forecasts are illustrative and depend on seed/configuration."}
 (PROCESSED/"forecast.json").write_text(json.dumps(out,indent=2)); print(json.dumps(out,indent=2))
if __name__=="__main__": main()
