from faker import Faker

faker = Faker()

def random_user():
    return {
        "name": faker.name(),
        "email": faker.email(),
        "address": faker.address(),
        "username": faker.user_name()
    }
