from pymongo import MongoClient

client = MongoClient("mongodb+srv://WaveNet:WaveNetAdmin@cluster0.pk2h25a.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["WaveNet"]