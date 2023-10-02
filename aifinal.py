from gpt_index import SimpleDirectoryReader, GPTListIndex, GPTSimpleVectorIndex, LLMPredictor, PromptHelper
from langchain import OpenAI
import sys
import os
import speech_recognition as sr
import time
import openai  # Add this line

os.environ["OPENAI_API_KEY"] = "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"

def createVectorIndex(path):
    max_input = 4096
    tokens = 256
    chunk_size = 600
    max_chunk_overlap = 20

    prompt_helper = PromptHelper(max_input, tokens, max_chunk_overlap, chunk_size_limit=chunk_size)

    #define LLM
    llmPredictor = LLMPredictor(llm=OpenAI(temperature=0, model_name="text-ada-001", max_tokens=tokens))
    docs = SimpleDirectoryReader(path).load_data()
    vectorIndex = GPTSimpleVectorIndex(documents=docs, llm_predictor=llmPredictor, prompt_helper=prompt_helper)
    vectorIndex.save_to_disk('vectorIndex.json')
    return vectorIndex

vectorIndex = createVectorIndex('knowledge')

def get_response(prompt, vIndex):  # Add vIndex as an argument
    while True:
        try:
            response = vIndex.query(prompt, response_mode="compact")
            return response
        except openai.error.RateLimitError:  # Now openai is recognized
            print("Rate limit exceeded, waiting for 60 seconds before retrying.")
            time.sleep(60)

def answerMe(vectorIndex):
    vIndex = GPTSimpleVectorIndex.load_from_disk(vectorIndex)
    recognizer = sr.Recognizer()

    while True:
        input_type = input("Do you want to provide voice input or text input? (v/t): ").lower()
        if input_type == 'v':
            print("Please ask your question:")
            with sr.Microphone() as source:
                audio = recognizer.listen(source)

            try:
                prompt = recognizer.recognize_google(audio)
                print(f"You asked: {prompt}")
            except sr.UnknownValueError:
                print("Sorry, I could not understand your audio.")
                continue
            except sr.RequestError as e:
                print(f"Could not request results from Google Speech Recognition service; {e}")
                continue
        elif input_type == 't':
            prompt = input("Please ask your question: ")
        else:
            print("Invalid option. Please enter 'v' for voice input or 't' for text input.")
            continue

        response = get_response(prompt, vIndex)  # Pass vIndex to get_response
        print(f"Response: {response}\n")

answerMe('vectorIndex.json')
