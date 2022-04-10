from googleapiclient.discovery import build
from key import developerKey
from datetime import date
import json

today = date.today()
file = open(f'./votes/votes-{today}.json', "w")
voters = []
votes = {}
summary = {}
videoId = "Zu8qMuhsEso" # <- Current video you want to count votes for

def countVotes(voters, votes, apiKey, videoId):
    # creating youtube resource object
    youtube = build('youtube','v3', developerKey=apiKey)
    
    # retrieve youtube video results
    video_response=youtube.commentThreads().list(
    part='snippet,replies',
    videoId=videoId
    ).execute()

    while video_response:
        for item in video_response['items']:
        # Extracting comments
            comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
            authorUrl = item['snippet']['topLevelComment']['snippet']['authorChannelUrl']
            authorName = item['snippet']['topLevelComment']['snippet']['authorDisplayName']
            likeCount = item['snippet']['topLevelComment']['snippet']['likeCount']
            date = item['snippet']['topLevelComment']['snippet']['publishedAt']
            symbol = None
            reason = None

            # Check if the person is attempting to vote with the template
            if comment[0:7].lower() == "symbol:":
                symbol = comment.split(':')[1].split('<')[0].strip()
                
                # Remove encoding for singe quote
                reason = (comment.split('<br>')[1]).replace("&#39;", "'")
            else:
                # If the comment isn't using the voting template, continue
                continue

            if authorUrl in voters:
                # If the person already voted once, go to next comment
                continue 

            # Keep track of new voter
            voters.append({"voterChannel" : authorUrl, "voter": authorName, "likes": likeCount, "symbol":symbol, "reason": reason, "date": date})
            if symbol not in votes:
                votes[symbol] = 0

            # Count all the comment likes as votes
            votes[symbol] += (1 + likeCount)
        break

countVotes(voters, votes, developerKey, videoId)
summary["date"] = f'{today}'
summary["votesSummary"] = votes
summary["votesActual"] = voters
file.write(json.dumps(summary))