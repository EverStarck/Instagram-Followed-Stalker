# igFollowing
_Track the changes in the accounts you follow. (Who do you stop following or what new account do you follow)_
<br />
<br />
Here's how igFollowing looks in action.

```
$ python igFollowing.py myIgAccount 0 ./myIgAccount.txt

    _       ______      ____              _
   (_)___ _/ ____/___  / / /___ _      __(_)___  ____ _
  / / __ `/ /_  / __ \/ / / __ \ | /| / / / __ \/ __ `/
 / / /_/ / __/ / /_/ / / / /_/ / |/ |/ / / / / / /_/ /
/_/\__, /_/    \____/_/_/\____/|__/|__/_/_/ /_/\__, /
  /____/                                      /____/


Accounts that you no longer follow but that you followed before:
[-] 1234567890 ---- TestAccount

Tracked accounts that are not in your txt:
[] 123456789 ---- Other Test


[Δ][Δ] No changes were made to your txt. If you want to update it, you must execute the command again: python igFollowing.py acountName 1
```

## Setup

1) Clone the repository

```
$ git clone https://github.com/EverStarck/igFollowing
```

2) Install the dependencies

```
$ cd igFollowing
$ pip install -r requirements.txt
```

3) Introduce your instagram cookie

```python
7. COOKIE = '' # <--- HERE
```
To get your instagram cookie just go to ig official page and follow the next steps: <br/>
1. Right click in empty space > inspect element > Network tab
2. Press f5 to realod the page
3. Search for "www.instagram.com", it should be the first
4. Search for Request Headers
5. Copy all the content of "Cookie"

It should look like this:
```py
COOKIE = 'ig_did=1111111-1111-1111-1111-111111111111; ig_nrcb=1; mid=B_BBBBBBBBBBBBB-BBBBBBBBBBBB; fbm_11111111111111=base_domain=.instagram.com; datr=AAAAAAAAAAAAAAAAAAAAAAAAAAA; ds_user_id=11111111111; csrftoken=AAAAAAAAAAAAAAAAAAAAAAAAAAAAAA; sessionid=111111111111111111111111; shbid="11111\1111111111111\11111111111:111111111111111111111111111111111111111111111111111111111111111"; shbts="111111111\1111111111\111111111111:11111111111111111111111111111111111111111111111111111111111111"; rur="AAA\111111111111\11111111111:1111111111111111111111111111111111111111111111111111"' # <--- HERE
```

4) Run the script

```
$ python igFollowing.py myIgAccount 0 ./myIgAccount.txt
```

## Usage

### Generate or update list of people you follow
```
$ python igFollowing.py myIgAccount 1
```

### Compare the list with your instagram account
```
$ python igFollowing.py myIgAccount 0 ./myIgAccount.txt
```

## Δ
The script is not optimized and was not tested on accounts with a large number of followers [maximum tested : 1k]. <br/>
If the script doesn't work as it should because of this, feel free to open an issue or a PR


## Compatibility

Tested on Python 3.9 on Linux and Windows. Feel free to open an issue if you have bug reports or questions. If you want to collaborate, you're welcome.

