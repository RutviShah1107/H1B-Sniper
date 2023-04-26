def generate_query(search_term, filters=None):
    # Construct the SQL query based on the user input and filter criteria
    query = f"""
        SELECT job.job_title AS job_title, 
               employer.employer_name AS employer_name, 
               employer.employer_state AS employer_state, 
               employer.employer_city AS employer_city, 
               "case".case_status AS case_status, 
               DATE("case".decision_date) AS decision_date,
               wage.wage_rate_of_pay_from AS wage_rate_of_pay_from, 
               wage.wage_unit_of_pay AS wage_unit_of_pay, 
               others.h_1b_dependent AS h_1b_dependent, 
               job.full_time_position AS full_time_position
        FROM job
        INNER JOIN employer ON job.case_number = employer.case_number
        INNER JOIN wage ON job.case_number = wage.case_number
        INNER JOIN others ON job.case_number = others.case_number
        INNER JOIN "case" ON job.case_number = "case".case_number
        WHERE (LOWER(job.job_title) LIKE LOWER('%{search_term}%') 
               OR LOWER(employer.employer_name) LIKE LOWER('%{search_term}%') 
               OR LOWER(employer.employer_city) LIKE LOWER('%{search_term}%') 
               OR LOWER(employer.employer_state) LIKE LOWER('%{search_term}%'))
    """
    
    # Add filter criteria to the SQL query if provided
    if filters:
        if filters['case_status']:
            if filters['case_status'].lower() == 'all':
                pass
            else:
                query += f"AND LOWER(\"case\".case_status) = LOWER('{filters['case_status']}') "
        if filters['decision_date']:
            if filters['decision_date'].lower() == 'all':
                pass
            else:
                year = filters['decision_date'][-4:]
                query += f"AND EXTRACT(year FROM DATE(\"case\".decision_date)) = '{year}' "
        if filters['wage_unit_of_pay']:
            if filters['wage_unit_of_pay'].lower() == 'all':
                pass
            else:
                query += f"AND LOWER(wage.wage_unit_of_pay) = LOWER('{filters['wage_unit_of_pay']}') "
        if filters['h_1b_dependent']:
            if filters['h_1b_dependent'].lower() == 'all':
                pass
            else:
                if filters['h_1b_dependent'].lower() == 'yes':
                    query += f"AND (LOWER(others.h_1b_dependent) = 'yes' OR LOWER(others.h_1b_dependent) = 'y') "
                elif filters['h_1b_dependent'].lower() == 'no':
                    query += f"AND (LOWER(others.h_1b_dependent) = 'no' OR LOWER(others.h_1b_dependent) = 'n') "
        if filters['full_time_position']:
            if filters['full_time_position'].lower() == 'all':
                pass
            else:
                query += f"AND LOWER(job.full_time_position) = LOWER('{filters['full_time_position'][0]}') "
        if filters['wage_rate_of_pay_from']:
            if filters['wage_rate_of_pay_from'].lower() == 'default':
                pass
            elif filters['wage_rate_of_pay_from'].lower() == 'asce':
                query += "ORDER BY wage.wage_rate_of_pay_from ASC "
            elif filters['wage_rate_of_pay_from'].lower() == 'desc':
                query += "ORDER BY wage.wage_rate_of_pay_from DESC "
        
    # Limit the query to 30 results
    query += "LIMIT 30"

    return query



# Apply filter on the query results
def filter_results(results, case_status=None, decision_date=None, wage_rate_of_pay_from=None, h_1b_dependent=None, full_time_position=None):
    # Define the field names
    fields = ['job_title', 'full_time_position', 'employer_name', 'employer_state', 'employer_city', 'wage_rate_of_pay_from', 'wage_unit_of_pay', 'h_1b_dependent', 'case_status', 'decision_date']
    
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
    
    return filtered_results
