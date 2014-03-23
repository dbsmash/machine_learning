from traveling_salesman import City
from traveling_salesman import CityList
from traveling_salesman import TravelPlan
from traveling_salesman import Algorithm

def test_city():
	city = City()
	city.set_location(0,0)

	other_city = City()
	other_city.set_location(25,25)
	assert other_city.x == 25
	assert other_city.y == 25

	distance = city.distance_to(other_city)
	assert int(distance) == 35

def test_city_list():
	cl = CityList()
	cl.populate_list()
	assert cl.size() == CityList.list_size

def test_travel_plan():
	city1 = City()
	city1.set_location(0,10)

	city2 = City()
	city2.set_location(0,20)

	city3 = City()
	city3.set_location(0,30)

	tp = TravelPlan()
	tp.add_city(city1)
	tp.add_city(city2)
	tp.add_city(city3)

	assert tp.get_total_distance() == 40

def test_mutation():
	city1 = City()
	city1.set_location(0,10)

	city2 = City()
	city2.set_location(0,20)

	city3 = City()
	city3.set_location(0,30)

	tp = TravelPlan()
	tp.add_city(city1)
	tp.add_city(city2)
	tp.add_city(city3)

	starting_order = [(x.x, x.y) for x in tp.cities]

	algorithm = Algorithm()
	algorithm.mutation_rate = 1.0
	algorithm.mutate(tp)

	ending_order = [(x.x, x.y) for x in tp.cities]
	assert not ending_order == starting_order


if __name__ == '__main__':
	test_city()
	test_city_list()
	test_travel_plan()
	test_mutation()