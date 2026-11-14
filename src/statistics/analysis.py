"""Run hypothesis testing, correlation and interpretable regression."""
import json, pandas as pd
from scipy.stats import ttest_ind,pearsonr
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error,r2_score
from src.config import PROCESSED,get_engine
def main():
 e=get_engine(); orders=pd.read_sql("SELECT * FROM fact_orders",e); items=pd.read_sql("SELECT order_id,SUM(line_revenue) revenue FROM fact_order_items GROUP BY order_id",e); d=orders.merge(items,on="order_id"); d=d[d.order_status!="cancelled"]
 promo=d[d.promotion_applied==1].revenue; no_promo=d[d.promotion_applied==0].revenue; stat,p=ttest_ind(promo,no_promo,equal_var=False)
 delivery=pd.read_sql("SELECT promised_delivery_date,actual_delivery_date,customer_rating FROM fact_deliveries",e); delay=(pd.to_datetime(delivery.actual_delivery_date)-pd.to_datetime(delivery.promised_delivery_date)).dt.days; corr,cp=pearsonr(delay,delivery.customer_rating)
 features=d[["promotion_applied"]].copy(); features["order_month"]=pd.to_datetime(d.order_date).dt.month; features["item_count"]=d.order_id.map(pd.read_sql("SELECT order_id,COUNT(*) cnt FROM fact_order_items GROUP BY order_id",e).set_index("order_id").cnt).fillna(0); X=features.fillna(0); y=d.revenue
 Xtr,Xte,ytr,yte=train_test_split(X,y,test_size=.2,random_state=42); model=LinearRegression().fit(Xtr,ytr); pred=model.predict(Xte)
 out={"promotion_welch_t_test":{"h0":"Promotion does not affect mean order revenue (proxy for AOV when order item totals are used).","h1":"Promotion changes mean order revenue.","alpha":0.05,"n_promotion":int(len(promo)),"n_no_promotion":int(len(no_promo)),"mean_promotion":float(promo.mean()),"mean_no_promotion":float(no_promo.mean()),"t_statistic":float(stat),"p_value":float(p),"significant":bool(p<.05),"interpretation":"Association only; this observational synthetic comparison does not establish causality."},"delivery_delay_rating_pearson":{"n":int(len(delivery)),"correlation":float(corr),"p_value":float(cp),"interpretation":"Correlation does not imply causation."},"revenue_regression":{"features":list(X.columns),"target":"order item revenue per order","coefficients":dict(zip(X.columns.tolist(),model.coef_.tolist())),"intercept":float(model.intercept_),"mae":float(mean_absolute_error(yte,pred)),"r2":float(r2_score(yte,pred)),"limitations":"Synthetic data, limited predictors, random holdout, and no causal interpretation."}}
 (PROCESSED/"statistical_analysis.json").write_text(json.dumps(out,indent=2)); print(json.dumps(out,indent=2))
if __name__=="__main__": main()
