import os

chromedriver_path = 'C:/path/to/chromedriver.exe'
if os.path.isfile(chromedriver_path):
    print(f"chromedriver found at: {chromedriver_path}")
else:
    print(f"chromedriver not found at: {chromedriver_path}")
