# import json
# import os
# import pandas as pd
# from django.shortcuts import render
# from django.http import HttpResponse, JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from django.views.decorators.http import require_http_methods

# # Create your views here.

# file_path = 'orders.csv'

# #endpoint home
# def home(request):

#     if os.path.exists(file_path):
#         df = pd.read_csv(file_path)
#     else:
#         # Create a DataFrame
#         df = pd.DataFrame({
#             'orderID': [1, 2, 3],
#             'orderName': ['Order A', 'Order B', 'Order C'],
#             'userName': ['User 1', 'User 2', 'User 3'],
#             'status': ['', '', '']
#         })

#         # Save the DataFrame to CSV
#         df.to_csv(file_path, index=False)

#     # Convert DataFrame to HTML for rendering
#     df_html = df.to_html(classes='table table-striped')

#     return render(request, 'home.html', {'df_html': df_html})


# @csrf_exempt
# @require_http_methods(["POST"])
# def postdata(request):
#     try:
#         # Parse JSON data from the request body
#         data = json.loads(request.body.decode('utf-8'))
        
#         # Extract fields from the JSON data
#         order_id = data.get('orderID')
#         order_name = data.get('orderName')
#         user_name = data.get('userName')
#         status = data.get('status')

#         # Check if all required fields are present
#         if not all([order_id, order_name, user_name, status]):
#             return JsonResponse({'error': 'Missing required fields'}, status=400)

#         # Check if file exists, if not create it with headers
#         if os.path.exists(file_path):
#             df = pd.read_csv(file_path)
#         else:
#             df = pd.DataFrame(columns=['orderID', 'orderName', 'userName', 'status'])

#         # Create a new DataFrame for the new data
#         new_data = pd.DataFrame([{
#             'orderID': order_id,
#             'orderName': order_name,
#             'userName': user_name,
#             'status': status
#         }])

#         # Concatenate the new data to the existing DataFrame
#         df = pd.concat([df, new_data], ignore_index=True)

#         # Save updated DataFrame to CSV
#         df.to_csv(file_path, index=False)

#         # Return a JSON response indicating success
#         return JsonResponse({'message': 'Data saved successfully'}, status=201)

#     except json.JSONDecodeError:
#         return JsonResponse({'error': 'Invalid JSON'}, status=400)

#     except Exception as e:
#         return JsonResponse({'error': str(e)}, status=500)

# def example_view(request):
#     return render(request, '/index.html') 

# ***************************************************************************************
# EDIT
# ***************************************************************************************

import os
import json
import pandas as pd
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
    if os.path.exists(file_path):
        # Read existing CSV file
        df = pd.read_csv(file_path)
    else:
        # Create a new DataFrame with default data
        df = pd.DataFrame({
            'orderID': [1, 2, 3],
            'orderName': ['Order A', 'Order B', 'Order C'],
            'userName': ['User 1', 'User 2', 'User 3'],
            'status': ['', '', '']
        })
        # Save the DataFrame to CSV
        df.to_csv(file_path, index=False)

    # Convert DataFrame to HTML for rendering
    df_html = df.to_html(classes='table table-striped')

    return render(request, 'home.html', {'df_html': df_html, 'status_options': status_options})

@csrf_exempt
@require_http_methods(["POST"])
def postdata(request):
    try:
        # Debugging: Print the raw request body
        print("Raw request body:", request.body)

        # Parse JSON data from the request body
        data = json.loads(request.body.decode('utf-8'))
        print(data)

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
            df = pd.read_csv(file_path)
        else:
            df = pd.DataFrame(columns=['orderID', 'orderName', 'userName', 'status'])

        # Create a new DataFrame for the new data
        new_data = pd.DataFrame([{
            'orderID': order_id,
            'orderName': order_name,
            'userName': user_name,
            'status': status
        }])

        # Append new data to the existing DataFrame
        df = pd.concat([df, new_data], ignore_index=True)

        # Save updated DataFrame to CSV
        df.to_csv(file_path, index=False)

        # Return a success message
        return JsonResponse({'message': 'Data saved successfully'}, status=201)

    except json.JSONDecodeError:
        print("Invalid JSON received")
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    except Exception as e:
        print("An error occurred:", e)
        return JsonResponse({'error': str(e)}, status=500)


def example_view(request):
    return render(request, 'index.html')
