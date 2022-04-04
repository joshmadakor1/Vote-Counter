from asyncio.subprocess import SubprocessStreamProtocol
import key
from googleapiclient.discovery import build

voters = {}
votes = {}
explanations = {}
videoId = "Zu8qMuhsEso"

def countVotes(voters, votes, explanations, apiKey, videoId):
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
            author = item['snippet']['topLevelComment']['snippet']['authorChannelUrl']
            likeCount = item['snippet']['topLevelComment']['snippet']['likeCount']
            symbol = None
            explanation = None

            # Check if the person is attempting to vote with the template
            if comment[0:7].lower() == "symbol:":
                symbol = comment.split(':')[1].split('<')[0].strip()
                explanation = comment.split('<br>')[1]
            else:
                # If the comment isn't using the voting template, continue
                continue

            if author in voters:
                # If the person already voted once, go to next comment
                continue 

            # Keep track of new voter
            voters[author] = True
            if symbol not in votes:
                votes[symbol] = 0
                explanations[symbol] = list()

            votes[symbol] += (1 + likeCount)
            explanations[symbol].append(explanation)
        break

countVotes(voters, votes, explanations, key.developerKey, videoId)

print("Voters: ",voters)
print("Votes: ", votes)
print("Explanations: ", explanations)