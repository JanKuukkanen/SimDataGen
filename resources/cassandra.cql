DROP KEYSPACE IF EXISTS measuring_data;
CREATE KEYSPACE measuring_data WITH replication = { 'class' : 'SimpleStrategy', 'replication_factor' : 1 };

CREATE TABLE simdatagen (id int, east int, korkeus_merenpinnasta double, lampotila double, nimi text, north int, ominaissahkojohtavuus double, paine double, vedenpinta double, virtausnopeus double, PRIMARY KEY (id));