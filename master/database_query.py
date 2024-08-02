from django.db import connection



#---------------- funtion to get all department details ------------------------------------------------------

def get_all_departments():
    with connection.cursor() as cursor:
        cursor.execute("SELECT department_id, department_name, description FROM department")
        rows = cursor.fetchall() 
        departments = [{'department_id': row[0], 'department_name': row[1], 'description': row[2]} for row in rows]
    return departments

def get_all_designations():
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT
                d.designation_id,
                d.designation_name,
                d.description,
                d.department_id,
                dep.department_name
            FROM
                designation d
            JOIN
                department dep ON d.department_id = dep.department_id
        """)
        rows = cursor.fetchall() 
        print("DESIG :",rows)
        designations = [{'designation_id': row[0], 'designation_name': row[1], 'description': row[2], 'department_id' : row[3],'department_name': row[4]} for row in rows]
    
    return designations