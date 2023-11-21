from BACK.authentication.jwt_handler import create_access_token

a = create_access_token("chapssal_kidn")

print(a)
print(type(a))
