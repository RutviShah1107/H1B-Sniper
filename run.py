from flask.views import MethodView
from flask import Flask, render_template, request
import psycopg2
from query.query import generate_query, filter_results

app = Flask(__name__)

# Define your database connection parameters
db_params = {
    'database': "5400_h1b",
    'user': "postgres",
    'password': "123",
    'host': "localhost",
    'port': '5432'
}

conn = psycopg2.connect(**db_params)
cur = conn.cursor()

class Homepage(MethodView):
    results = None
    filters = None

    def get(self):
        return render_template('index.html', results=self.results, filters=self.filters)

    def post(self):
        if 'search_term' in request.form:
            search_term = request.form.get('search_term')
        else:
            search_term = ''

        self.filters = {
            'case_status': request.form.get('status'),
            'decision_date': request.form.get('timeframe'),
            'wage_rate_of_pay_from': request.form.get('wage_rate_of_pay_from'),
            'wage_unit_of_pay': request.form.get('wage_unit_of_pay'),
            'h_1b_dependent': request.form.get('dependent'),
            'full_time_position': request.form.get('full_time_positon')
        }

        query = generate_query(search_term, self.filters)

        # Execute the query and fetch the results
        cur.execute(query)
        results = cur.fetchall()
        return render_template('index.html', results=results, filters=self.filters, search_term=search_term)


app.add_url_rule('/', view_func=Homepage.as_view('home_page'), methods=['GET', 'POST'])
app.add_url_rule('/search', view_func=Homepage.as_view('search_page'), methods=['POST'])

if __name__ == '__main__':
    app.run(debug=True)

cur.close()
conn.close()