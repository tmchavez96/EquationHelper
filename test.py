car = {
	"brand":"ford",
	"model":"Mustand",
	"year":3
}
x = car.get("year")
car["year"] = 2001+x
#car.update({"year":2001})
y = car.get("power")
if(y == None):
	car["power"] = 96
else:
	car["power"] = y + 1
print(car)
