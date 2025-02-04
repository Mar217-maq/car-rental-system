
class User:
    def __init__(
            self,
            user_id,
            username,
            password_hash,
            role,
            first_name=None,
            last_name=None,
            email=None,
            phone_number=None,
            address=None,
            license_number=None,
            license_expiry_date=None,
            date_joined=None,
    ):
        self.user_id = user_id
        self.username = username
        self.password_hash = password_hash
        self.role = role  # 'admin' or 'customer'
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone_number = phone_number
        self.address = address
        self.license_number = license_number
        self.license_expiry_date = license_expiry_date
        self.date_joined = date_joined

    def __repr__(self):
        return f"<User(username={self.username}, role={self.role})>"

    def is_admin(self):
        return self.role == 'Admin'

    def is_customer(self):
        return self.role == 'Customer'

    def validate_password(self, input_password, password_hash):
        return password_hash.verify(self.password_hash, input_password)

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "username": self.username,
            "role": self.role,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "phone_number": self.phone_number,
            "address": self.address,
            "license_number": self.license_number,
            "license_expiry_date": self.license_expiry_date,
            "date_joined": self.date_joined
        }

    @staticmethod
    def from_dict(data):
        """
                Create a User object from a dictionary.
                :param data: Dictionary containing user data.
                :return: A User object.
                """
        try:
            return User(
                user_id=data.get("user_id"),
                username=data.get("username"),
                password_hash=data.get("password_hash"),
                role=data.get("role"),
                first_name=data.get("first_name"),
                last_name=data.get("last_name"),
                email=data.get("email"),
                phone_number=data.get("phone_number"),
                address=data.get("address"),
                license_number=data.get("license_number"),
                license_expiry_date=data.get("license_expiry_date"),
                date_joined=data.get("date_joined")
            )
        except KeyError as e:
            print(f"KeyError: Missing key {e}")
            return None


