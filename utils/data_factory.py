from faker import Faker

fake = Faker()

class UserDataFactory:
    @staticmethod
    def get_invalid_email():
        return fake.user_name() + ".com"

    @staticmethod
    def get_weak_password():
        return fake.password(length=4)

    @staticmethod
    def get_valid_password():
        return fake.password(length=12, special_chars=True, digits=True, upper_case=True, lower_case=True)
