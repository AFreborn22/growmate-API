import bcrypt, inspect
print("bcrypt module:", bcrypt)
print("__file__:", getattr(bcrypt, "__file__", None))
try:
    print("__about__:", getattr(bcrypt, "__about__", None))
except Exception as e:
    print("about not found:", e)