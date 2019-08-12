import psycopg2

#Get column names from specific table
Query = (
    'SELECT COLUMN_NAME' +
    ' FROM information_schema.COLUMNS' +
    ' WHERE TABLE_NAME = \'cdplink\';'
)

Query1 = (
    'SELECT cdplink.cdpcachedeviceid, ipinterface.ipaddr, cdplink.cdpinterfacename, cdplink.cdpcachedeviceplatform,' +
    ' bridgemaclink.macaddress FROM node,ipinterface,bridgemaclink,cdplink' +
    ' WHERE node.nodeid = ipinterface.nodeid' +
    ' AND node.nodeid = cdplink.nodeid ' +
    ' AND cdplink.nodeid = bridgemaclink.nodeid ' +
    ' ORDER BY node.nodesysname DESC;'
)

Query2 = (

)

def connect():
    conn = None

    try:
        conn = psycopg2.connect(host="10.0.4.232", database="opennms", user="opennms", password="opennms")

        cur = conn.cursor()
        cur.execute(Query)

        row = cur.fetchone

        while row is not None:
            print(row)
            row = cur.fetchone()

        cur.close

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        if conn is not None:
            conn.close()
            print('Closed conn')

if __name__ == '__main__':
    connect()