# constants/queries.py

# Query to get the most recent active API key
GET_ACTIVE_API_KEY = """
    SELECT API_KEY FROM resy.t_api_keys
    WHERE EFFECTIVE_DATE <= CURDATE()
    AND IFNULL(TERMINATED_DATE, '3000-01-01') > CURDATE()
"""