import requests

url = 'http://127.0.0.1:5000/upload_excel'

file_path = r"C:\Users\sukes\Downloads\test.xlsx" 
with open(file_path, 'rb') as file:
    files = {'file': file}
    response = requests.post(url, files=files)

if response.status_code == 200:
    print(response.json())
elif response.status_code == 400:
    print('Validation issues found:')
    print(response.json())
else:
    print('Failed to upload file')
    print('Status code:', response.status_code)
    print('Response:', response.text)

