resultsMED={}
resultsSHORT={}
resultsLONG={}
 
#defines player class, storing the data for each user
class player: 
    def __init__(self, clientSecret, clientID, genres, dataM, artistsM, songsM, dataS, artistsS, songsS, dataL, artistsL, songsL): 
        self.clientSecret = clientSecret 
        self.clientID = clientID 
        self.genres = genres 
        self.dataMED = dataM 
        self.dataSHORT = dataS
        self.dataLONG = dataL
        self.artistsM = artistsM
        self.songsM = songsM
        self.artistsS = artistsS
        self.songsS = songsS
        self.artistsL = artistsL
        self.songsL = songsL
results={}
 
def idLists(s):
  #produces a list of the item ids for each user
  s_idlist=[]
  a_idlist=[]
  for i in range(len(s)):
    s_idlist.append(s[i]['id'])
    if s[i]['artists_id'] not in a_idlist:
      a_idlist.append(s[i]['artists_id'])
  return s_idlist, a_idlist
  
def shareds(p1,p2):
  #produces a list of all songs shared by users
  a=p1
  b=p2
  sharedc=0
  for i in range(len(a)):
    if a[i] in b:
      sharedc+=1
  #calculates the percentage of songs shared by users
  if (len(a)+len(b)-2*sharedc)==0:
    a=sharedc
  else:
    a=len(a)+len(b)
  percentage= ((sharedc)/a)*100
  return(percentage)
 
def top(p1,p2):
  #finds the top common songs between users
  for i in range(len(p1)):
    if p1[i] in p2:
      a=i
      b=p2.index(p1[i])
      
      break
  for i in range(len(p2)):
    if p2[i] in p1:
      B=p1.index(p2[i])
      A=i
      break
  c=a+b
  C=A+B
  #returns 'most top' song
  if c<C:
    return(p1[a])
  elif c==C:
    return p1[a]
  else:
    return p2[A]
    
def produceResults(res,a1,a2,s1,s2):
  #find the results for each data set, returning a dictionary
  res["sharedartists"]=shareds(a1,a2)
  res["sharedsongs"]=shareds(s1,s2)
  res["topsong"]=top(s1,s2)
  return res

#player1 = player('string', 'string',  
#                { "genres": ["alternative", "samba"]}, 
#                {"songsM": [{'name': 'Kingslayer (feat. BABYMETAL)', 'id': '7CAbF0By0Fpnbiu6Xn5ZF7', 'artists_name': 'Bring Me The Horizon', 'artists_id': '1Ffb6ejR6Fe5IamqA5oRUF'}, 
#                {'name': 'Ladies and gentlemen we are floating in space', 'id': '0fOjUafaAhJV16oRBgCtz7', 'artists_name': 'Spiritualized', 'artists_id': '6DKmuXxXASTF6xaJwcTfjv'}, 
#                {'name': 'Faint', 'id': '4Yf5bqU3NK4kNOypcrLYwU', 'artists_name': 'Linkin Park', 'artists_id': '6XyY86QOPPrYVGvF9ch6wz'}, 
#                {'name': 'Session', 'id': '00VKR5XH5jid1AgUdFz4bs', 'artists_name': 'Linkin Park', 'artists_id': '6XyY86QOPPrYVGvF9ch6wz'}, 
#                {'name': 'Man of War', 'id': '5HtNvKihacAXt34DDYYxBC', 'artists_name': 'Radiohead', 'artists_id': '4Z8W4fKeB5YxbusRsdQVPb'}, 
#                {'name': "Nobody's Listening", 'id': '1EU3VuKGZOvd1HTkxLPUXK', 'artists_name': 'Linkin Park', 'artists_id': '6XyY86QOPPrYVGvF9ch6wz'}, 
#                {'name': 'Papercut', 'id': '1Vej0qeQ3ioKwpI6FUbRv1', 'artists_name': 'Linkin Park', 'artists_id': '6XyY86QOPPrYVGvF9ch6wz'}, 
#                {'name': 'Pushing Me Away', 'id': '1gAaRSN57UYVRI4eWRyAvP', 'artists_name': 'Linkin Park', 'artists_id': '6XyY86QOPPrYVGvF9ch6wz'}, 
#                {'name': 'Numb', 'id': '2nLtzopw4rPReszdYBJU6h', 'artists_name': 'Linkin Park', 'artists_id': '6XyY86QOPPrYVGvF9ch6wz'}, 
#                {'name': "Don't Stay", 'id': '2yss0n7KmvmSr4EHvjfFpn', 'artists_name': 'Linkin Park', 'artists_id': '6XyY86QOPPrYVGvF9ch6wz'}, 
#                {'name': 'Easier to Run', 'id': '32fEW4jygJjjnZh2iBa5IR', 'artists_name': 'Linkin Park', 'artists_id': '6XyY86QOPPrYVGvF9ch6wz'}, 
#                {'name': 'One Step Closer', 'id': '3K4HG9evC7dg3N0R9cYqk4', 'artists_name': 'Linkin Park', 'artists_id': '6XyY86QOPPrYVGvF9ch6wz'}, 
#                {'name': 'Breaking the Habit', 'id': '3dxiWIBVJRlqh9xk144rf4', 'artists_name': 'Linkin Park', 'artists_id': '6XyY86QOPPrYVGvF9ch6wz'}, 
#                {'name': 'Somewhere I Belong', 'id': '3fjmSxt0PskST13CSdBUFx', 'artists_name': 'Linkin Park', 'artists_id': '6XyY86QOPPrYVGvF9ch6wz'}, 
#                {'name': 'Cure for the Itch', 'id': '3rpnfXSECgapxeGeRgUYqy', 'artists_name': 'Linkin Park', 'artists_id': '6XyY86QOPPrYVGvF9ch6wz'}, 
#                {'name': 'Lying from You', 'id': '4qVR3CF8FuFvHN4L6vXlB1', 'artists_name': 'Linkin Park', 'artists_id': '6XyY86QOPPrYVGvF9ch6wz'}, 
#                {'name': 'Hit the Floor', 'id': '4wHktoSf6C0C0fAO8IIWqs', 'artists_name': 'Linkin Park', 'artists_id': '6XyY86QOPPrYVGvF9ch6wz'}, 
#                {'name': 'Crawling', 'id': '57BrRMwf9LrcmuOsyGilwr', 'artists_name': 'Linkin Park', 'artists_id': '6XyY86QOPPrYVGvF9ch6wz'}, 
#                {'name': 'Points of Authority', 'id': '5egqKwgK5r5rvGD1LrtR7J', 'artists_name': 'Linkin Park', 'artists_id': '6XyY86QOPPrYVGvF9ch6wz'}, 
#                {'name': 'A Place for My Head', 'id': '5rAxhWcgFng3s570sGO2F8', 'artists_name': 'Linkin Park', 'artists_id': '6XyY86QOPPrYVGvF9ch6wz'}]}
#                ,'list','list'
#                ,{"songsS":},
#                'list','list'
#                ,{"songsL":},
#                'list','list')
 
# Aidan ^^^ (to be deleted later)
 
#defines the player objects
player2 = player('string', 'string',   
                { "genres":['rock and roll', 'funk rock', 'space rock', 'dream pop', 'metal', 'indie rock', 'doom metal', 'jangle pop', 'hard rock', 'new wave', 'stoner rock', 'symphonic rock', 'progressive rock', 'downtempo', 'grunge', 'garage rock', 'madchester', 'rock', 'heavy metal', 'psychedelic rock', 'art rock', 'shoegaze', 'classic rock', 'alternative rock', 'indie', 'trip hop'] },  
                {"songsM": [{'name': 'Man of War', 'id': '5HtNvKihacAXt34DDYYxBC', 'artists_name': 'Radiohead', 'artists_id': '4Z8W4fKeB5YxbusRsdQVPb'}, {'name': 'Ladies and gentlemen we are floating in space', 'id': '0fOjUafaAhJV16oRBgCtz7', 'artists_name': 'Spiritualized', 'artists_id': '6DKmuXxXASTF6xaJwcTfjv'}, {'name': 'Let Down', 'id': '2fuYa3Lx06QQJAm0MjztKr', 'artists_name': 'Radiohead', 'artists_id': '4Z8W4fKeB5YxbusRsdQVPb'}, {'name': 'Everything In Its Right Place', 'id': '2kRFrWaLWiKq48YYVdGcm8', 'artists_name': 'Radiohead', 'artists_id': '4Z8W4fKeB5YxbusRsdQVPb'}, {'name': 'Lift', 'id': '7xztI3ccyUdEYqKYABkMQM', 'artists_name': 'Radiohead', 'artists_id': '4Z8W4fKeB5YxbusRsdQVPb'}, {'name': 'And I Love Her', 'id': '7x4b0UccXSKBWxWmjcrG2T', 'artists_name': 'Kurt Cobain', 'artists_id': '6pAuTi6FXi6qFQJ1dzMXQs'}, {'name': "The Craving (Jenna's version)", 'id': '4hfqe20vqkuRv1RDsA1LbQ', 'artists_name': 'Twenty One Pilots', 'artists_id': '3YQKmKGau1PzlVlkL1iodx'}, {'name': 'Paranoid Android', 'id': '6LgJvl0Xdtc73RJ1mmpotq', 'artists_name': 'Radiohead', 'artists_id': '4Z8W4fKeB5YxbusRsdQVPb'}, {'name': 'Exit Music (For A Film)', 'id': '0z1o5L7HJx562xZSATcIpY', 'artists_name': 'Radiohead', 'artists_id': '4Z8W4fKeB5YxbusRsdQVPb'}, {'name': "Can't Stop", 'id': '3ZOEytgrvLwQaqXreDs2Jx', 'artists_name': 'Red Hot Chili Peppers', 'artists_id': '0L8ExT028jH3ddEcZwqJJ5'}, {'name': 'Jigsaw Falling Into Place', 'id': '0YJ9FWWHn9EfnN0lHwbzvV', 'artists_name': 'Radiohead', 'artists_id': '4Z8W4fKeB5YxbusRsdQVPb'}, {'name': 'Karma Police', 'id': '63OQupATfueTdZMWTxW03A', 'artists_name': 'Radiohead', 'artists_id': '4Z8W4fKeB5YxbusRsdQVPb'}, {'name': '505', 'id': '58ge6dfP91o9oXMzq3XkIS', 'artists_name': 'Arctic Monkeys', 'artists_id': '7Ln80lUS6He07XvHI8qqHH'}, {'name': 'Plug in Baby', 'id': '2UKARCqDrhkYDoVR4FN5Wi', 'artists_name': 'Muse', 'artists_id': '12Chz98pHFMPJEknJQMWvI'}, {'name': 'As the World Caves In', 'id': '3NM41PVVUr0ceootKAtkAj', 'artists_name': 'Matt Maltese', 'artists_id': '12j6dJrPXanCBwY599pZxf'}, {'name': 'Audacious', 'id': '1TNdQw9rHynqZ6wur56bpr', 'artists_name': 'Franz Ferdinand', 'artists_id': '0XNa1vTidXlvJ2gHSsRi4A'}, {'name': 'Bara Bada Bastu', 'id': '2gThkoApt6B7ajBWZRLAVv', 'artists_name': 'KAJ', 'artists_id': '4blbIMKwfzTxHGvN0Est1t'}, {'name': 'Black Hole Sun', 'id': '7fURZRPkB2S70sYR1naKTK', 'artists_name': 'Soundgarden', 'artists_id': '5xUf6j4upBrXZPg6AI4MRK'}, {'name': 'No Surprises', 'id': '10nyNJ6zNy2YVYLrcwLccB', 'artists_name': 'Radiohead', 'artists_id': '4Z8W4fKeB5YxbusRsdQVPb'}, {'name': 'I Promise', 'id': '06KakoES48DwEoAiUIdjmg', 'artists_name': 'Radiohead', 'artists_id': '4Z8W4fKeB5YxbusRsdQVPb'}] }
                ,'list','list'
                ,{"songsS":[{'name': 'Man of War', 'id': '5HtNvKihacAXt34DDYYxBC', 'artists_name': 'Radiohead', 'artists_id': '4Z8W4fKeB5YxbusRsdQVPb'}, {'name': 'Let Down', 'id': '2fuYa3Lx06QQJAm0MjztKr', 'artists_name': 'Radiohead', 'artists_id': '4Z8W4fKeB5YxbusRsdQVPb'}, {'name': 'Lift', 'id': '7xztI3ccyUdEYqKYABkMQM', 'artists_name': 'Radiohead', 'artists_id': '4Z8W4fKeB5YxbusRsdQVPb'}, {'name': 'I Promise', 'id': '06KakoES48DwEoAiUIdjmg', 'artists_name': 'Radiohead', 'artists_id': '4Z8W4fKeB5YxbusRsdQVPb'}, {'name': 'Paranoid Android', 'id': '6LgJvl0Xdtc73RJ1mmpotq', 'artists_name': 'Radiohead', 'artists_id': '4Z8W4fKeB5YxbusRsdQVPb'}, {'name': 'Ladies and gentlemen we are floating in space', 'id': '0fOjUafaAhJV16oRBgCtz7', 'artists_name': 'Spiritualized', 'artists_id': '6DKmuXxXASTF6xaJwcTfjv'}, {'name': 'Lull - Remastered', 'id': '6NVuMdBwKcxKDJe3ICzZLP', 'artists_name': 'Radiohead', 'artists_id': '4Z8W4fKeB5YxbusRsdQVPb'}, {'name': 'Malibu', 'id': '5bVOX6eyHsML2sB4aMlZEi', 'artists_name': 'Hole', 'artists_id': '5SHQUMAmEK5KmuSb0aDvsn'}, {'name': 'Everything In Its Right Place', 'id': '2kRFrWaLWiKq48YYVdGcm8', 'artists_name': 'Radiohead', 'artists_id': '4Z8W4fKeB5YxbusRsdQVPb'}, {'name': 'So Real', 'id': '6PBzdsMi6YNdYAevzozBRi', 'artists_name': 'Jeff Buckley', 'artists_id': '3nnQpaTvKb5jCQabZefACI'}, {'name': "Cupid's Chokehold / Breakfast in America - Radio Mix", 'id': '23hbqaze4DcmXchvsqIB5Q', 'artists_name': 'Gym Class Heroes', 'artists_id': '4IJczjB0fJ04gs4uvP0Fli'}, {'name': 'Meeting in the Aisle - Remastered', 'id': '4Dq6LgGObozz8ykRgYKIGn', 'artists_name': 'Radiohead', 'artists_id': '4Z8W4fKeB5YxbusRsdQVPb'}, {'name': 'And I Love Her', 'id': '7x4b0UccXSKBWxWmjcrG2T', 'artists_name': 'Kurt Cobain', 'artists_id': '6pAuTi6FXi6qFQJ1dzMXQs'}, {'name': 'Polyethylene (Parts 1 & 2) - Remastered', 'id': '17npanU0UU9JzglUnCoKdL', 'artists_name': 'Radiohead', 'artists_id': '4Z8W4fKeB5YxbusRsdQVPb'}, {'name': 'As the World Caves In', 'id': '3NM41PVVUr0ceootKAtkAj', 'artists_name': 'Matt Maltese', 'artists_id': '12j6dJrPXanCBwY599pZxf'}, {'name': 'Voyage', 'id': '4Y0lQy86Qz9ncQwgTTS2rc', 'artists_name': 'Zoë Më', 'artists_id': '1ceXjlrYcTS2i4ShwhjjcN'}, {'name': 'Sultans Of Swing', 'id': '37Tmv4NnfQeb0ZgUC4fOJj', 'artists_name': 'Dire Straits', 'artists_id': '0WwSkZ7LtFUFjGjMZBMt6T'}, {'name': 'Jigsaw Falling Into Place', 'id': '0YJ9FWWHn9EfnN0lHwbzvV', 'artists_name': 'Radiohead', 'artists_id': '4Z8W4fKeB5YxbusRsdQVPb'}, {'name': 'Melatonin - Remastered', 'id': '70lnEv38W5ilDiDdGjgcLP', 'artists_name': 'Radiohead', 'artists_id': '4Z8W4fKeB5YxbusRsdQVPb'}, {'name': 'Nude', 'id': '35YyxFpE0ZTOoqFx5bADW8', 'artists_name': 'Radiohead', 'artists_id': '4Z8W4fKeB5YxbusRsdQVPb'}] }
                ,'list','list'
                ,{"songsL":[{'name': 'Exit Music (For A Film)', 'id': '0z1o5L7HJx562xZSATcIpY', 'artists_name': 'Radiohead', 'artists_id': '4Z8W4fKeB5YxbusRsdQVPb'}, {'name': 'Everything In Its Right Place', 'id': '2kRFrWaLWiKq48YYVdGcm8', 'artists_name': 'Radiohead', 'artists_id': '4Z8W4fKeB5YxbusRsdQVPb'}, {'name': 'Just', 'id': '1dyTcli07c77mtQK3ahUZR', 'artists_name': 'Radiohead', 'artists_id': '4Z8W4fKeB5YxbusRsdQVPb'}, {'name': 'Man of War', 'id': '5HtNvKihacAXt34DDYYxBC', 'artists_name': 'Radiohead', 'artists_id': '4Z8W4fKeB5YxbusRsdQVPb'}, {'name': 'Karma Police', 'id': '63OQupATfueTdZMWTxW03A', 'artists_name': 'Radiohead', 'artists_id': '4Z8W4fKeB5YxbusRsdQVPb'}, {'name': 'Jigsaw Falling Into Place', 'id': '0YJ9FWWHn9EfnN0lHwbzvV', 'artists_name': 'Radiohead', 'artists_id': '4Z8W4fKeB5YxbusRsdQVPb'}, {'name': 'Let Down', 'id': '2fuYa3Lx06QQJAm0MjztKr', 'artists_name': 'Radiohead', 'artists_id': '4Z8W4fKeB5YxbusRsdQVPb'}, {'name': 'Paranoid Android', 'id': '6LgJvl0Xdtc73RJ1mmpotq', 'artists_name': 'Radiohead', 'artists_id': '4Z8W4fKeB5YxbusRsdQVPb'}, {'name': 'Ladies and gentlemen we are floating in space', 'id': '0fOjUafaAhJV16oRBgCtz7', 'artists_name': 'Spiritualized', 'artists_id': '6DKmuXxXASTF6xaJwcTfjv'}, {'name': "Can't Stop", 'id': '3ZOEytgrvLwQaqXreDs2Jx', 'artists_name': 'Red Hot Chili Peppers', 'artists_id': '0L8ExT028jH3ddEcZwqJJ5'}, {'name': 'Last Nite', 'id': '7kzKAuUzOITUauHAhoMoxA', 'artists_name': 'The Strokes', 'artists_id': '0epOFNiUfyON9EYx7Tpr6V'}, {'name': 'No Surprises', 'id': '10nyNJ6zNy2YVYLrcwLccB', 'artists_name': 'Radiohead', 'artists_id': '4Z8W4fKeB5YxbusRsdQVPb'}, {'name': 'And I Love Her', 'id': '7x4b0UccXSKBWxWmjcrG2T', 'artists_name': 'Kurt Cobain', 'artists_id': '6pAuTi6FXi6qFQJ1dzMXQs'}, {'name': 'Lift', 'id': '7xztI3ccyUdEYqKYABkMQM', 'artists_name': 'Radiohead', 'artists_id': '4Z8W4fKeB5YxbusRsdQVPb'}, {'name': 'Airbag', 'id': '7c378mlmubSu7NGkLFa4sN', 'artists_name': 'Radiohead', 'artists_id': '4Z8W4fKeB5YxbusRsdQVPb'}, {'name': 'Nude', 'id': '35YyxFpE0ZTOoqFx5bADW8', 'artists_name': 'Radiohead', 'artists_id': '4Z8W4fKeB5YxbusRsdQVPb'}, {'name': "The Craving (Jenna's version)", 'id': '4hfqe20vqkuRv1RDsA1LbQ', 'artists_name': 'Twenty One Pilots', 'artists_id': '3YQKmKGau1PzlVlkL1iodx'}, {'name': 'All Along the Watchtower', 'id': '2aoo2jlRnM3A0NyLQqMN2f', 'artists_name': 'Jimi Hendrix', 'artists_id': '776Uo845nYHJpNaStv1Ds4'}, {'name': 'Black Hole Sun', 'id': '2EoOZnxNgtmZaD8uUmz2nD', 'artists_name': 'Soundgarden', 'artists_id': '5xUf6j4upBrXZPg6AI4MRK'}, {'name': '21st Century Schizoid Man - Including "Mirrors"', 'id': '2MfrET7Nc3StKQcGoZKqr9', 'artists_name': 'King Crimson', 'artists_id': '7M1FPw29m5FbicYzS2xdpi'}] }
                ,'list','list') 
player1 = player('string', 'string',   
                { "genres":['rock and roll', 'funk rock', 'space rock', 'dream pop', 'metal', 'indie rock', 'doom metal', 'jangle pop', 'hard rock', 'new wave', 'stoner rock', 'symphonic rock', 'progressive rock', 'downtempo', 'grunge', 'garage rock', 'madchester', 'rock', 'heavy metal', 'psychedelic rock', 'art rock', 'shoegaze', 'classic rock', 'alternative rock', 'indie', 'trip hop'] },  
                {"songsM": [{'name': 'Man of War', 'id': '5HtNvKihacAXt34DDYYxBC', 'artists_name': 'Radiohead', 'artists_id': '4Z8W4fKeB5YxbusRsdQVPb'}, {'name': 'Ladies and gentlemen we are floating in space', 'id': '0fOjUafaAhJV16oRBgCtz7', 'artists_name': 'Spiritualized', 'artists_id': '6DKmuXxXASTF6xaJwcTfjv'}, {'name': 'Let Down', 'id': '2fuYa3Lx06QQJAm0MjztKr', 'artists_name': 'Radiohead', 'artists_id': '4Z8W4fKeB5YxbusRsdQVPb'}, {'name': 'Everything In Its Right Place', 'id': '2kRFrWaLWiKq48YYVdGcm8', 'artists_name': 'Radiohead', 'artists_id': '4Z8W4fKeB5YxbusRsdQVPb'}, {'name': 'Lift', 'id': '7xztI3ccyUdEYqKYABkMQM', 'artists_name': 'Radiohead', 'artists_id': '4Z8W4fKeB5YxbusRsdQVPb'}, {'name': 'And I Love Her', 'id': '7x4b0UccXSKBWxWmjcrG2T', 'artists_name': 'Kurt Cobain', 'artists_id': '6pAuTi6FXi6qFQJ1dzMXQs'}, {'name': "The Craving (Jenna's version)", 'id': '4hfqe20vqkuRv1RDsA1LbQ', 'artists_name': 'Twenty One Pilots', 'artists_id': '3YQKmKGau1PzlVlkL1iodx'}, {'name': 'Paranoid Android', 'id': '6LgJvl0Xdtc73RJ1mmpotq', 'artists_name': 'Radiohead', 'artists_id': '4Z8W4fKeB5YxbusRsdQVPb'}, {'name': 'Exit Music (For A Film)', 'id': '0z1o5L7HJx562xZSATcIpY', 'artists_name': 'Radiohead', 'artists_id': '4Z8W4fKeB5YxbusRsdQVPb'}, {'name': "Can't Stop", 'id': '3ZOEytgrvLwQaqXreDs2Jx', 'artists_name': 'Red Hot Chili Peppers', 'artists_id': '0L8ExT028jH3ddEcZwqJJ5'}, {'name': 'Jigsaw Falling Into Place', 'id': '0YJ9FWWHn9EfnN0lHwbzvV', 'artists_name': 'Radiohead', 'artists_id': '4Z8W4fKeB5YxbusRsdQVPb'}, {'name': 'Karma Police', 'id': '63OQupATfueTdZMWTxW03A', 'artists_name': 'Radiohead', 'artists_id': '4Z8W4fKeB5YxbusRsdQVPb'}, {'name': '505', 'id': '58ge6dfP91o9oXMzq3XkIS', 'artists_name': 'Arctic Monkeys', 'artists_id': '7Ln80lUS6He07XvHI8qqHH'}, {'name': 'Plug in Baby', 'id': '2UKARCqDrhkYDoVR4FN5Wi', 'artists_name': 'Muse', 'artists_id': '12Chz98pHFMPJEknJQMWvI'}, {'name': 'As the World Caves In', 'id': '3NM41PVVUr0ceootKAtkAj', 'artists_name': 'Matt Maltese', 'artists_id': '12j6dJrPXanCBwY599pZxf'}, {'name': 'Audacious', 'id': '1TNdQw9rHynqZ6wur56bpr', 'artists_name': 'Franz Ferdinand', 'artists_id': '0XNa1vTidXlvJ2gHSsRi4A'}, {'name': 'Bara Bada Bastu', 'id': '2gThkoApt6B7ajBWZRLAVv', 'artists_name': 'KAJ', 'artists_id': '4blbIMKwfzTxHGvN0Est1t'}, {'name': 'Black Hole Sun', 'id': '7fURZRPkB2S70sYR1naKTK', 'artists_name': 'Soundgarden', 'artists_id': '5xUf6j4upBrXZPg6AI4MRK'}, {'name': 'No Surprises', 'id': '10nyNJ6zNy2YVYLrcwLccB', 'artists_name': 'Radiohead', 'artists_id': '4Z8W4fKeB5YxbusRsdQVPb'}, {'name': 'I Promise', 'id': '06KakoES48DwEoAiUIdjmg', 'artists_name': 'Radiohead', 'artists_id': '4Z8W4fKeB5YxbusRsdQVPb'}] },'list','list'
                ,{"songsS":[{'name': 'Man of War', 'id': '5HtNvKihacAXt34DDYYxBC', 'artists_name': 'Radiohead', 'artists_id': '4Z8W4fKeB5YxbusRsdQVPb'}, {'name': 'Let Down', 'id': '2fuYa3Lx06QQJAm0MjztKr', 'artists_name': 'Radiohead', 'artists_id': '4Z8W4fKeB5YxbusRsdQVPb'}, {'name': 'Lift', 'id': '7xztI3ccyUdEYqKYABkMQM', 'artists_name': 'Radiohead', 'artists_id': '4Z8W4fKeB5YxbusRsdQVPb'}, {'name': 'I Promise', 'id': '06KakoES48DwEoAiUIdjmg', 'artists_name': 'Radiohead', 'artists_id': '4Z8W4fKeB5YxbusRsdQVPb'}, {'name': 'Paranoid Android', 'id': '6LgJvl0Xdtc73RJ1mmpotq', 'artists_name': 'Radiohead', 'artists_id': '4Z8W4fKeB5YxbusRsdQVPb'}, {'name': 'Ladies and gentlemen we are floating in space', 'id': '0fOjUafaAhJV16oRBgCtz7', 'artists_name': 'Spiritualized', 'artists_id': '6DKmuXxXASTF6xaJwcTfjv'}, {'name': 'Lull - Remastered', 'id': '6NVuMdBwKcxKDJe3ICzZLP', 'artists_name': 'Radiohead', 'artists_id': '4Z8W4fKeB5YxbusRsdQVPb'}, {'name': 'Malibu', 'id': '5bVOX6eyHsML2sB4aMlZEi', 'artists_name': 'Hole', 'artists_id': '5SHQUMAmEK5KmuSb0aDvsn'}, {'name': 'Everything In Its Right Place', 'id': '2kRFrWaLWiKq48YYVdGcm8', 'artists_name': 'Radiohead', 'artists_id': '4Z8W4fKeB5YxbusRsdQVPb'}, {'name': 'So Real', 'id': '6PBzdsMi6YNdYAevzozBRi', 'artists_name': 'Jeff Buckley', 'artists_id': '3nnQpaTvKb5jCQabZefACI'}, {'name': "Cupid's Chokehold / Breakfast in America - Radio Mix", 'id': '23hbqaze4DcmXchvsqIB5Q', 'artists_name': 'Gym Class Heroes', 'artists_id': '4IJczjB0fJ04gs4uvP0Fli'}, {'name': 'Meeting in the Aisle - Remastered', 'id': '4Dq6LgGObozz8ykRgYKIGn', 'artists_name': 'Radiohead', 'artists_id': '4Z8W4fKeB5YxbusRsdQVPb'}, {'name': 'And I Love Her', 'id': '7x4b0UccXSKBWxWmjcrG2T', 'artists_name': 'Kurt Cobain', 'artists_id': '6pAuTi6FXi6qFQJ1dzMXQs'}, {'name': 'Polyethylene (Parts 1 & 2) - Remastered', 'id': '17npanU0UU9JzglUnCoKdL', 'artists_name': 'Radiohead', 'artists_id': '4Z8W4fKeB5YxbusRsdQVPb'}, {'name': 'As the World Caves In', 'id': '3NM41PVVUr0ceootKAtkAj', 'artists_name': 'Matt Maltese', 'artists_id': '12j6dJrPXanCBwY599pZxf'}, {'name': 'Voyage', 'id': '4Y0lQy86Qz9ncQwgTTS2rc', 'artists_name': 'Zoë Më', 'artists_id': '1ceXjlrYcTS2i4ShwhjjcN'}, {'name': 'Sultans Of Swing', 'id': '37Tmv4NnfQeb0ZgUC4fOJj', 'artists_name': 'Dire Straits', 'artists_id': '0WwSkZ7LtFUFjGjMZBMt6T'}, {'name': 'Jigsaw Falling Into Place', 'id': '0YJ9FWWHn9EfnN0lHwbzvV', 'artists_name': 'Radiohead', 'artists_id': '4Z8W4fKeB5YxbusRsdQVPb'}, {'name': 'Melatonin - Remastered', 'id': '70lnEv38W5ilDiDdGjgcLP', 'artists_name': 'Radiohead', 'artists_id': '4Z8W4fKeB5YxbusRsdQVPb'}, {'name': 'Nude', 'id': '35YyxFpE0ZTOoqFx5bADW8', 'artists_name': 'Radiohead', 'artists_id': '4Z8W4fKeB5YxbusRsdQVPb'}] },
                'list','list'
                ,{"songsL":[{'name': 'Exit Music (For A Film)', 'id': '0z1o5L7HJx562xZSATcIpY', 'artists_name': 'Radiohead', 'artists_id': '4Z8W4fKeB5YxbusRsdQVPb'}, {'name': 'Everything In Its Right Place', 'id': '2kRFrWaLWiKq48YYVdGcm8', 'artists_name': 'Radiohead', 'artists_id': '4Z8W4fKeB5YxbusRsdQVPb'}, {'name': 'Just', 'id': '1dyTcli07c77mtQK3ahUZR', 'artists_name': 'Radiohead', 'artists_id': '4Z8W4fKeB5YxbusRsdQVPb'}, {'name': 'Man of War', 'id': '5HtNvKihacAXt34DDYYxBC', 'artists_name': 'Radiohead', 'artists_id': '4Z8W4fKeB5YxbusRsdQVPb'}, {'name': 'Karma Police', 'id': '63OQupATfueTdZMWTxW03A', 'artists_name': 'Radiohead', 'artists_id': '4Z8W4fKeB5YxbusRsdQVPb'}, {'name': 'Jigsaw Falling Into Place', 'id': '0YJ9FWWHn9EfnN0lHwbzvV', 'artists_name': 'Radiohead', 'artists_id': '4Z8W4fKeB5YxbusRsdQVPb'}, {'name': 'Let Down', 'id': '2fuYa3Lx06QQJAm0MjztKr', 'artists_name': 'Radiohead', 'artists_id': '4Z8W4fKeB5YxbusRsdQVPb'}, {'name': 'Paranoid Android', 'id': '6LgJvl0Xdtc73RJ1mmpotq', 'artists_name': 'Radiohead', 'artists_id': '4Z8W4fKeB5YxbusRsdQVPb'}, {'name': 'Ladies and gentlemen we are floating in space', 'id': '0fOjUafaAhJV16oRBgCtz7', 'artists_name': 'Spiritualized', 'artists_id': '6DKmuXxXASTF6xaJwcTfjv'}, {'name': "Can't Stop", 'id': '3ZOEytgrvLwQaqXreDs2Jx', 'artists_name': 'Red Hot Chili Peppers', 'artists_id': '0L8ExT028jH3ddEcZwqJJ5'}, {'name': 'Last Nite', 'id': '7kzKAuUzOITUauHAhoMoxA', 'artists_name': 'The Strokes', 'artists_id': '0epOFNiUfyON9EYx7Tpr6V'}, {'name': 'No Surprises', 'id': '10nyNJ6zNy2YVYLrcwLccB', 'artists_name': 'Radiohead', 'artists_id': '4Z8W4fKeB5YxbusRsdQVPb'}, {'name': 'And I Love Her', 'id': '7x4b0UccXSKBWxWmjcrG2T', 'artists_name': 'Kurt Cobain', 'artists_id': '6pAuTi6FXi6qFQJ1dzMXQs'}, {'name': 'Lift', 'id': '7xztI3ccyUdEYqKYABkMQM', 'artists_name': 'Radiohead', 'artists_id': '4Z8W4fKeB5YxbusRsdQVPb'}, {'name': 'Airbag', 'id': '7c378mlmubSu7NGkLFa4sN', 'artists_name': 'Radiohead', 'artists_id': '4Z8W4fKeB5YxbusRsdQVPb'}, {'name': 'Nude', 'id': '35YyxFpE0ZTOoqFx5bADW8', 'artists_name': 'Radiohead', 'artists_id': '4Z8W4fKeB5YxbusRsdQVPb'}, {'name': "The Craving (Jenna's version)", 'id': '4hfqe20vqkuRv1RDsA1LbQ', 'artists_name': 'Twenty One Pilots', 'artists_id': '3YQKmKGau1PzlVlkL1iodx'}, {'name': 'All Along the Watchtower', 'id': '2aoo2jlRnM3A0NyLQqMN2f', 'artists_name': 'Jimi Hendrix', 'artists_id': '776Uo845nYHJpNaStv1Ds4'}, {'name': 'Black Hole Sun', 'id': '2EoOZnxNgtmZaD8uUmz2nD', 'artists_name': 'Soundgarden', 'artists_id': '5xUf6j4upBrXZPg6AI4MRK'}, {'name': '21st Century Schizoid Man - Including "Mirrors"', 'id': '2MfrET7Nc3StKQcGoZKqr9', 'artists_name': 'King Crimson', 'artists_id': '7M1FPw29m5FbicYzS2xdpi'}] },
                'list','list')
 
#assign data to the player objects
player1.songsM,player1.artistsM=idLists(player1.dataMED["songsM"])
player2.songsM,player2.artistsM=idLists(player2.dataMED["songsM"])
player1.songsS,player1.artistsS=idLists(player1.dataSHORT["songsS"])
player2.songsS,player2.artistsS=idLists(player2.dataSHORT["songsS"])
player1.songsL,player1.artistsL=idLists(player1.dataLONG["songsL"])
player2.songsL,player2.artistsL=idLists(player2.dataLONG["songsL"])
 
#produce a dictionary to compile the results
resultsMED=produceResults(resultsMED,player1.artistsM,player2.artistsM,player1.songsM,player2.songsM)
resultsSHORT=produceResults(resultsSHORT,player1.artistsS,player2.artistsS,player1.songsS,player2.songsS)
resultsLONG=produceResults(resultsLONG,player1.artistsL,player2.artistsL,player1.songsL,player2.songsL)
results["sharedgenres"]=shareds(player1.genres["genres"],player2.genres["genres"])
results["medium"]=resultsMED
results["short"]=resultsSHORT
results["long"]=resultsLONG
print(results)
