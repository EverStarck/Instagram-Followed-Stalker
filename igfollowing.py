import requests
import re
import sys, colorama
from colorama import Fore, Style
from pathlib import Path

USER_AGENT = "Mozilla/5.0 (iPhone; CPU iPhone OS 12_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Instagram 105.0.0.11.118 (iPhone11,8; iOS 12_3_1; en_US; en-US; scale=2.00; 828x1792; 165586599)"
COOKIE = ''
headers = {"user-agent": USER_AGENT, "cookie": COOKIE}


profile = sys.argv[1]
getInfoUrl = f"https://www.instagram.com/{profile}/?__a=1"

saveFollows = 0
try:
    saveFollows = int(sys.argv[2])
except:
    pass

# Get user ID with profile name
def getID():
    try:
        req = requests.session()
        req.headers.update(headers)
        res = req.get(getInfoUrl)
        userInfo = res.json()
        return {
            "id": userInfo["graphql"]["user"]["id"],
            "followersNumber": userInfo["graphql"]["user"]["edge_follow"]["count"],
        }
    except:
        print(
            f"Hubo un error obteniendo el usuario {profile}\nSi el user está bien entonces es un error de cookies"
        )
        sys.exit()

# Save list of follow users in txt
def saveFile(itemToWrite):
    try:
        titleFile = re.sub("[^A-Za-z0-9\s]+", "", profile).rstrip()
        # Create file
        with open(f"./{titleFile}.txt", "w") as file:
            file.write(str(itemToWrite))
        print("Usuarios seguidos guardados con exito")
        return True
    except:
        print("Hubo un error guardando los usuarios en el archivo")
        return False

def compareFollows(followingList):
    print(followingList)

# Get list of all follow user
def getFollowers():
    userID = getID()
    try:
        req = requests.session()
        req.headers.update(headers)
        res = req.get(
            f"https://i.instagram.com/api/v1/friendships/{userID['id']}/following/?count={userID['followersNumber']}"
        )
        if res.status_code == 200:
            json = res.json()
            followingList = []
            for user in json["users"]:
                defaultDict = {
                    "id": user["pk"],
                    "username": user["username"],
                    "photo": user["profile_pic_url"],
                }
                followingList.append(defaultDict)
            if saveFollows:
                saveFile(followingList)
                return
            compareFollows(followingList)
            return True
        else:
            print("Hubo un error obteniendo los followers")
            return False
    except:
        print("Hubo un error obteniendo los followers\nQuizas es un error de cookies")
        sys.exit()


getFollowers()