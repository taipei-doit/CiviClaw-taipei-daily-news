with open("run_exp_v7.py", "r") as f:
    code = f.read()

code = code.replace('"Taipei & Fukuoka MOU"', '"Taipei & Fukuoka Sign Historic Friendship Pact"')
code = code.replace('"台北と福岡が覚書締結"', '"台北市と福岡市が歴史的な友好交流協定を締結"')
code = code.replace('v6_', 'v7_')
code = code.replace('experiment_11labs_v6', 'experiment_11labs_v7')

with open("run_exp_v7.py", "w") as f:
    f.write(code)
