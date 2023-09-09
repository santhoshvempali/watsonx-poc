api_key = 'YBFDc0SBHRKMDejR4ZJKbq02KTwEDfXxB2VQyLTfHqsA'
location = 'us-south'


import requests
import json
import os

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
def predict(inputs):
    API_KEY = api_key
    token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
    API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
    mltoken = token_response.json()["access_token"]
    # mltoken="eyJraWQiOiIyMDIzMDgwOTA4MzQiLCJhbGciOiJSUzI1NiJ9.eyJpYW1faWQiOiJJQk1pZC02OTcwMDAyS0RUIiwiaWQiOiJJQk1pZC02OTcwMDAyS0RUIiwicmVhbG1pZCI6IklCTWlkIiwianRpIjoiZjQ4MjI5NjEtNWU4Ni00NjE2LTgzY2ItYmM5MzlmZjg5OGNlIiwiaWRlbnRpZmllciI6IjY5NzAwMDJLRFQiLCJnaXZlbl9uYW1lIjoiU2lkZGhhcnRoIiwiZmFtaWx5X25hbWUiOiJPYWsiLCJuYW1lIjoiU2lkZGhhcnRoIE9hayIsImVtYWlsIjoic2lkZGhhcnRoNHdhdHNvbnhAZ21haWwuY29tIiwic3ViIjoic2lkZGhhcnRoNHdhdHNvbnhAZ21haWwuY29tIiwiYXV0aG4iOnsic3ViIjoic2lkZGhhcnRoNHdhdHNvbnhAZ21haWwuY29tIiwiaWFtX2lkIjoiSUJNaWQtNjk3MDAwMktEVCIsIm5hbWUiOiJTaWRkaGFydGggT2FrIiwiZ2l2ZW5fbmFtZSI6IlNpZGRoYXJ0aCIsImZhbWlseV9uYW1lIjoiT2FrIiwiZW1haWwiOiJzaWRkaGFydGg0d2F0c29ueEBnbWFpbC5jb20ifSwiYWNjb3VudCI6eyJ2YWxpZCI6dHJ1ZSwiYnNzIjoiOGM1MWUyZGQ0Y2E3NGQ3YWJmNWEyODQwYTk1NWZjNWUiLCJpbXNfdXNlcl9pZCI6IjExMzI4NTI5IiwiZnJvemVuIjp0cnVlLCJpbXMiOiIyNjk4NzI5In0sImlhdCI6MTY5MzM2ODM1NCwiZXhwIjoxNjkzMzcxOTU0LCJpc3MiOiJodHRwczovL2lhbS5jbG91ZC5pYm0uY29tL2lkZW50aXR5IiwiZ3JhbnRfdHlwZSI6InVybjppYm06cGFyYW1zOm9hdXRoOmdyYW50LXR5cGU6YXBpa2V5Iiwic2NvcGUiOiJpYm0gb3BlbmlkIiwiY2xpZW50X2lkIjoiZGVmYXVsdCIsImFjciI6MSwiYW1yIjpbInB3ZCJdfQ.be_ujXI5vXRqbX9ny0nM_TKN13fs6U7dJ-Fi73_0ps7abq3c1vv8VGuqY10gsR9UfIOfqNtWPXPi83dQOuCHLJ7w7nGx9WSHWcdgZdp_zbf4zvUYlXaCjZmuLR54zfor8sIwoTZc_DvrwnBxzvvvkYeMBTZoySeHIEJkt5RVEgDl_kdU8OeZ07HanvSWZmtlY4Zubzhr5QGPNnYPzjOp5gT-X_rYUBRKnEJL7OnQX252D2zTvmAn0OCR1cF1I5sKPEOGYtqsk352pomysLI-d5vflKZUVeXKFJDcdUOUIV46x5rm-XA02YLVNTFYPO5jwycq5FOlKqJtR3XuAaGsDw"
    print(mltoken)
    # mltoken="eyJraWQiOiIyMDIzMDgwOTA4MzQiLCJhbGciOiJSUzI1NiJ9.eyJpYW1faWQiOiJJQk1pZC01MDFEQlA2SFRYIiwiaWQiOiJJQk1pZC01MDFEQlA2SFRYIiwicmVhbG1pZCI6IklCTWlkIiwianRpIjoiMWE5ZWM1NmEtODg2My00YWU0LTliZTEtODU4MDRkY2U5ZDlhIiwiaWRlbnRpZmllciI6IjUwMURCUDZIVFgiLCJnaXZlbl9uYW1lIjoiU2lkZGhhcnRoIiwiZmFtaWx5X25hbWUiOiJPYWsiLCJuYW1lIjoiU2lkZGhhcnRoIE9hayIsImVtYWlsIjoic2lkZGhhcnRoLm9ha0Bnc2xhYi5jb20iLCJzdWIiOiJzaWRkaGFydGgub2FrQGdzbGFiLmNvbSIsImF1dGhuIjp7InN1YiI6InNpZGRoYXJ0aC5vYWtAZ3NsYWIuY29tIiwiaWFtX2lkIjoiSUJNaWQtNTAxREJQNkhUWCIsIm5hbWUiOiJTaWRkaGFydGggT2FrIiwiZ2l2ZW5fbmFtZSI6IlNpZGRoYXJ0aCIsImZhbWlseV9uYW1lIjoiT2FrIiwiZW1haWwiOiJzaWRkaGFydGgub2FrQGdzbGFiLmNvbSJ9LCJhY2NvdW50Ijp7InZhbGlkIjp0cnVlLCJic3MiOiJjNGExZGVhMzVhM2M3NTdiM2RiOGM1MGQ1MDAzMTZiOCIsImltc191c2VyX2lkIjoiMTEyOTI1MzMiLCJmcm96ZW4iOnRydWUsImltcyI6IjI2OTQyOTMifSwiaWF0IjoxNjkyNTkwNDYxLCJleHAiOjE2OTI1OTQwNjEsImlzcyI6Imh0dHBzOi8vaWFtLmNsb3VkLmlibS5jb20vaWRlbnRpdHkiLCJncmFudF90eXBlIjoidXJuOmlibTpwYXJhbXM6b2F1dGg6Z3JhbnQtdHlwZTphcGlrZXkiLCJzY29wZSI6ImlibSBvcGVuaWQiLCJjbGllbnRfaWQiOiJkZWZhdWx0IiwiYWNyIjoxLCJhbXIiOlsicHdkIl19.WrNdPdpXepoQ8LA9HTByA6cSmIghajg9FbPb2UoDQol6KY0AGBBSLXAaBtaPCYQoWpjzXO8RnMiCKjEHeoGORGfTHqaBNsVYZA-922J3d0-Mjvj9UEwmOkNZ3XlPik7PTtqN7iIIsVjPa2IGVxJjJVTZL7_P27AdgWDcWJVo1cYptN24070R4qL56abN2SbjIasr4lIohtfaU2BdB4FdYUe1uNyzrjow1_VFunkx8Z5vKafRv1NZ_CoZjc7CO4PTwmNh5yfNheBqXvLeIfCa91voNnfmYObc_reVVWAMkN7o4pLkxCVips3cS3zL74dplCqy9XJMqvbMi4eg8p_8Dg"

    header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

    # NOTE: manually define and pass the array(s) of values to be scored in the next line
    payload_scoring = {"input_data": [{"fields": ["pregnancy", "glucose", "bp", "skin", "insulin", "bmi", "dpf", "age"], "values": [inputs]}]}



    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/88694958-07a0-407d-b8ac-2a160115a3a5/predictions?version=2021-05-01', json=payload_scoring,
    headers={'Authorization': 'Bearer ' + mltoken})    
    print("Scoring response")
    print(response_scoring.json())
    predictions=response_scoring.json()
    print(predictions["predictions"][0]["values"][0][0])
    return predictions["predictions"][0]["values"][0][0]

# print(predict([6,	148.0,	72.0,	35.0,	169.5,	33.6,	0.627,	50]))

# 89
# 66
# 23
# 94
# 28.1
# 0.167
# 21


# 137
# 40
# 35
# 168
# 43.1
# 2.288
# 33
# 1

# 116
# 74
# 0
# 0
# 25.6
# 0.201
# 30
# 0