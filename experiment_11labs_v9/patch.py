import re

with open("run_exp_v9.py", "r", encoding="utf-8") as f:
    code = f.read()

# Replace Fukuoka with Himeji in English
code = code.replace('Taipei and Fukuoka Deepen Ties with Historic Friendship Pact', 'Taipei & Himeji Sign Historic Friendship Pact')
code = code.replace('Taipei & Fukuoka Sign Historic Friendship Pact', 'Taipei & Himeji Sign Historic Friendship Pact')
code = code.replace('Fukuoka Mayor Takashima', 'Himeji Mayor Hideyasu Kiyomoto')
code = code.replace('Taipei & Fukuoka MOU', 'Taipei & Himeji MOU') # just in case

# Replace Fukuoka with Himeji in Japanese
code = code.replace('福岡', '姫路')
code = code.replace('高島', '清元秀泰')

code = code.replace('v8_', 'v9_')
code = code.replace('experiment_11labs_v8', 'experiment_11labs_v9')

with open("run_exp_v9.py", "w", encoding="utf-8") as f:
    f.write(code)
