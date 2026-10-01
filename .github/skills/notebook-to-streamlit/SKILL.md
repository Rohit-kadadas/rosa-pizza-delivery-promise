# Notebook to Streamlit Skill

## Purpose

Convert the Rosa's Pizza delivery-promise analysis from the Python notebook into a Streamlit application.

## Required functionality

The Streamlit app must:

1. Allow the user to select a delivery zone.
2. Allow the user to select a time block.
3. Allow the user to specify the range of promised delivery times to test.
4. Allow the user to adjust:
   - Profit margin per order
   - Estimated churn orders per late order
   - Refund cost per late order
5. Calculate the cost associated with each late order.
6. Calculate net profit for every promised delivery time.
7. Identify the promised delivery time with the highest net profit.
8. Display the recommended promised delivery time after the user clicks a button.

## Notebook logic

The app should reuse the notebook's existing logic:

- `delivery_times()` generates simulated delivery times.
- An order is late when its delivery time exceeds the promised delivery time.
- Total late-order cost equals:
  refund cost + (churn orders × profit margin).
- Net profit equals:
  total profit from orders − total late-order costs.
- The recommended promise is the promise with the highest net profit.

## Reproducibility

Use `seed=1` when calling `delivery_times()` so that simulation results are reproducible.

## Interface

Use Streamlit widgets such as:

- `st.selectbox()` for zone and time block.
- `st.number_input()` or sliders for cost assumptions.
- Inputs for minimum, maximum, and increment of promised delivery times.
- `st.button()` to trigger the recommendation.

The app should present the recommended promise and corresponding net profit clearly.
