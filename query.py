import psycopg2

def generate_query(search_term, case_status=None, decision_date=None, wage_rate_of_pay_from=None, h_1b_dependent=None, full_time_position=None):
    # Construct the SQL query based on the user input and filter criteria
    query = f"""
        SELECT job.job_title AS job_title, 
               job.full_time_position AS full_time_position, 
               employer.employer_name AS employer_name, 
               employer.employer_state AS employer_state, 
               employer.employer_city AS employer_city, 
               wage.wage_rate_of_pay_from AS wage_rate_of_pay_from, 
               wage.wage_unit_of_pay AS wage_unit_of_pay, 
               others.h_1b_dependent AS h_1b_dependent, 
               "case".case_status AS case_status, 
               "case".decision_date AS decision_date
        FROM job
        INNER JOIN employer ON job.case_number = employer.case_number
        INNER JOIN wage ON job.case_number = wage.case_number
        INNER JOIN others ON job.case_number = others.case_number
        INNER JOIN "case" ON job.case_number = "case".case_number
        WHERE (job.job_title ILIKE '%{search_term}%' 
               OR employer.employer_name ILIKE '%{search_term}%' 
               OR employer.employer_city ILIKE '%{search_term}%' 
               OR employer.employer_state ILIKE '%{search_term}%')
    """
    
    # Add filter criteria to the SQL query if provided
    if case_status:
        query += f"AND \"case\".case_status = '{case_status}' "
    if decision_date:
        query += f"AND \"case\".decision_date = '{decision_date}' "
    if wage_rate_of_pay_from:
        query += f"AND wage.wage_rate_of_pay_from = '{wage_rate_of_pay_from}' "
    if h_1b_dependent:
        query += f"AND others.h_1b_dependent = '{h_1b_dependent}' "
    if full_time_position:
        query += f"AND job.full_time_position = '{full_time_position}' "
    
    # Execute the query
    cur.execute(query)
    
    # Fetch the results and print them out
    results = cur.fetchall()
    for row in results:
        print(row)
    
    # Close the database connection
    cur.close()
    conn.close()

# Apply filter on the query results
def filter_results(results, case_status=None, decision_date=None, wage_rate_of_pay_from=None, h_1b_dependent=None, full_time_position=None):
    # Define the field names
    fields = ['job_title', 'full_time_position', 'employer_name', 'employer_state', 'employer_city', 'wage_rate_of_pay_from', 'wage_unit_of_pay',\ 'h_1b_dependent', 'case_status', 'decision_date']
    
    # Filter the results based on the provided criteria
    filtered_results = []
    for row in results:
        if case_status and row[fields.index('case_status')] != case_status:
            continue
        if decision_date and row[fields.index('decision_date')] != decision_date:
            continue
        if wage_rate_of_pay_from and row[fields.index('wage_rate_of_pay_from')] != wage_rate_of_pay_from:
            continue
        if h_1b_dependent and row[fields.index('h_1b_dependent')] != h_1b_dependent:
            continue
        if full_time_position and row[fields.index('full_time_position')] != full_time_position:
            continue
        filtered_results.append(row)
    
    # Print out the filtered results
    for row in filtered_results:
        print(row)
