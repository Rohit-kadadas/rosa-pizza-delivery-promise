import streamlit as st

from starter import COSTS, TIME_BLOCKS, ZONES, delivery_times


def cost_per_late_order(refund_cost, churn_orders, profit_margin):
	return refund_cost + churn_orders * profit_margin


def best_promise(
	zone,
	time_block,
	minimum_promise,
	maximum_promise,
	promise_increment,
	profit_margin,
	churn_orders,
	refund_cost,
):
	if minimum_promise <= 0 or maximum_promise <= 0:
		raise ValueError("Promised delivery times must be positive.")
	if maximum_promise < minimum_promise:
		raise ValueError("Maximum promise must be at least the minimum promise.")
	if promise_increment <= 0:
		raise ValueError("Promise increment must be positive.")

	late_order_cost = cost_per_late_order(
		refund_cost, churn_orders, profit_margin
	)
	results = []
	for promise in range(
		minimum_promise, maximum_promise + 1, promise_increment
	):
		times = delivery_times(zone, time_block, promise=promise, seed=1)
		order_count = len(times)
		late_order_count = sum(bool(time > promise) for time in times)
		total_profit = order_count * profit_margin
		total_late_order_cost = late_order_count * late_order_cost
		results.append(
			{
				"Promised delivery (min)": promise,
				"Orders": order_count,
				"Late orders": late_order_count,
				"Total profit ($)": total_profit,
				"Late-order costs ($)": total_late_order_cost,
				"Net profit ($)": total_profit - total_late_order_cost,
			}
		)

	return max(results, key=lambda result: result["Net profit ($)"]), results


st.set_page_config(page_title="Rosa's Pizza | Delivery Promise", page_icon="🍕")
st.title("Rosa's Pizza delivery promise")
st.caption(
	"Find the promised delivery time with the highest estimated net profit "
	"for a four-week simulation."
)

with st.form("promise_analysis"):
	zone_col, time_col = st.columns(2)
	with zone_col:
		zone = st.selectbox("Delivery zone", ZONES)
	with time_col:
		time_block = st.selectbox("Time block", TIME_BLOCKS)

	st.subheader("Promise range")
	min_col, max_col, increment_col = st.columns(3)
	with min_col:
		minimum_promise = st.number_input(
			"Minimum (minutes)", min_value=1, value=30, step=1
		)
	with max_col:
		maximum_promise = st.number_input(
			"Maximum (minutes)", min_value=1, value=60, step=1
		)
	with increment_col:
		promise_increment = st.number_input(
			"Increment (minutes)", min_value=1, value=5, step=1
		)

	st.subheader("Order economics")
	margin_col, churn_col, refund_col = st.columns(3)
	with margin_col:
		profit_margin = st.number_input(
			"Profit margin per order ($)",
			min_value=0.0,
			value=float(COSTS["margin"]),
			step=0.5,
			format="%.2f",
		)
	with churn_col:
		churn_orders = st.number_input(
			"Churn orders per late order",
			min_value=0.0,
			value=float(COSTS["churn_orders"]),
			step=0.1,
			format="%.1f",
		)
	with refund_col:
		refund_cost = st.number_input(
			"Refund cost per late order ($)",
			min_value=0.0,
			value=float(COSTS["refund"]),
			step=0.5,
			format="%.2f",
		)

	calculate = st.form_submit_button("Calculate recommended promise")

if calculate:
	try:
		recommendation, results = best_promise(
			zone,
			time_block,
			int(minimum_promise),
			int(maximum_promise),
			int(promise_increment),
			profit_margin,
			churn_orders,
			refund_cost,
		)
	except ValueError as error:
		st.error(str(error))
	else:
		st.subheader("Recommendation")
		promise_col, profit_col = st.columns(2)
		promise_col.metric(
			"Recommended promise",
			f'{recommendation["Promised delivery (min)"]} minutes',
		)
		profit_col.metric("Maximum net profit", f'${recommendation["Net profit ($)"]:,.2f}')
		st.dataframe(results, hide_index=True, use_container_width=True)
		st.caption(
			"Each simulated late order costs the refund plus the estimated "
			"profit lost to churn. Orders and delivery times are simulated "
			"with seed=1 for each promise."
		)
