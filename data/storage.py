class OrderStorage:
    """
    In-memory storage for order statuses.
    Stores data in a dictionary: {order_id: {system: status, type: type, subtype: subtype}}
    """
    def __init__(self):
        self.orders = {}

    def get_order(self, order_id: str) -> dict | None:
        """
        Retrieve order data by order_id.
        Returns None if order_id doesn't exist.
        """
        return self.orders.get(order_id)

    def save_order(self, order_id: str, type: str, subtype: str, statuses: dict) -> None:
        """
        Save or update order data.
        statuses: {system: status}, e.g., {"Siebel": "Pending", "LDAP": "Completed"}
        """
        self.orders[order_id] = {
            "type": type,
            "subtype": subtype,
            "statuses": statuses
        }

    def update_status(self, order_id: str, system: str, status: str) -> bool:
        """
        Update status for a specific system in an order.
        Returns True if updated, False if order_id or system is invalid.
        """
        if order_id in self.orders and system in self.orders[order_id]["statuses"]:
            self.orders[order_id]["statuses"][system] = status
            return True
        return False