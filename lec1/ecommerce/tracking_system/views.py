import os
import json
import csv
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

# File path for storing CSV data
file_path = 'orders.csv'

# Predefined list of status options
status_options = ['Pending', 'In Progress', 'Completed', 'Cancelled']

# Home endpoint
def home(request):
    # Check if the CSV file exists
    if os.path.exists(file_path):
        # Read existing CSV file
        with open(file_path, 'r', newline='') as file:
            reader = csv.DictReader(file)
            orders = list(reader)
    else:
        # Create default data
        orders = [
            {'orderID': '1', 'orderName': 'Order A', 'userName': 'User 1', 'status': ''},
            {'orderID': '2', 'orderName': 'Order B', 'userName': 'User 2', 'status': ''},
            {'orderID': '3', 'orderName': 'Order C', 'userName': 'User 3', 'status': ''}
        ]

        # Write default data to CSV
        with open(file_path, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['orderID', 'orderName', 'userName', 'status'])
            writer.writeheader()
            writer.writerows(orders)

    # Pass the data directly to the template
    return render(request, 'home.html', {'orders': orders, 'status_options': status_options})

@csrf_exempt
@require_http_methods(["POST"])
def postdata(request):
    try:
        # Parse JSON data from the request body
        data = json.loads(request.body.decode('utf-8'))

        # Extract fields from the JSON data
        order_id = data.get('orderID')
        order_name = data.get('orderName')
        user_name = data.get('userName')
        status = data.get('status')

        # Validate the presence of required fields
        if not all([order_id, order_name, user_name, status]):
            return JsonResponse({'error': 'Missing required fields'}, status=400)

        # Validate the status
        if status not in status_options:
            return JsonResponse({'error': 'Invalid status value'}, status=400)

        # Read or create the CSV file
        if os.path.exists(file_path):
            with open(file_path, 'r', newline='') as file:
                reader = csv.DictReader(file)
                orders = list(reader)
        else:
            orders = []

        # Check for duplicate Order ID
        if any(order['orderID'] == order_id for order in orders):
            return JsonResponse({'error': 'Order ID must be unique'}, status=400)

        # Add new data to the existing list
        new_order = {'orderID': order_id, 'orderName': order_name, 'userName': user_name, 'status': status}
        orders.append(new_order)

        # Write updated data back to CSV
        with open(file_path, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['orderID', 'orderName', 'userName', 'status'])
            writer.writeheader()
            writer.writerows(orders)

        # Return a success message
        return JsonResponse({'message': 'Data saved successfully'}, status=201)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def delete_order(request):
    try:
        # Parse JSON data from the request body
        data = json.loads(request.body.decode('utf-8'))
        order_id = data.get('orderID')

        # Check if orderID is provided
        if not order_id:
            return JsonResponse({'error': 'Order ID is required'}, status=400)

        # Read existing CSV file
        if os.path.exists(file_path):
            with open(file_path, 'r', newline='') as file:
                reader = csv.DictReader(file)
                orders = list(reader)

            # Remove the order with the specified orderID
            orders = [order for order in orders if order['orderID'] != order_id]

            # Write the updated data back to the CSV file
            with open(file_path, 'w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=['orderID', 'orderName', 'userName', 'status'])
                writer.writeheader()
                writer.writerows(orders)

            return JsonResponse({'message': 'Order deleted successfully'}, status=200)
        else:
            return JsonResponse({'error': 'File not found'}, status=404)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def edit_order(request):
    try:
        # Parse JSON data from the request body
        data = json.loads(request.body.decode('utf-8'))
        order_id = data.get('orderID')
        order_name = data.get('orderName')
        user_name = data.get('userName')
        status = data.get('status')

        # Validate the presence of required fields
        if not all([order_id, order_name, user_name, status]):
            return JsonResponse({'error': 'Missing required fields'}, status=400)

        # Validate the status
        if status not in status_options:
            return JsonResponse({'error': 'Invalid status value'}, status=400)

        # Read existing CSV file
        if os.path.exists(file_path):
            with open(file_path, 'r', newline='') as file:
                reader = csv.DictReader(file)
                orders = list(reader)

            # Find and update the order with the specified orderID
            order_found = False
            for order in orders:
                if order['orderID'] == order_id:
                    order['orderName'] = order_name
                    order['userName'] = user_name
                    order['status'] = status
                    order_found = True
                    break

            # If order not found, return an error
            if not order_found:
                return JsonResponse({'error': 'Order not found'}, status=404)

            # Write the updated data back to the CSV file
            with open(file_path, 'w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=['orderID', 'orderName', 'userName', 'status'])
                writer.writeheader()
                writer.writerows(orders)

            return JsonResponse({'message': 'Order updated successfully'}, status=200)
        else:
            return JsonResponse({'error': 'File not found'}, status=404)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    except Exception as e:
        # Catch all other exceptions and return an error message
        return JsonResponse({'error': str(e)}, status=500)

def example_view(request):
    return render(request, 'index.html')
