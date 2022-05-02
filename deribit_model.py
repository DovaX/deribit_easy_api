import deribit_easy_api.deribit_easy_api_core as derapi



client=derapi.DeribitClient("dgVf4SU3","fxy1PNb2PCYS7a4neMBklGh1utJJd1jerBNoxVFGdE") #TEST API

response=client.limit_buy(36000, 10)
print(response)


