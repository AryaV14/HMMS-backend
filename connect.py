import psycopg2

DATABASE_URL = 'postgres://anant:XdiCZe52gS1pv3shGOL9I57k7nulsA1y@dpg-cl7r0civokcc73apcb30-a/hmms_f87i'
def connector():

    try:
        
        conn = psycopg2.connect(DATABASE_URL)

        return conn,"Successfully connected"

    except (Exception, psycopg2.Error) as error:
        print("Error fetching tables:", error)
        return None,"Connection failed"
