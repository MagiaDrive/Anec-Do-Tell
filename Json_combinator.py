import json
counter = 0
all_anecdots=[]
with open("native-english.json", 'r') as J_file:
    file = json.load(J_file)
for i in file:
    all_anecdots.append({"id":counter, "text": i['text']})
    counter+=1
with open("output.json", 'r') as J_file:
    file = json.load(J_file)
for i in file:
    all_anecdots.append({"id":counter, "text": i['text']})
    counter+=1
with open("extracted_jokes.json", 'r') as J_file:
    file = json.load(J_file)
for i in file:
    all_anecdots.append({"id":counter, "text": i['text']})
    counter+=1
print(len(all_anecdots))

with open("final_dataset.json", 'w') as file:
    json.dump(all_anecdots, file)
