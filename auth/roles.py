def get_model_temperature_for_role(role: str) -> float:
    return {
        "customer": 0.5,
        "l1": 0.8,
        "l2": 1,
        "superadmin": 1.5,
    }.get(role, 0.7)
