import requests
import time
import random
import threading

vanity = ""
server_id = ""
user_cookie = ""

webhook_url = ""

banli = False
# BANLI İSE TRUE

start = 1
end = 1.25

with open("proxies.txt", "r") as file:
  lines = file.readlines()

proxies = []

for line in lines:

  line = line.rstrip("\n")

  parts = line.split(":")

  if len(parts) == 4:

    ip_address = parts[0]
    port = parts[1]
    username = parts[2]
    password = parts[3]

    proxy = f"http://{username}:{password}@{ip_address}:{port}"
  else:

    ip_address = parts[0]
    port = parts[1]

    proxy = f"{ip_address}:{port}"

  proxies.append(proxy)

for proxy in proxies:
  print(proxy)


def find():
  p_r = (1.4 / len(proxies)) + 0.2
  print("[i] Retry time " + str(p_r) + " Proxy number = ", len(proxies))
  a = 0
  loop = True
  proxycheck = True
  while loop:

    time.sleep(random.uniform(p_r, p_r + 0.3))
    a = a + 1
    try:
      if proxycheck == True:
        proxy = {"http": "http://" + proxies[a % len(proxies)]}
        responses = requests.request("GET",
                                     "https://discord.com/api/v9/invites/" +
                                     vanity,
                                     proxies=proxy)
      else:
        responses = requests.request(
          "GET", "https://discord.com/api/v9/invites/" + vanity)

      if responses.status_code == 404:
        if banli == True:
          time.sleep(3)

          print("Kapılıyor..")
          keep()
          responses = requests.get("https://discord.com/api/v9/invites/" +
                                   vanity)
          if responses.status_code == 200:
            print("Kapıldı")
            data = {"content": "@everyone URL kapıldı " + vanity}
            requests.post(webhook_url, json=data)
            loop = False

        else:
          print("Kapılıyor..")
          keep()
          data = {"content": "@everyone URL kapıldı " + vanity}
          requests.post(webhook_url, json=data)
          loop = False

      elif responses.status_code == 429:
        print("Site tarafından değer döndürülmedi.")
      else:
        print(
          "[i] Url kullanımda tekrar deneniyor " + str(a) + " [p] Proxy = ",
          proxies[a % len(proxies)])
    except requests.exceptions.RequestException as e:
      data = {
        "content": "URL checklerken bir hata meydana geldi hata kodu = " + e
      }
      requests.post(webhook_url, json=data)
      print("Hata oluştu:", e)
      continue


def checkToken():

  headers = {"Content-Type": "application/json", "Authorization": user_cookie}
  while True:
    time.sleep(10)
    try:
      response = requests.get("https://discord.com/api/v9/users/@me",
                              headers=headers)
      if response.status_code == 200:
        print("Token geçerli")
      else:
        data = {"content": "Tokende bir sıkıntı var"}
        requests.post(webhook_url, json=data)
        print("Token geçersiz")
    except requests.exceptions.RequestException as e:
      data = {
        "content":
        "Tokeni kontrol ederken bir hata meydana geldi hata kodu = " + e
      }
      requests.post(webhook_url, json=data)
      print("Hata oluştu:", e)


def keep():
  payload = {"code": vanity}
  headers = {"Content-Type": "application/json", "Authorization": user_cookie}
  url = "https://discord.com/api/v9/guilds/" + server_id + "/vanity-url"
  response = requests.request("PATCH", url, json=payload, headers=headers)
  print(response.text)


t1 = threading.Thread(target=find)
t2 = threading.Thread(target=checkToken)

t1.start()
t2.start()
