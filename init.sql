CREATE TABLE IF NOT EXISTS urls ("url" varchar);

CREATE OR REPLACE PROCEDURE insert_urls_table(urls varchar) 
LANGUAGE SQL
AS $$
    INSERT INTO urls VALUES (urls);
$$;



COMMIT;

