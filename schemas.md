Authorization: 'x-api-key: 00000000000000000000000000000000'

# Lyrics POST /v1/lyrics
- Request:
{"prompt": "Happy song"}

- Response:
{"status":200,"message":"Success","data":{"text":"[Verse]\nWoke up this morning with a smile on my face\nSunshine pouring through the window like lace\nFeet on the ground but I’m floating in space\nDancing to the rhythm at my own pace\n\n[Verse 2]\nCoffee’s on and the toast is golden brown\nGonna hit the streets\nTake a trip downtown\nMeeting with friends\nNever feeling down\nLife’s too short to wear a frown\n\n[Chorus]\nLife’s a party\nWe are all invited\nEvery little moment got us so excited\nHands in the air\nWe are ignited\nIn this crazy world\nWe are united\n\n[Verse 3]\nIn the park\nThe dogs run wild and free\nKids on the swings\nIt's a sight to see\nLaughter fills the air like a melody\nWe live in harmony\nJust you and me\n\n[Bridge]\nThe sky’s the limit and we’re reaching high\nNo looking back\nNo saying goodbye\nWith every heartbeat\nWe aim to fly\nUnderneath this endless\nEternal sky\n\n[Chorus]\nLife’s a party\nWe are all invited\nEvery little moment got us so excited\nHands in the air\nWe are ignited\nIn this crazy world\nWe are united","title":"Bright As The Sun"}}


# Music POST /v1/music
!!Long loading
- Request:
"is_auto": 1,
"prompt": "Happy song",
"lyrics": "[Verse]\nWoke up this morning with a smile on my face\nSunshine pouring through the window like lace\nFeet on the ground but I’m floating in space\nDancing to the rhythm at my own pace\n\n[Verse 2]\nCoffee’s on and the toast is golden brown\nGonna hit the streets\nTake a trip downtown\nMeeting with friends\nNever feeling down\nLife’s too short to wear a frown\n\n[Chorus]\nLife’s a party\nWe are all invited\nEvery little moment got us so excited\nHands in the air\nWe are ignited\nIn this crazy world\nWe are united\n\n[Verse 3]\nIn the park\nThe dogs run wild and free\nKids on the swings\nIt's a sight to see\nLaughter fills the air like a melody\nWe live in harmony\nJust you and me\n\n[Bridge]\nThe sky’s the limit and we’re reaching high\nNo looking back\nNo saying goodbye\nWith every heartbeat\nWe aim to fly\nUnderneath this endless\nEternal sky\n\n[Chorus]\nLife’s a party\nWe are all invited\nEvery little moment got us so excited\nHands in the air\nWe are ignited\nIn this crazy world\nWe are united",
"title": "Bright As The Sun"

Response:
- {
  "status": 200,
  "message": "Success",
  "data": [
    {
      "audio_file": "https://files.topmediai.com/aimusic/api/393c9e21-b4b5-480d-924b-90dbc57cb576-audio.mp3",
      "image_file": "https://files.topmediai.com/aimusic/9808384/1778471a-49cd-4b54-a9fe-1505d66adbcf-image.png",
      "item_uuid": "393c9e21-b4b5-480d-924b-90dbc57cb576",
      "title": "AI Music",
      "lyric": "[Verse]\\nWoke up this morning with a smile on my face\\nSunshine pouring through the window like lace\\nFeet on the ground but I’m floating in space\\nDancing to the rhythm at my own pace\\n\\n[Verse 2]\\nCoffee’s on and the toast is golden brown\\nGonna hit the streets\\nTake a trip downtown\\nMeeting with friends\\nNever feeling down\\nLife’s too short to wear a frown\\n\\n[Chorus]\\nLife’s a party\\nWe are all invited\\nEvery little moment got us so excited\\nHands in the air\\nWe are ignited\\nIn this crazy world\\nWe are united\\n\\n[Verse 3]\\nIn the park\\nThe dogs run wild and free\\nKids on the swings\\nIt's a sight to see\\nLaughter fills the air like a melody\\nWe live in harmony\\nJust you and me\\n\\n[Bridge]\\nThe sky’s the limit and we’re reaching high\\nNo looking back\\nNo saying goodbye\\nWith every heartbeat\\nWe aim to fly\\nUnderneath this endless\\nEternal sky\\n\\n[Chorus]\\nLife’s a party\\nWe are all invited\\nEvery little moment got us so excited\\nHands in the air\\nWe are ignited\\nIn this crazy world\\nWe are united",
      "tags": "Happy song"
    },
    {
      "audio_file": "https://files.topmediai.com/aimusic/api/6ae1e63c-3ce2-4735-b0af-77026e6f143d-audio.mp3",
      "image_file": "https://files.topmediai.com/aimusic/9674824/84a30e23-b12f-47d5-a276-7b09be080b95-image.png",
      "item_uuid": "6ae1e63c-3ce2-4735-b0af-77026e6f143d",
      "title": "AI Music",
      "lyric": "[Verse]\\nWoke up this morning with a smile on my face\\nSunshine pouring through the window like lace\\nFeet on the ground but I’m floating in space\\nDancing to the rhythm at my own pace\\n\\n[Verse 2]\\nCoffee’s on and the toast is golden brown\\nGonna hit the streets\\nTake a trip downtown\\nMeeting with friends\\nNever feeling down\\nLife’s too short to wear a frown\\n\\n[Chorus]\\nLife’s a party\\nWe are all invited\\nEvery little moment got us so excited\\nHands in the air\\nWe are ignited\\nIn this crazy world\\nWe are united\\n\\n[Verse 3]\\nIn the park\\nThe dogs run wild and free\\nKids on the swings\\nIt's a sight to see\\nLaughter fills the air like a melody\\nWe live in harmony\\nJust you and me\\n\\n[Bridge]\\nThe sky’s the limit and we’re reaching high\\nNo looking back\\nNo saying goodbye\\nWith every heartbeat\\nWe aim to fly\\nUnderneath this endless\\nEternal sky\\n\\n[Chorus]\\nLife’s a party\\nWe are all invited\\nEvery little moment got us so excited\\nHands in the air\\nWe are ignited\\nIn this crazy world\\nWe are united",
      "tags": "Happy song"
    }
  ]
}


# Submit POST /v2/submit
- Request:
  "is_auto": 1,
  "prompt": "Happy song",
  "model_version": "v3.5"

- Response:
{
  "status": 200,
  "message": "Success",
  "data": [
    {
      "audio": "https://aimusic-api.topmediai.com/api/audio/423b7480-9b57-4f4a-9109-4623eb4b2537",
      "audio_duration": -1,
      "image": "https://files.topmediai.com/aimusic/9425027/92237181-a300-494c-afc4-7ef58749e3d7-image.png",
      "lyric": "[Verse]\nWoke up to a rainbow\nBright colors in the sky\nToday feels like magic oh\nTime for dreams to fly\n\n[Verse 2]\nGonna laugh till we cry\nFeel the joy inside\nCaught up in this high\nLet’s take that wild ride\n\n[Chorus]\nWe’re dancing on sunshine\nHearts beating in time\nLet’s leave the world behind\nOur smiles in every line\n\n[Verse 3]\nThrow our worries away\nChase the clouds away\nIn this moment we'll stay\nForever in this day\n\n[Bridge]\nHands up reaching the sky\nWe can touch the stars\nIn this light we'll rise\nWherever we are\n\n[Chorus]\nWe’re dancing on sunshine\nHearts beating in time\nLet’s leave the world behind\nOur smiles in every line",
      "song_id": "423b7480-9b57-4f4a-9109-4623eb4b2537",
      "status": "RUNNING",
      "tags": "pop, happy, lively",
      "title": "Dancing on Sunshine"
    },
    {
      "audio": "https://aimusic-api.topmediai.com/api/audio/6d694f35-52ef-40d9-b0eb-f9660d6bb161",
      "audio_duration": -1,
      "image": "https://files.topmediai.com/aimusic/9850513/cf2fb25f-4ca2-4941-9c3a-3c12253e80b1-image.png",
      "lyric": "[Verse]\nWoke up to a rainbow\nBright colors in the sky\nToday feels like magic oh\nTime for dreams to fly\n\n[Verse 2]\nGonna laugh till we cry\nFeel the joy inside\nCaught up in this high\nLet’s take that wild ride\n\n[Chorus]\nWe’re dancing on sunshine\nHearts beating in time\nLet’s leave the world behind\nOur smiles in every line\n\n[Verse 3]\nThrow our worries away\nChase the clouds away\nIn this moment we'll stay\nForever in this day\n\n[Bridge]\nHands up reaching the sky\nWe can touch the stars\nIn this light we'll rise\nWherever we are\n\n[Chorus]\nWe’re dancing on sunshine\nHearts beating in time\nLet’s leave the world behind\nOur smiles in every line",
      "song_id": "6d694f35-52ef-40d9-b0eb-f9660d6bb161",
      "status": "RUNNING",
      "tags": "pop, happy, lively",
      "title": "Dancing on Sunshine"
    }
  ]
}


# Query GET /v2/query
- Request:
https://api.topmediai.com/v2/query?song_id=423b7480-9b57-4f4a-9109-4623eb4b2537

- Response:
{
  "status": 200,
  "message": "Success",
  "data": [
    {
      "audio": "https://aimusic-api.topmediai.com/api/audio/423b7480-9b57-4f4a-9109-4623eb4b2537",
      "image": "https://files.topmediai.com/aimusic/9425027/92237181-a300-494c-afc4-7ef58749e3d7-image.png",
      "song_id": "423b7480-9b57-4f4a-9109-4623eb4b2537",
      "title": "",
      "lyric": "",
      "tags": "pop, happy, lively",
      "status": "RUNNING",
      "audio_duration": -1
    }
  ]
}
{
  "status": 200,
  "message": "Success",
  "data": [
    {
      "audio": "https://files.topmediai.com/aimusic/12141654/423b7480-9b57-4f4a-9109-4623eb4b2537-audio.mp3",
      "image": "https://files.topmediai.com/aimusic/9425027/92237181-a300-494c-afc4-7ef58749e3d7-image.png",
      "song_id": "423b7480-9b57-4f4a-9109-4623eb4b2537",
      "title": "",
      "lyric": "",
      "tags": "pop, happy, lively",
      "status": "FINISHED",
      "audio_duration": 138280
    }
  ]
}
