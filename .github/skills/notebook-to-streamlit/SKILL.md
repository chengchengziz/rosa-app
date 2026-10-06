---
name: notebook-to-streamlit
description: Turn the analysis logic in a Jupyter notebook into a Streamlit app. Use this when building or updating app.py from rosa_assignment1.ipynb.
---

# Notebook to Streamlit

## Goal
Build a Streamlit app (app.py) that reuses the functions from the notebook, so the app gives the same results as the notebook.

## Steps
1. Read the notebook rosa_assignment1.ipynb. Find the functions the app needs: late_one, cost_per_late, net_profit and best_promise.
2. Copy these functions into app.py exactly as they are in the notebook. Do not change their logic, names or inputs.
3. Do not copy test cells, print statements, markdown text or the !pip install line.
4. Import the data from the starter package: from starter import ZONES, TIME_BLOCKS, COSTS, PROMISE, delivery_times. Never write your own version of ZONES, TIME_BLOCKS, COSTS, PROMISE or delivery_times.
5. Build the user interface:
   - set the page with st.set_page_config (page title, layout="centered"), then a clear title and one short sentence saying what the app does
   - a dropdown (st.selectbox) for the zone, using ZONES, and a dropdown for the time block, using TIME_BLOCKS, side by side with st.columns(2)
   - one range slider (st.slider with two handles) for the shortest and longest promise, from 5 to 120 minutes, default (20, 75), step 5; next to it a small slider for the step, from 1 to 15 minutes, default 5
   - under a small subheader "Costs", three number inputs in one row with st.columns(3): the refund per late order, the lost future orders per late order (churn) and the profit margin per order, with default values from COSTS
   - a primary button with full width (type="primary", width="stretch"); only after the button is clicked, call best_promise()
   - show the results with st.metric in three columns: the best promise (minutes), the net profit at the best promise ($), and the difference compared with today's promise PROMISE ($); save them in st.session_state so they stay on the page
   - under the results, a line chart of the net profit for every promise and a table (index hidden) with promise, orders, late orders, late rate (%) and net profit ($)
6. Build a costs dictionary from the user's inputs, with the same keys as COSTS ("refund", "churn_orders", "margin"), and pass it to best_promise().
7. Check the inputs: the shortest promise must be greater than 0 and smaller than the longest. If not, show st.error and do not run.
8. If the best promise is the first or the last value of the range, show st.warning saying the range should be wider.
9. Make sure requirements.txt contains streamlit, numpy and git+https://github.com/zhouy185/rosa-starter.git.
10. Test: with Far West, Fri/Sat eve, range 20 to 75 in steps of 5 and the default costs, the app must show 55 minutes and a net profit of 1212.40 dollars, the same as the notebook.

## Style
- Keep the code simple, at the level of an introductory Python course: functions, for loops, if/else, lists and dictionaries.
- Use 2-space indentation and no extra spaces around = and operators, the same style as the notebook.
- Write short English comments.
- Do not put any personal information in any file, because the repository may be public.
