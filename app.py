import streamlit as st
import google.generativeai as genai
import os
from youtube_transcript_api import YouTubeTranscriptApi

# Load the API key from environment variables
key = os.getenv("Gemini_API_Key")

# Check if the API key is set
if key is None:
    st.error("API key is not set. Please set the Gemini_API_Key environment variable.")
else:
    # Configure the generative AI model with the API key
    genai.configure(api_key=key)

    prompt = """
    You are a YouTube video summarizer. You will be taking the transcript text
    and summarizing the entire video and providing the important summary in points
    within 250 words. Please provide the summary of the text given here:  
    """

# Configure the generative AI model with the API key
    
    fields = {
            "temperature": 1,
            "top_p": 0.95,
            "top_k": 64,
            "max_output_tokens": 8192,
            #"response_mime_type": "text/plain"
        }

        # Assuming GenerativeModel is the correct class to use
    llm = genai.GenerativeModel(
            model_name="gemini-1.5-pro",
            generation_config=fields
        )


## getting the transcript data from yt videos
def extract_transcript_details(youtube_video_url):
    try:
        video_id=youtube_video_url.split("=")[1]
        
        transcript_text=YouTubeTranscriptApi.get_transcript(video_id)

        transcript = ""
        for i in transcript_text:
            transcript += " " + i["text"]

        return transcript

    except Exception as e:
        raise e
    
   

    
## getting the summary based on Prompt from Google Gemini Pro
def generate_gemini_content(transcript_text,prompt):

    #model=genai.GenerativeModel("gemini-pro")
    response=llm.generate_content(prompt+transcript_text)
    return response.text

st.header('YouTube Transcript to Detailed Notes Converter:beginner:', divider='rainbow')
youtube_link = st.text_input("Enter YouTube Video Link:")

if youtube_link:
    video_id = youtube_link.split("=")[1]
    print(video_id)
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)

if st.button("Get Detailed Notes"):
    transcript_text=extract_transcript_details(youtube_link)

    if transcript_text:
        summary=generate_gemini_content(transcript_text,prompt)
        st.markdown("## Detailed Notes:")
        st.write(summary)


if __name__ == "__main__":
    main()