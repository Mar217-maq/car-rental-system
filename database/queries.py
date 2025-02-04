# User Management Queries
create_user = """
INSERT INTO user_management (
    username, 
    password_hash, 
    role, 
    first_name, 
    last_name, 
    email, 
    phone_number, 
    address, 
    license_number, 
    license_expiry_date, 
    date_joined
) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
"""




get_user_by_username = "SELECT user_id, password_hash, role FROM user_management  WHERE username = %s"
update_user_password = "UPDATE user_management  SET password_hash = %s WHERE user_id = %s"
select_user_by_email = "SELECT user_id, first_name FROM user_management  WHERE email = %s"

# Car Management Queries
add_car = """
INSERT INTO car_management(make, model, year, mileage, available_now, min_rent_period, max_rent_period, daily_rate)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
"""
select_available_cars = "SELECT * FROM car_management WHERE available_now = 1"
select_car_by_id = "SELECT * FROM car_management WHERE car_id = %s"
update_car = "UPDATE car_management SET make=%s, model=%s, year=%s, mileage=%s, available_now=%s, min_rent_period=%s, max_rent_period=%s WHERE car_id=%s"
delete_car = "DELETE FROM car_management WHERE car_id=%s"

#Rental Booking Queries
create_rental = "INSERT INTO rentals (user_id, car_id, start_date, end_date, total_cost, status) VALUES (%s, %s, %s, %s, %s, 'Pending')"
select_rentals_by_user = "SELECT * FROM rentals WHERE user_id=%s"
select_rental_by_status = "SELECT * FROM Rentals WHERE status = %s"
select_rental_by_id = "SELECT * FROM Rentals WHERE id = %s"
update_rental_status = "UPDATE Rentals SET status = %s WHERE id = %s"


# Rental Management Queries(Admin Operations)
# Rental Management Queries(Admin Operations)
get_pending_rentals = "SELECT * FROM rental_management WHERE status = 'pending_approval'"
approve_rental = "UPDATE rental_management SET admin_action = 'approved', status = 'active' WHERE rental_id = %s"
reject_rental = "UPDATE rental_management SET admin_action = 'rejected', status = 'cancelled' WHERE rental_id = %s"
update_rental_cost = "UPDATE rental_management SET total_amount = %s WHERE rental_id = %s"