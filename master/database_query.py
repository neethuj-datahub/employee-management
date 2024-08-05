from django.db import connection
from django.http import JsonResponse

def get_departments():
    with connection.cursor() as cursor:
        cursor.execute("SELECT department_id, department_name, description FROM department")
        rows = cursor.fetchall() 
        departments = [{'department_id': row[0], 'department_name': row[1], 'description': row[2]} for row in rows]
    return departments

#---------------- funtion to get all department details ------------------------------------------------------

def get_all_departments(request):
    # with connection.cursor() as cursor:
    #     cursor.execute("SELECT department_id, department_name, description FROM department")
    #     rows = cursor.fetchall() 
    #     departments = [{'department_id': row[0], 'department_name': row[1], 'description': row[2]} for row in rows]
    # return departments

    draw = int(request.GET.get('draw', 1))
    start = int(request.GET.get('start', 0))
    length = int(request.GET.get('length', 10))
    search_value = request.GET.get('search[value]', '')

    # SQL query for counting total records
    total_count_query = "SELECT COUNT(*) FROM department"
    with connection.cursor() as cursor:
        cursor.execute(total_count_query)
        total_records = cursor.fetchone()[0]

    # SQL query for filtered records
    filtered_count_query = """
        SELECT COUNT(*) FROM department 
        WHERE department_name LIKE %s OR description LIKE %s
    """
    with connection.cursor() as cursor:
        cursor.execute(filtered_count_query, (f'%{search_value}%', f'%{search_value}%'))
        filtered_records = cursor.fetchone()[0]

    # SQL query for paginated and sorted records
    query = """
        SELECT department_id, department_name, description 
        FROM department 
        WHERE department_name LIKE %s OR description LIKE %s
        ORDER BY %s %s 
        LIMIT %s OFFSET %s
    """
    order_column = request.GET.get('order[0][column]', '0')  # Default to first column
    order_dir = request.GET.get('order[0][dir]', 'asc')      # Default to ascending

    columns = ['department_id', 'department_name', 'description']
    order_by = columns[int(order_column)]  # Get the column name to order by

    with connection.cursor() as cursor:
        cursor.execute(query, (f'%{search_value}%', f'%{search_value}%', order_by, order_dir, length, start))
        rows = cursor.fetchall()

    data = [{
        'department_id': row[0],
        'department_name': row[1],
        'description': row[2]
    } for row in rows]

    response = {
        'draw': draw,
        'recordsTotal': total_records,
        'recordsFiltered': filtered_records,
        'data': data
    }
    return JsonResponse(response)

#---------------- funtion to get all designation details ------------------------------------------------------

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
        designations = [{'designation_id': row[0], 'designation_name': row[1], 'description': row[2], 'department_id' : row[3],'department_name': row[4]} for row in rows]
    
    return designations

#---------------- funtion to get all location details ------------------------------------------------------

def get_all_locations():
    with connection.cursor() as cursor:
        cursor.execute("SELECT location_id, location_name, description FROM location")
        rows = cursor.fetchall() 
        locations = [{'location_id': row[0], 'location_name': row[1], 'description': row[2]} for row in rows]
    return locations