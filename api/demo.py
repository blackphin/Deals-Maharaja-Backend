from datetime import datetime
var1 = "2023-04-14 18:01:35.679625+00"
var2 = datetime.strptime(var1, "%Y-%m-%d %H:%M:%S.%f%z")
print(var2)
