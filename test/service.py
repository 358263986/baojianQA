from bert_serving.client import BertClient
# from bert_serving.server import BertServer
bc = BertClient()
print(bc.encode(['中国','美国']))
