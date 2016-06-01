from database_connect import DatabaseSession

# initialize database object
tmp_conn = DatabaseSession()

# Connect to database
tmp_conn.establish_connection()

con_success = tmp_conn.get_connection()

if (con_success == True):
	tmp_conn.fetch_waterlevel()

	tmp_conn.close_connection()