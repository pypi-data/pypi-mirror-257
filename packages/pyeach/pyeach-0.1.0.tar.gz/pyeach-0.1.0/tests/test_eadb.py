"""
Test the functions in eadb.py
"""

from tests.config import server

########## Test query_edw ##########

from pyeach.eadb import query_edw

########## Test string input query ##########
query = """
SET NOCOUNT ON;

SELECT TOP 100 *
FROM Epic.Encounter.PatientEncounter;
"""

string_test = query_edw(server=server, query=query)
assert string_test.shape[0] == 100, "Result from query should have 100 rows."

########## Test file input query ##########
file = "tests/sql/test_query.sql"
file_test = query_edw(server=server, file=file)
assert file_test.shape[0] == 100, "Result from query should have 100 rows."

########## Test query_socrata ##########
from pyeach.eadb import query_socrata

query = """
select
    countyname,
    locationid,
    measure,
    short_question_text,
    data_value,
    low_confidence_limit,
    high_confidence_limit,
    data_value_unit
where
    statedesc = 'North Carolina'
    and countyname in ('Guilford', 'Alamance', 'Rockingham', 'Randolph', 'Forsyth', 'Caswell')
limit 100
"""

test_socrata = query_socrata("data.cdc.gov", "cwsq-ngmh", query=query)
assert test_socrata.shape[0] == 100, "Result from query should have 100 rows."
