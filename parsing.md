# https://account-api.topmediai.com/

## GET /account/login
- Request:
    ?email=nikpet00300%40gmail.com&password=c4f5e2f03cb2796f698e413b74072e28&lang=en&information_sources=https:%2F%2Faccount.topmediai.com&source_site=www.topmediai.com
- Response:
``{"code":200,"msg":"Login successful.","data":{"member_id":"12130774","member_code":"f4b83482f43fcc90","token":"000000000000000000000000000000000000000000","email":"nikpet00300@gmail.com","mobile":"","area_code":"","account":"nikpet00300@gmail.com","notice_email":"nikpet00300@gmail.com","sources_brand_id":"19","first_name":"nikpet00300","account_url":"https:\/\/account.topmediai.com","icart_url":"https:\/\/orderapi.topmediai.com"},"time":1737032838}``

## GET /account/index
Get account information
- Request:
    ?token=000000000000000000000000000000000000000000&information_sources=https:%2F%2Faccount.topmediai.com&timestamp=1737032838925&sign=B09777A2F4DA3E02534319C3CCA4D119A3D4B80F
- Response: ``
{"code":200,"msg":"Operation is successful.","data": { "id":"12130774", "uuid":"bfb56d36-d32c-11ef-bb25-00163e0fdf2c", "email":"nikpet00300@gmail.com", "mobile":"","area_code":"","brand_id":"19","head_photo":"","last_name":"","first_name":"nikpet00300","gender":"0","birthday":"0","address":"","create_time":"1736937462","vip_type":"2","notice_email":"nikpet00300@gmail.com","modified_notice_email":"0","remind_stime":"1","member_code":"f4b83482f43fcc90","source_site":"www.topmediai.com","country_code":"NL","account":"nikpet00300@gmail.com","gender_value":"Unspecified","birthday_value":"","country_value":"Netherlands","head_photo_thumbnail":"","show_tip":"1","has_password":"1","google_account":"","facebook_account":"","apple_account":"","wechat_account":"","accumulated_points":"0","lock_points":"0","sign_in_ip":"","time_zone":"","sign_in_days":"0","last_sign_in_time":"0","has_google_account":"2","has_facebook_account":"2","has_apple_account":"2","has_wechat_account":"2","email_verification":"0","member_shipping_address":[],"icart_url":"https:\/\/orderapi.topmediai.com","is_promotion":"0","sign_in_task_tag":"SIGNIN000000","sign_in_task_target":"5","has_sign_in":"2","sign_in_points":"2","is_show_sign_in_task":"1","gen_seven_days_points":"0"},"time":1737032839}``

# https://tp-gateway-api.topmediai.com

## GET /tp_member/permission/info
Check for balance
- Request: ``
    ?product_id=12&token=000000000000000000000000000000000000000000
    Authorization: 000000000000000000000000000000000000000000
    X-Requested-With: TTS
    Token: 000000000000000000000000000000000000000000``

- Response:
``{"check_code":200000,"data":{"email":"nikpet00300@gmail.com","music":{"all":502,"free":2,"is_super_vip":false,"is_vip":true,"left":502,"rate":1.0,"used":0},"nick_name":"","user_avatar":"","user_id":"12130774"},"message":"Success","status":200}``

# https://aimusic-api.topmediai.com

## POST /generate/music
Request for music generation
1. With voice
- Request: ``
    Authorization: 000000000000000000000000000000000000000000
    X-Requested-With: TTS
    Token: 000000000000000000000000000000000000000000
    Content-Type: **multipart/form-data;**

    mv=v4.0
    instrumental=0
    g_num=2
    is_public=0
    is_auto=0
    prompt=Guitar
    lyrics=Happy song
    title=Asfasdf
    gender=male
    token=000000000000000000000000000000000000000000``

- Response:
``{
  "data": [
    {
      "id": 1128400,
      "is_public": 0,
      "music": [
        {
          "audio_duration": "Infinity",
          "audio_file": "jZkSvaJaFfi3sZ0F7TTJIwIlKlHfP3OtS9gMdugpUWRD9pg8y9vqiyvwWU1++qkt26l5LbfdG3N5rjDvNue+ng==",
          "image_file": "jSDI6QcA5vXwnarnl0AKvnDpPQTvxkee58yUMDexdCfyjSfO/8JPXhS0sOEtoF5ZL2eZ9VCRVWJlnDeUIN6btI+lcilEbRLxRNvC0g/+X9w=",
          "item_uuid": "3a28337f-2928-464e-9f7d-8d110422f006",
          "lyric": "Happy song",
          "tags": "Guitar, male voice",
          "title": "Asfasdf"
        },
        {
          "audio_duration": "Infinity",
          "audio_file": "jZkSvaJaFfi3sZ0F7TTJI/XjBguCpQH0c/uk8TVZOQkybI6wyDfOEa/zBjVwOaDWURsdgRuVgtj0qk/buIZR6Q==",
          "image_file": "jSDI6QcA5vXwnarnl0AKvkb1JjoX6I310VSyMcFXA0p4Y66Zbe8n3LCyOjnCS3UjEMaptTecnNPduaIE52Tyx6jtsL9LWxLuOK7B5nRx3kI=",
          "item_uuid": "723cdcdb-6470-46cf-80a3-b1043771eae3",
          "lyric": "Happy song",
          "tags": "Guitar, male voice",
          "title": "Asfasdf"
        }
      ],
      "part": 1,
      "uuid": "2e3044a4-d40c-11ef-bd0a-00163e0c6618"  It is the request uuid
    }
  ],
  "message": "Success",
  "status": 200
}``

2. No voice
- Request:
    Authorization: 000000000000000000000000000000000000000000
    X-Requested-With: TTS
    Token: 000000000000000000000000000000000000000000
    Content-Type: **multipart/form-data;**

    mv=v4.0
    instrumental=1
    g_num=2
    is_public=0
    is_auto=1
    prompt=Happy song
    token=000000000000000000000000000000000000000000
``
- Response: ``
{
  "data": [
    {
      "id": 1128663,
      "is_public": 0,
      "music": [
        {
          "audio_duration": "Infinity",
          "audio_file": "0//UbatF4grLI0BnGQOqSBQLrej+ji/UvDlJae2GLScCGRicHPiKWMIAg0wDha44hrm3ZvIg5Uyh8sd7BAEOydVSbb6J7Eq7VqEP3ZxNO8Y=",
          "image_file": "jSDI6QcA5vXwnarnl0AKvsm8juTeYlgmCyDsLwOR71bbUwaCExrsoq3PjAvOQbfbpk3ppLAWbb6U83+DdiJz7mY/im/+lbn3W+kGHvqmTaA=",
          "item_uuid": "5b16e6d0-61eb-4aad-a46a-6969d2bb3eb1",
          "lyric": "[Instrumental]",
          "tags": "pop, upbeat, happy, energetic",
          "title": "Sunshine All the Way"
        },
        {
          "audio_duration": "Infinity",
          "audio_file": "0//UbatF4grLI0BnGQOqSBQLrej+ji/UvDlJae2GLSdlfS3sjIJEV0yv4axxfX5VhQYdHZgwlwGVVZyXViPZdi3s/j/G4LxlWg36srIHKOs=",
          "image_file": "jSDI6QcA5vXwnarnl0AKvj8d9vRoOYWFN/41DDl5Y1a81m1nXpQ2yxBY94mxTq1S+mEYd+hq2bos8DgGXPSG3zgsEVMXV1xR69bBFpqgS98=",
          "item_uuid": "2dd746c5-bc4f-4228-a543-a656abbaf12a",
          "lyric": "[Instrumental]",
          "tags": "pop, upbeat, happy, energetic",
          "title": "Sunshine All the Way"
        }
      ],
      "part": 1,
      "uuid": "8588231c-d410-11ef-8414-00163e0c66d5"
    }
  ],
  "message": "Success",
  "status": 200
}
``


## GET /generate/query
Check status of generation
- Request: ``
    ?uuid=2e3044a4-d40c-11ef-bd0a-00163e0c6618&token=000000000000000000000000000000000000000000
    Authorization: 000000000000000000000000000000000000000000
    X-Requested-With: TTS
    Token: 000000000000000000000000000000000000000000

    uuid is uuid from generation request
``

- Response:
1.
``{
  "data": [
    {
      "info": [
        {
          "audio_duration": 3640,
          "audio_file": "em9bPfhUBM8P+rQS2tYrTRuDwl69hLo1lkV1iGKezeRdOLlMRzAogXbPMPoJtlYRIFstGE9zfl+qlg0wKCvp9uCZLW5APVezXuVNrvkZKYw+Y8haY3T+nGQ2Ruk8hW95",
          "image_file": "em9bPfhUBM8P+rQS2tYrTRuDwl69hLo1lkV1iGKezeRdOLlMRzAogXbPMPoJtlYRIFstGE9zfl+qlg0wKCvp9uCZLW5APVezXuVNrvkZKYwPVEdkFJdXqAYFNwArYeKe"
        },
        {
          "audio_duration": 8680,
          "audio_file": "em9bPfhUBM8P+rQS2tYrTRuDwl69hLo1lkV1iGKezeQARi0M1yt/cWWRGZWU3ScJUvdP9IoJrU36BoJU9UbJmuJ6fAGjkI0tw03uCURtjE1W74JUkxlWFtQuj136ISlx",
          "image_file": "em9bPfhUBM8P+rQS2tYrTRuDwl69hLo1lkV1iGKezeQARi0M1yt/cWWRGZWU3ScJUvdP9IoJrU36BoJU9UbJmuJ6fAGjkI0tw03uCURtjE2tMZMJHYZ1cAx7fVSS8zrU"
        }
      ],
      "status": 0,  0 for finished, 2 for in progress
      "uuid": "2e3044a4-d40c-11ef-bd0a-00163e0c6618"
    }
  ],
  "message": "Success",
  "status": 200
}``
2. ``{"data":[{"info":[],"status":2,"uuid":"8588231c-d410-11ef-8414-00163e0c66d5"}],"message":"Success","status":200}``


# https://files.topmediai.com

## GET /aimusic/12130774/3a28337f-2928-464e-9f7d-8d110422f006-audio.mp3
- Request:
12130774 is member_id from login
3a28337f-2928-464e-9f7d-8d110422f006 is item_uuid
- Response:
Audio file
