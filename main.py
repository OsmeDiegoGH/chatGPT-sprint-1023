#!/usr/bin/env python3

from dotenv import load_dotenv

from training_assistant import TrainingAssistant

# Load environment variables from the .env file
load_dotenv()


def start_training_assistant():
    training_assistant = TrainingAssistant()
    training_assistant.build_routine()


if __name__ == "__main__":
    start_training_assistant()
