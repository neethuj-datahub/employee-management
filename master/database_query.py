from django.db import connection
from django.http import JsonResponse
from django.conf import settings


#---------------- funtion to get all department details ------------------------------------------------------
def get_departments():
    with connection.cursor() as cursor:
        cursor.execute("SELECT department_id, department_name, description FROM department")
        rows = cursor.fetchall() 
        departments = [{'department_id': row[0], 'department_name': row[1], 'description': row[2]} for row in rows]
    return departments



def get_all_departments(request):

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

def get_designations():
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



def designation_list_query(start_index, page_length, search_value, draw):
    script1 = ''' 
    SELECT 
        ds.designation_id, ds.designation_name, ds.description, 
        d.department_name
    FROM designation ds
    LEFT JOIN department d ON ds.department_id = d.department_id
    WHERE ds.designation_name <> 'ALL'
    '''
    
    script2 = ''' 
    SELECT COUNT(*) FROM designation ds
    LEFT JOIN department d ON ds.department_id = d.department_id
    WHERE ds.designation_name <> 'ALL'
    '''
    
    if search_value:
        search_script = " AND ds.designation_name LIKE %s"
        script1 += search_script
        script2 += search_script

    script1 += " ORDER BY ds.designation_name ASC LIMIT %s OFFSET %s;"

    with connection.cursor() as cursor:
        if search_value:
            cursor.execute(script1, ('%' + search_value + '%', int(page_length), int(start_index)))
        else:
            cursor.execute(script1, (int(page_length), int(start_index)))
        designations = cursor.fetchall()

        if search_value:
            cursor.execute(script2, ('%' + search_value + '%',))
        else:
            cursor.execute(script2)
        total_records = cursor.fetchone()[0]

    designation_list = []
    if start_index.isdigit():
        sl_no = int(start_index) + 1
    else:
        sl_no = 1

    for row in designations:
        designation = {
            'sl_no':sl_no,
            'designation_id': row[0],
            'designation_name': row[1],
            'description': row[2],
            'department_name': row[3]
        }
        designation_list.append(designation)
        sl_no += 1
    filtered_records = total_records

    response = {
        "draw": draw,
        "recordsTotal": total_records,
        "recordsFiltered": filtered_records,
        "data": designation_list
    }
    return response

#---------------- funtion to get all location details ------------------------------------------------------

def get_all_locations():
    with connection.cursor() as cursor:
        cursor.execute("SELECT location_id, location_name, description FROM location")
        rows = cursor.fetchall() 
        locations = [{'location_id': row[0], 'location_name': row[1], 'description': row[2]} for row in rows]
    return locations

def location_list_query(start_index, page_length, search_value, draw):
    script1 = ''' 
    SELECT 
        l.location_id, l.location_name, l.description
    FROM location l
    WHERE l.location_name <> 'ALL'
    '''
    
    script2 = ''' 
    SELECT COUNT(*) FROM location l
    WHERE l.location_name <> 'ALL'
    '''
    
    if search_value:
        search_script = " AND l.location_name LIKE %s"
        script1 += search_script
        script2 += search_script

    script1 += " ORDER BY l.location_name ASC LIMIT %s OFFSET %s;"

    with connection.cursor() as cursor:
        if search_value:
            cursor.execute(script1, ('%' + search_value + '%', int(page_length), int(start_index)))
        else:
            cursor.execute(script1, (int(page_length), int(start_index)))
        locations = cursor.fetchall()

        if search_value:
            cursor.execute(script2, ('%' + search_value + '%',))
        else:
            cursor.execute(script2)
        total_records = cursor.fetchone()[0]

    location_list = []
    if start_index.isdigit():
        sl_no = int(start_index) + 1
    else:
        sl_no = 1

    for row in locations:
        location = {
            'sl_no':sl_no,
            'location_id': row[0],
            'location_name': row[1],
            'description': row[2]
        }
        location_list.append(location)
        sl_no += 1

    filtered_records = total_records

    response = {
        "draw": draw,
        "recordsTotal": total_records,
        "recordsFiltered": filtered_records,
        "data": location_list
    }
    return response

#---------------- funtion to get all employee details ------------------------------------------------------

def employee_list_query(start_index, page_length, search_value, draw):
    # Set default values if start_index or page_length are None
    start_index = start_index if start_index is not None else 0
    page_length = page_length if page_length is not None else 10
    
    # Convert to integers and handle possible conversion errors
    try:
        start_index = int(start_index)
        page_length = int(page_length)
    except ValueError:
        start_index = 0
        page_length = 10
    
    script1 = ''' 
    SELECT 
        e.employee_id, e.join_date, e.employee_no, e.name, e.phone, e.address, 
        e.emp_start_date, e.emp_end_date, e.photo, e.status,
        d.department_name, ds.designation_name, l.location_name
    FROM employee e
    LEFT JOIN department d ON e.department_id = d.department_id
    LEFT JOIN designation ds ON e.designation_id = ds.designation_id
    LEFT JOIN location l ON e.location_id = l.location_id
    WHERE e.name <> 'ALL'
    '''
    
    script2 = ''' 
    SELECT COUNT(*) FROM employee e
    LEFT JOIN department d ON e.department_id = d.department_id
    LEFT JOIN designation ds ON e.designation_id = ds.designation_id
    LEFT JOIN location l ON e.location_id = l.location_id
    WHERE e.name <> 'ALL'
    '''
    
    if search_value:
        search_script = " AND e.name LIKE %s"
        script1 += search_script
        script2 += search_script

    script1 += " ORDER BY e.name ASC LIMIT %s OFFSET %s;"

    with connection.cursor() as cursor:
        if search_value:
            cursor.execute(script1, ('%' + search_value + '%', page_length, start_index))
        else:
            cursor.execute(script1, (page_length, start_index))
        employees = cursor.fetchall()

        if search_value:
            cursor.execute(script2, ('%' + search_value + '%',))
        else:
            cursor.execute(script2)
        total_records = cursor.fetchone()[0]

    employee_list = []
    sl_no = start_index + 1

    for row in employees:
        employee = {
            'sl_no': sl_no,
            'employee_id': row[0],
            'join_date': row[1],
            'employee_no': row[2],
            'name': row[3],
            'phone': row[4],
            'address': row[5],
            'emp_start_date': row[6],
            'emp_end_date': row[7],
            'photo': settings.MEDIA_URL + row[8],
            'status': row[9],
            'department_name': row[10],
            'designation_name': row[11],
            'location_name': row[12],
        }
        employee_list.append(employee)
        sl_no += 1

    filtered_records = total_records

    response = {
        "draw": draw,
        "recordsTotal": total_records,
        "recordsFiltered": filtered_records,
        "data": employee_list
    }
    return response

