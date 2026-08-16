import numpy as np
from scipy import stats


class InventoryOptimizer:

    def __init__(
        self,
        forecast_demand,
        demand_std,
        lead_time_days,
        holding_cost_percent=0.25,
        ordering_cost=50,
        unit_cost=100,
        service_level=0.95
    ):

        self.forecast = forecast_demand
        self.demand_std = demand_std
        self.lead_time = lead_time_days

        self.holding_cost = (
            holding_cost_percent * unit_cost
        )

        self.ordering_cost = ordering_cost
        self.unit_cost = unit_cost
        self.service_level = service_level

    def calculate_safety_stock(self):

        z_score = stats.norm.ppf(
            self.service_level
        )

        safety_stock = (
            z_score
            * self.demand_std
            * np.sqrt(self.lead_time)
        )

        return round(safety_stock, 2)

    def calculate_eoq(self):

        annual_demand = self.forecast * 365

        eoq = np.sqrt(
            (
                2
                * annual_demand
                * self.ordering_cost
            )
            / self.holding_cost
        )

        return round(eoq, 2)

    def calculate_reorder_point(self):

        lead_time_demand = (
            self.forecast
            * self.lead_time
        )

        safety_stock = (
            self.calculate_safety_stock()
        )

        return round(
            lead_time_demand + safety_stock,
            2
        )

    def get_recommendation(self, current_stock):

        reorder_point = (
            self.calculate_reorder_point()
        )

        eoq = self.calculate_eoq()

        safety_stock = (
            self.calculate_safety_stock()
        )

        if current_stock <= reorder_point:

            order_qty = max(
                eoq,
                reorder_point
                - current_stock
                + safety_stock
            )

            return {
                "action": "REORDER",
                "order_quantity": round(
                    order_qty,
                    0
                ),
                "reorder_point": reorder_point,
                "safety_stock": safety_stock,
                "eoq": eoq,
                "urgency": (
                    "critical"
                    if current_stock <= safety_stock
                    else "normal"
                )
            }

        else:

            return {
                "action": "NO_ACTION",
                "current_stock": current_stock,
                "reorder_point": reorder_point,
                "safety_stock": safety_stock,
                "days_until_reorder": round(
                    (
                        current_stock
                        - reorder_point
                    )
                    / self.forecast,
                    1
                )
            }