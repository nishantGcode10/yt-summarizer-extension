#import flask
from flask import Flask,jsonify,request,json
from youtube_transcript_api import YouTubeTranscriptApi
from transformers import pipeline
import urllib.parse as urlparse
from flask_cors import CORS
app =Flask(__name__)
CORS(app)
#homepage endpoint
@app.route('/',methods =["GET"])
def main():
    return jsonify("hello")


#landing page after submit button
@app.route('/link',methods = ["GET","POST"])
def fetchLink():
  try:
    if request.method =="POST":
        request_data=json.loads(request.data)
        percent = request_data["percent"]
        
        percent = int(percent)
        try:
          url=request_data['content']

          url_data = urlparse.urlparse(url)
          query = urlparse.parse_qs(url_data.query)
          video_id = query["v"][0]
          return fetchSummary(video_id,percent)
        
        except:
          return jsonify("invalid url")
    return "hello"
  except:
    return jsonify('Network error')



# function for summarization of the video recieved by the form through post request
def fetchSummary(vid_id, percentage):
  try:
    transcript=YouTubeTranscriptApi.get_transcript(vid_id)
    result = ""
    for i in transcript:
      result += ' ' + i['text']
    num_iters = int((len(result)*(percentage/100))/1000)
    summarized_text = []
    summarization=pipeline("summarization")
    for i in range(0, num_iters + 1):
      start = 0
      start = i * 1000
      end = (i + 1) * 1000
      if end-start>1000:
        return "Video too big to summarize"
      out = summarization(result[start:end])
      out = out[0]
      out = out['summary_text']
      summarized_text.append(out)

    return jsonify(summarized_text)
  except:
    return jsonify("Monkey")
if __name__=='__main__':
  app.run()


