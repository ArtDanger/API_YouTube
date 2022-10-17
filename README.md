# This API doesn't use API owned by YouTube.<br/>It uses "[undetected_chromedriver](https://github.com/ultrafunkamsterdam/undetected-chromedriver)"(basic Selenium).

## **3.7** Version

Add `user_data_dir`, this is the correct usage, see [here why](https://github.com/ultrafunkamsterdam/undetected-chromedriver/issues/820#issuecomment-1264383059).<br/> 
Now you can upload multiple videos at once.<br/>
For your convenience, I have created a [repository](https://github.com/ArtDanger/Prepare_Profile) that will help you create `Profiles` correctly.<br/>

See `example_3.7.py`

## **3.5** Version

Add upload profile. 
See `example_profile.py`

## **3.4** Version

This project public the shorts video to the YouTube.<br/>
You'll need: @gmail, Password and backup_code.<br/>

See `example.py`

###### What to get a backup code, enable in your account settings:

1. Manage your Google Account
2. Security
3. 2-Step Verification(Turn On)

The program has been tested in the Netherlands and expects you to use English.

###### How use?

1. `pip install api-youtube-uc`
2. Create YouTube channel(go to the YouTube Studio for the first time)
3. Watch file example `example.py`
