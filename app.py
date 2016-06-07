import csv
from flask import Flask 
from helpers import get_data, sort_by_criteria
from collections import Counter
from flask import render_template, request
app = Flask(__name__)

inmates = get_data()

@app.route("/")
def homepage():
	
	manner_of_death = Counter([d['manner_of_death'] for d in inmates])
	manners_list = manner_of_death.most_common()
	top_manners = manners_list[0:5]

	county_of_death = Counter([d['county'] for d in inmates])
	counties_list = county_of_death.most_common()
	top_counties = counties_list[0:5]

	location_of_death = Counter([d['agency_name'] for d in inmates])
	locations_list = location_of_death.most_common()
	top_locations = locations_list[0:5]

	return render_template('homepage.html', 
							top_manners=top_manners,
							top_counties=top_counties,
							top_locations=top_locations,
							inmate_count = len(inmates), 
							top_inmates=inmates[0:20])

@app.route('/results/')
def results():
	inmate_name = request.args['partial_name']
	#_sortby = reqargs.get['sortby']

	filtered_inmates = []
	for row in inmates:
		if inmate_name.upper() in row['full_name'].upper():
			filtered_inmates.append(row)
	#filtered_inmates = sort_by_criteria(sortby=sortby,datarows=filtered_inmates)
	
	return render_template('results.html', inmates=filtered_inmates)

@app.route('/county')
def county():
	inmate_name = request.args['county_name_partial']

	filtered_inmates = []
	for row in inmates:
		if inmate_name.upper() in row['county'].upper():
			filtered_inmates.append(row)
	return render_template('results.html', inmates=filtered_inmates)


if __name__ == '__main__':
	app.run(debug=True, use_reloader=True)

