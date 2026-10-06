import streamlit as st
from starter import ZONES, TIME_BLOCKS, COSTS, PROMISE, delivery_times


# Block 1: count late orders and all orders for one zone-time block pair
def late_one(zone,time_block,promise):
  # get the delivery times of all orders in this pair
  times=delivery_times(zone,time_block,promise,seed=1)
  # put orders longer than the promise into the late list
  late=[]
  for t in times:
    if t>promise:
      late.append(t)
  # return the number of late orders and the number of all orders
  return len(late),len(times)


# Total cost of one late order
def cost_per_late(costs):
  # direct cost: the refund given to the customer
  refund=costs["refund"]
  # churn cost: future orders lost x profit per order
  churn_cost=costs["churn_orders"]*costs["margin"]
  return refund+churn_cost


# Net profit of one zone-time block pair for one promise
def net_profit(zone,time_block,promise,costs):
  # number of late orders and all orders
  n_late,n_orders=late_one(zone,time_block,promise)
  # profit from all orders minus the cost of late orders
  profit=n_orders*costs["margin"]-n_late*cost_per_late(costs)
  return n_orders,n_late,profit


# Find the promise with the highest net profit
def best_promise(zone,time_block,promises,costs):
  # step 1: try every promise and save its net profit
  profits=[]
  for p in promises:
    n_orders,n_late,profit=net_profit(zone,time_block,p,costs)
    profits.append(profit)
  # step 2: find the highest net profit and its promise
  best_profit=max(profits)
  best_p=promises[profits.index(best_profit)]
  return best_p,best_profit


# ---------------- Streamlit UI ----------------
st.set_page_config(page_title="Rosa's Delivery Promise",layout="centered")
st.title("Rosa's Delivery Promise Helper")
st.write("Find the promised delivery time that gives Rosa the highest net profit.")

# zone and time block side by side
col1,col2=st.columns(2)
with col1:
  zone=st.selectbox("Zone",ZONES)
with col2:
  time_block=st.selectbox("Time block",TIME_BLOCKS)

# range of promises to try
col1,col2=st.columns([3,1])
with col1:
  shortest,longest=st.slider("Promise range (minutes)",5,120,(20,75),step=5)
with col2:
  step=st.slider("Step",1,15,5)

# costs in one row, same keys as COSTS
st.subheader("Costs")
col1,col2,col3=st.columns(3)
with col1:
  refund=st.number_input("Refund per late order ($)",value=float(COSTS["refund"]))
with col2:
  churn=st.number_input("Lost future orders per late order",value=float(COSTS["churn_orders"]))
with col3:
  margin=st.number_input("Profit margin per order ($)",value=float(COSTS["margin"]))
costs={"refund":refund,"churn_orders":churn,"margin":margin}

if st.button("Find the best promise",type="primary",width="stretch"):
  # check the inputs
  if shortest<=0 or shortest>=longest:
    st.error("The shortest promise must be greater than 0 and smaller than the longest promise.")
  else:
    promises=list(range(shortest,longest+1,step))
    best_p,best_profit=best_promise(zone,time_block,promises,costs)
    # net profit with today's promise, to compare
    today_orders,today_late,today_profit=net_profit(zone,time_block,PROMISE,costs)
    # build one table row for every promise
    rows=[]
    for p in promises:
      n_orders,n_late,profit=net_profit(zone,time_block,p,costs)
      rows.append({
        "Promise (minutes)":p,
        "Orders":n_orders,
        "Late orders":n_late,
        "Late rate (%)":round(n_late/n_orders*100,1) if n_orders>0 else 0.0,
        "Net profit ($)":round(profit,2),
      })
    # save the result so it stays on the page
    st.session_state["result"]={
      "zone":zone,
      "time_block":time_block,
      "best_p":best_p,
      "best_profit":best_profit,
      "difference":best_profit-today_profit,
      "edge":best_p==promises[0] or best_p==promises[-1],
      "rows":rows,
    }

# show the saved result until the button is clicked again
result=st.session_state.get("result")
if result:
  st.subheader(f"{result['zone']} during {result['time_block']}")
  col1,col2,col3=st.columns(3)
  col1.metric("Best promise (minutes)",result["best_p"])
  col2.metric("Net profit at best promise ($)",f"{result['best_profit']:.2f}")
  col3.metric(f"Difference vs today's {PROMISE}-minute promise ($)",f"{result['difference']:+.2f}")
  # warn if the best promise is at the edge of the range
  if result["edge"]:
    st.warning("The best promise is at the edge of the range, so the range should be wider.")
  st.line_chart(result["rows"],x="Promise (minutes)",y="Net profit ($)")
  st.dataframe(result["rows"],hide_index=True,column_config={"Net profit ($)":st.column_config.NumberColumn(format="%.2f")})
