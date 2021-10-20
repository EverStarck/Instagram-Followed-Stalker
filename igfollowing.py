import requests
import re
import ast
import sys, colorama
from colorama import Fore, Style

COOKIE = '' # <--- HERE
USER_AGENT = "Mozilla/5.0 (iPhone; CPU iPhone OS 12_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Instagram 105.0.0.11.118 (iPhone11,8; iOS 12_3_1; en_US; en-US; scale=2.00; 828x1792; 165586599)"
headers = {"user-agent": USER_AGENT, "cookie": COOKIE}


profile = sys.argv[1]
getInfoUrl = f"https://www.instagram.com/{profile}/?__a=1"

saveFollows = 0
try:
    saveFollows = int(sys.argv[2])
except:
    pass


#initialize colorama
colorama.init()
bad = Fore.RED + '[-]' + Style.RESET_ALL
good = Fore.GREEN + '[+]' + Style.RESET_ALL
alert = Fore.YELLOW + '[Δ]' + Style.RESET_ALL


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
            "isPrivate": userInfo["graphql"]["user"]["is_private"]
        }
    except:
        print(
            f"There was an error getting the user {profile}\nIf the user is ok then it is a cookie error"
        )
        sys.exit()


# Save list of follow users in txt
def saveFile(itemToWrite):
    try:
        titleFile = re.sub("[^A-Za-z0-9\s]+", "", profile).rstrip()
        # Create file
        with open(f"./{titleFile}.txt", "w") as file:
            file.write(str(itemToWrite))
        print("Followed users saved successfully")
        return True
    except:
        print("There was an error saving users into file")
        return False


# Open follows file and compare with fresh instagram follows
def compareFollows(freshList):
    try:
        with open(sys.argv[3], "r") as file:
            txtList = file.read()
            txtList = ast.literal_eval(txtList)
            txtSet = set()
            for user in txtList:
                txtSet.add(user["id"])
            freshSet = set()
            for user in freshList:
                freshSet.add(user["id"])

            justB = list(txtSet - freshSet)  # A-B (Actualmente ya no lo sigue, por lo que en freshList no está pero en txt si)
            justA = list(freshSet - txtSet)  # B-A (Lo sigue en ig pero no está en el txt)

            if len(justB) == 0 and len(justA) == 0:
                print("There were no changes")
                return

            changesB = ""
            changesA = ""
            # A-B
            for id in justB:
                for user in txtList:
                    if id == user["id"]:
                        changesB = changesB + f"{bad} {user['id']} ---- {user['username']}\n"
            # B-A
            for id in justA:
                for user in freshList:
                    if id == user["id"]:
                        changesA = changesA + f"{good} {user['id']} ---- {user['username']}\n"

            if len(changesB) == 0:
                print("There are no accounts that you used to follow but no longer\n")
            else:
                print("Accounts that you no longer follow but that you followed before:\n",changesB)
            if len(changesA) == 0:
                print("There aren't new follows\n")
            else:
                print("Tracked accounts that are not in your txt:\n",changesA)
        return True
    except:
        print("There was an error trying to open the file. Check that everything is fine and if the error persists, generate a new one")
        return False


# Get list of all follow user
def getFollowers():
    userID = getID()
    if userID['isPrivate']:
        print("The account is private, you cannot get followers info.")
        return
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
                defaultDict = {"id": user["pk"], "username": user["username"]}
                followingList.append(defaultDict)
            if saveFollows:
                saveFile(followingList)
                return
            compareFollows(followingList)
            return
        else:
            print("There was an error getting the followers")
            return False
    except:
        print("There was an error getting the followers\nMaybe it's a cookie error")
        sys.exit()


print("""
    _       ______      ____              _            
   (_)___ _/ ____/___  / / /___ _      __(_)___  ____ _
  / / __ `/ /_  / __ \/ / / __ \ | /| / / / __ \/ __ `/
 / / /_/ / __/ / /_/ / / / /_/ / |/ |/ / / / / / /_/ / 
/_/\__, /_/    \____/_/_/\____/|__/|__/_/_/ /_/\__, /  
  /____/                                      /____/   
 \n""")

getFollowers()

print(f"\n{alert}{alert} No changes were made to your txt. If you want to update it, you must execute the command again: python igFollowing.py acountName 1")
