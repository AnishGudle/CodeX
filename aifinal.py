from gpt_index import SimpleDirectoryReader, GPTListIndex, GPTSimpleVectorIndex, LLMPredictor, PromptHelper
from langchain import OpenAI
import sys
import os
import speech_recognition as sr

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

def answerMe(vectorIndex):
    vIndex = GPTSimpleVectorIndex.load_from_disk(vectorIndex)
    recognizer = sr.Recognizer()

    while True:
        print("Please ask your question:")
        with sr.Microphone() as source:
            audio = recognizer.listen(source)

        try:
            prompt = recognizer.recognize_google(audio)
            print(f"You asked: {prompt}")
            response = vIndex.query(prompt, response_mode="compact")
            print(f"Response: {response}\n")
        except sr.UnknownValueError:
            print("Sorry, I could not understand your audio.")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")

answerMe('vectorIndex.json')
