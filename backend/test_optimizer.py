from inventory_optimizer import InventoryOptimizer


optimizer = InventoryOptimizer(
    forecast_demand=10,
    demand_std=3,
    lead_time_days=7,
    unit_cost=100
)


print("Safety Stock:")
print(optimizer.calculate_safety_stock())


print("\nEOQ:")
print(optimizer.calculate_eoq())


print("\nReorder Point:")
print(optimizer.calculate_reorder_point())


print("\nRecommendation:")
print(
    optimizer.get_recommendation(
        current_stock=20
    )
)