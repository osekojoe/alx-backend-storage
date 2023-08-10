-- Creates a trigger that decreases the quantity of an item after adding a new order.
-- Quantity in the table items can be negative.
CREATE TRIGGER decrease_quantity
AFTER INSERT ON orders
FOR EACH ROW
BEGIN
	UPDATE items
	SET quantity = quantity - NEW.number
	WHERE NAME = NEW.item_name;
END;
//

DELIMITER;