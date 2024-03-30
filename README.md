# AI Tutor Flask App

This is a Flask application that serves as an AI tutor. It uses the OpenAI GPT-3.5 model to answer questions and provides relevant YouTube video links based on the user's query.

## Table of Contents
- [Overview](#overview)
- [Usage](#usage)
- [Endpoints](#endpoints)


## Overview
The AI tutor Flask app utilizes the OpenAI GPT-3.5 model to generate responses to user questions. It also integrates with the YouTube API to search for relevant videos based on the user's query.

## Usage
The AI tutor Flask app utilizes the OpenAI GPT-3.5 model to generate responses to user questions. It also integrates with the YouTube API to search for relevant videos based on the user's query.
Start the Flask server:
- python app.py
Send POST requests to the /asks endpoint with a JSON payload containing the user's question:
- curl -X POST -H "Content-Type: application/json" -d '{"question": "What is the capital of France?"}' http://localhost:5000/asks

## Usage
POST /asks: Receive a question from the user and return an answer along with relevant YouTube video links.




