# H1B-Sniper
An idea to identify the companies that provide H1B sponsorship to international employees. Using governmental data for the past decade to analyze the companies, skills and job roles required to increase the chance for obtaining H1B visa sponsorships. This API can be added as an extension to companies like LinkedIn in their “Job Search” Section.
# H1B-Sponsorship-Tracker-Web-APP

### Data Source
United States Department of Labor (DOL) website - http://www.foreignlaborcert.doleta.gov/performancedata.cfm#dis

### Data Information
Size: 1.6+ GB
2+ million entries, 100 columns
Data types: datetime64(5), float64(10), int64(8), object(77)
The dataset contains information on visa applications. We select 9 categories of variables to create tables in the database, including case, job, employer, attorney/agent, website, wage, preparer, and others

### Data Preprocessing - (Pandas)
Remove NULL & duplicate values
2,074,099 -> 1,749,116 records
1.6+ GB -> 1.45 GB
Eradicating columns not required for our analysis
100 columns -> 10 columns

### Backend - Relational database (SQL/PgAdmin/psycopg)
Create databases to store the H-1B data following integrity constraints
	9 tables
Define the query generating function to fetch filtered results based on inputs

### Frontend - Flask framework (HTML/CSS/Javascript/Python)
Build a search bar for inputs
Inputs -> job title, location, company
Add filters to further shrink the target roles
Filters -> case status, time frame, pay, H-1B dependent, full time

#### Screenshot of the Application:
![image](https://user-images.githubusercontent.com/86033480/234723338-3d05f61a-60e2-4ab6-9b64-42306f82b5c3.png)

Implemented by TOP GUN Team
