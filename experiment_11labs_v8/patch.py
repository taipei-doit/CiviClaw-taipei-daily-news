with open("run_exp_v8.py", "r", encoding="utf-8") as f:
    code = f.read()

# Update English intro TTS
code = code.replace('"tts": "Taipei City News Update."', '"tts": "Taipei City News Update, created by AI."')

# Update Japanese intro TTS
code = code.replace('"tts": "台北市政ニュース。"', '"tts": "台北市政ニュース。AIによって作成されました。"')

# Replace v7 with v8
code = code.replace('v7_', 'v8_')
code = code.replace('experiment_11labs_v7', 'experiment_11labs_v8')

with open("run_exp_v8.py", "w", encoding="utf-8") as f:
    f.write(code)
