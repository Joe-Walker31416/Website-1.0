from app import app
from flask import jsonify
#Add test data

@app.route("/api/card_data")
def carddata():
    return jsonify([(song['name'], song['artists_name'], song['image']) for song in json_string["data"]])



json_string = {"data":
        [{'name': 'The Galway Girl', 'id': '1i92xro4lPLyjiOd3y2aqA', 'artists_name': 'Sharon Shannon', 'artists_id': '6gABJRqeRV4XW6T8vP9QEn', 'image': 'https://i.scdn.co/image/ab67616d0000b27369b1fdf0417848e1905aebe7'},
        {'name': 'Tell Me Ma', 'id': '0Z3p6q8nol4dlf3b0WRI1a', 'artists_name': 'Gaelic Storm', 'artists_id': '5dlzTgw97q5k5ws89Ww1UK', 'image': 'https://i.scdn.co/image/ab67616d0000b2737fdb0728b6252787c72ff443'}, 
        {'name': 'The Rocky Road To Dublin', 'id': '2AMHDHBuhSvcEhbv5IVSB1', 'artists_name': 'The High Kings', 'artists_id': '6wXjctGBzxkT0ghwfQ8FC0', 'image': 'https://i.scdn.co/image/ab67616d0000b27379469ad2979872c3fe41c3ad'}, 
        {'name': 'Irish Pub Song', 'id': '6zX3HwSuoQThrabeoHJvCs', 'artists_name': 'The High Kings', 'artists_id': '6wXjctGBzxkT0ghwfQ8FC0', 'image': 'https://i.scdn.co/image/ab67616d0000b273cd95e0a5bb4765ede11154fd'}, 
        {'name': 'Green and Red of Mayo', 'id': '1QfY6hlEyWSdaT8XTVGEa1', 'artists_name': 'The Saw Doctors', 'artists_id': '7jzktaiZ0YO4RquEFi4oKp', 'image': 'https://i.scdn.co/image/ab67616d0000b27334936dd63957a5cdae5461ae'}, 
        {'name': 'Whiskey in the Jar', 'id': '1UzofFX5AkfTDnwjcBkM4J', 'artists_name': 'The Dubliners', 'artists_id': '72RvmgEg2omdlMV9aExO6a', 'image': 'https://i.scdn.co/image/ab67616d0000b2730a6473e2fd56ea8049a234b1'}, 
        {'name': 'The Island', 'id': '1kSkAYLMmGyNdBQ3zP8xoQ', 'artists_name': 'Paul Brady', 'artists_id': '7lauB9o5ZYmU5lTBOw7w8L', 'image': 'https://i.scdn.co/image/ab67616d0000b273b1c97f9036d60197ef06d54e'}, 
        {'name': 'Nothing but the Same Old Story', 'id': '2jAAjATGx5CWxZx6jYdwwz', 'artists_name': 'Paul Brady', 'artists_id': '7lauB9o5ZYmU5lTBOw7w8L', 'image': 'https://i.scdn.co/image/ab67616d0000b2733838a8c2d2dfec47c3b9eaa9'}, 
        {'name': "Donald Where's Your Trousers", 'id': '3gzuSrER3D3Qunaz20bUZn', 'artists_name': 'The Irish Rovers', 'artists_id': '0tkKwWigaADLYB9HdFCjYo', 'image': 'https://i.scdn.co/image/ab67616d0000b2737bb2c012ee757142d3b3a000'}, 
        {'name': 'Galway Girl', 'id': '47gMKSBivwMXYGLXXs28GC', 'artists_name': 'The High Kings', 'artists_id': '6wXjctGBzxkT0ghwfQ8FC0', 'image': 'https://i.scdn.co/image/ab67616d0000b27308f6e3cf06a7b3e4c6ff5b03'}, 
        {'name': 'Drink The Night Away', 'id': '49t8OTCiR2zeV0VrDImdaM', 'artists_name': 'Gaelic Storm', 'artists_id': '5dlzTgw97q5k5ws89Ww1UK', 'image': 'https://i.scdn.co/image/ab67616d0000b273bb524f7f58f07ad9327faefe'}, 
        {'name': 'And a Bang on the Ear', 'id': '4tzpjYQOwqSrfiIVcyEwzm', 'artists_name': 'The Waterboys', 'artists_id': '5TnuP42pw475UrjjeabtwZ', 'image': 'https://i.scdn.co/image/ab67616d0000b273717ee086bedd41aa1df34973'}, 
        {'name': "Finnegan's Wake", 'id': '6K5Ps8meS93P4ANFl2JRoD', 'artists_name': 'The Irish Rovers', 'artists_id': '0tkKwWigaADLYB9HdFCjYo', 'image': 'https://i.scdn.co/image/ab67616d0000b273cc8c0f6f0f82225933ca7950'}, 
        {'name': 'If I Ever Leave This World Alive', 'id': '6l6UyIBwaNibzWZKfGkmJW', 'artists_name': 'Flogging Molly', 'artists_id': '5kQGFREO5FzMBMsAO3cEtj', 'image': 'https://i.scdn.co/image/ab67616d0000b27320195c851e88b96e21181de4'}, 
        {'name': "I'll Tell Me Ma", 'id': '7jwWYra6ERhJyb4UJq8oVl', 'artists_name': 'The Irish Rovers', 'artists_id': '0tkKwWigaADLYB9HdFCjYo', 'image': 'https://i.scdn.co/image/ab67616d0000b2739e73cac15fd6104adf029971'}, 
        {'name': 'Summer in Dublin', 'id': '7mY1GSHaJplKRF8yJOf8iO', 'artists_name': 'Bagatelle', 'artists_id': '4NlVFd1K2l7eDURUGjXxde', 'image': 'https://i.scdn.co/image/ab67616d0000b273c597a146b5b66231f518aa5c'}, 
        {'name': "I'm Shipping Up To Boston", 'id': '7rSERmjAT38lC5QhJ8hnQc', 'artists_name': 'Dropkick Murphys', 'artists_id': '7w9jdhcgHNdiPeNPUoFSlx', 'image': 'https://i.scdn.co/image/ab67616d0000b273030915ffa58125ae36f13a6f'}, 
        {'name': "The Foggy Dew (with Sinéad O'Connor)", 'id': '054D5EaNJTeQfPSs0UbH0F', 'artists_name': 'The Chieftains', 'artists_id': '6AnrSlk5Gp1YMXgaI3mWCL', 'image': 'https://i.scdn.co/image/ab67616d0000b27370d1c9e3e37dffeec0c37de4'}, 
        {'name': 'The Lakes of Pontchartrain - New Recording', 'id': '0ASba8RN3DZvGEwhjzVulA', 'artists_name': 'Paul Brady', 'artists_id': '7lauB9o5ZYmU5lTBOw7w8L', 'image': 'https://i.scdn.co/image/ab67616d0000b273ce54d415c80f83d30fd3dd2c'}, 
        {'name': "The Foggy Dew (with Sinéad O'Connor)", 'id': '054D5EaNJTeQfPSs0UbH0F', 'artists_name': 'The Chieftains', 'artists_id': '6AnrSlk5Gp1YMXgaI3mWCL', 'image': 'https://i.scdn.co/image/ab67616d0000b27370d1c9e3e37dffeec0c37de4'}, 
        {'name': 'The Lakes of Pontchartrain - New Recording', 'id': '0ASba8RN3DZvGEwhjzVulA', 'artists_name': 'Paul Brady', 'artists_id': '7lauB9o5ZYmU5lTBOw7w8L', 'image': 'https://i.scdn.co/image/ab67616d0000b273ce54d415c80f83d30fd3dd2c'}, 
        {'name': "Arrive On St. Patrick's Day", 'id': '0E4tTwpmHQTXQbI9Ov7V2S', 'artists_name': 'Sir Reg', 'artists_id': '0ircDsEvOEB5iDlGl2lT63', 'image': 'https://i.scdn.co/image/ab67616d0000b2735abcee8ea69057f19a548c93'}
]}


@app.route("/api/testdata")
def testdata():
    return [(song['name'],song['image']) for song in json_string["data"]] 

