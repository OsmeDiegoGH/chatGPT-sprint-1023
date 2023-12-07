from dotenv import load_dotenv

from chat_gpt import ChatGPT
from textwrap import dedent

from trainee import Trainee

gym_equipment = {
    1: "Treadmill",
    2: "Elliptical Machine",
    4: "Rowing Machine",
    5: "Stair Climber",
    6: "Spin Bike",
    8: "Smith Machine",
    9: "Leg Press Machine",
    10: "Cable Machine",
    11: "Abdominal Machine",
    12: "Free Weights (Dumbbells and Barbells)",
    13: "High/Low Pulley Machine",
    14: "Chest Press Machine",
    15: "Leg Extension Machine",
    16: "Bicep Curl Machine",
    17: "Leg Curl Machine",
    19: "Ab Coaster",
    20: "Glute Machine",
    21: "Functional Training Equipment",
    22: "Bosu Ball",
    23: "Medicine Balls",
    24: "TRX (Suspension Training)",
}

training_levels = {
    1: {
        "name": "Beginner",
        "training_days_per_week": 3,
        "description": "I am just starting on this Fitness world, or I used to do exercise but now I'm taking my path "
                       "again. Let's start calmed but with all the Energy."
    },
    2: {
        "name": "Intermediate",
        "training_days_per_week": 5,
        "description": "I have being training for a couple of months. I still have to get used to the exercise routine "
                       "so my body can recover when doing heavy routines."
    },
    3: {
        "name": "Advanced",
        "training_days_per_week": 7,
        "description": "I have no fear, I'm a exercise machine, I need to work out otherwise I feel incomplete. Pain "
                       "is temporary, pride is forever!!"
    }
}

goals = {
    1: {
        "name": "Weight Loss",
        "training_days_per_week": 3,
        "description": "I want to look as my old years, I dont care about having big muscles or running a marathon."
    },
    2: {
        "name": "Muscle Building (Hypertrophy)",
        "training_days_per_week": 5,
        "description": "I want to show my muscles wherever I go, I like how muscles make you look aesthetic"
    },
    3: {
        "name": "Endurance and Cardiovascular Health (Sports)",
        "training_days_per_week": 7,
        "description": "I want to focus on Sports, I like fast and explosive exercises"
    }
}


def get_int_input(console_message, expected_answers=None):
    while True:
        response = input(console_message)
        try:
            int_response = int(response)
            if expected_answers is not None and int_response not in expected_answers:
                raise ValueError(f'Unexpected int {int_response}')
            break
        except ValueError:
            print("Ups, your response is not a valid number, please answer again\n")

    return int_response


def get_float_input(console_message):
    while True:
        response = input(console_message)
        try:
            float(response)
            break
        except ValueError:
            print("Ups, your response is not a valid decimal, please answer again\n")

    return float(response)


def get_string_input(console_message, expected_answers):
    while True:
        response = input(console_message)
        if response is not None and response.lower() in expected_answers:
            break

        print("Ups, your response are not the one expected, please answer again\n")

    return response


class TrainingAssistant:

    def __init__(self):
        self.chat_gpt = ChatGPT()
        self.trainee = None

    def start(self):
        self.print_welcome_message()
        self.collect_trainee_data()
        self.build_routine()

    def print_welcome_message(self):
        welcome_message = dedent('''
        Hi, I am your Training Assistant, and I will help you achieve your goals.
        First, lets collect some information about you and your Gym environment so I can bring you the most effective
        way to help you rock inside the Fitness world.        
        ''')
        print(welcome_message)

    def collect_trainee_data(self):
        self.trainee = Trainee()
        self.collect_age()
        self.collect_weight()
        self.collect_height()
        self.collect_level()
        self.collect_goal()
        self.collect_equipment()

    def collect_age(self):
        trainee_age = get_int_input("Please share me your age (I promise I wont tell anyone else about it)\n")

        if trainee_age < 14:
            input(
                "Hey looks like you are under the recommended age to train, I will help you when you are older than 14, Best wishes")
            exit(0)

        self.trainee.age = trainee_age

    def collect_weight(self):
        self.trainee.weight = get_float_input("Please share me your weight in Kg (again I will be a closed tomb)\n")

    def collect_height(self):
        self.trainee.height = get_float_input("Please share me your height in Cm (Are we ok with this, right?)\n")

    def collect_level(self):
        print("Thanks for sharing me your current info, now let's see your background and your specific goals\n")
        level_message = "Let's talk about your actual physical condition. Could you specify on which level you feel more comfortable\n"
        for level_id in training_levels.keys():
            level_message += '\n{}. {}'.format(level_id, training_levels[level_id]['description'])

        level_message += '\nPlease answer ({})\n'.format(','.join(str(x) for x in training_levels.keys()))
        self.trainee.level = get_int_input(level_message, list(training_levels.keys()))

    def collect_goal(self):
        goal_message = "Cool, now I know your current situation. Now, please share me what is your main goal you want to achieve"
        for goal_id in goals.keys():
            goal_message += '\n{}. {}'.format(goal_id, goals[goal_id]['description'])
        goal_message += '\nPlease answer ({})\n'.format(','.join(str(x) for x in goals.keys()))
        self.trainee.goal = get_int_input(goal_message, list(goals.keys()))

    def collect_equipment(self):
        select_equipment = get_string_input(
            "I have the option to specify Gym equipment to select for the routine generation, "
            "Would you like it to do it?\n", ["y", "n", "yes", "no"]
        )
        if select_equipment.lower() in ["n", "no"]:
            print("Got it, no ask about equipment then")
            self.trainee.gym_equipment = list(gym_equipment.keys())
            return

        print("Ok, so let's start with the equipment selection")

        equipment_ids = []
        for equipment_id in gym_equipment.keys():
            have_equipment = get_string_input(
                "On your gym, do you have access to {}? (y/n)".format(gym_equipment[equipment_id]),
                ["y", "n", "yes", "no"]
            )
            if "y" == have_equipment:
                equipment_ids.append(equipment_id)

        self.trainee.gym_equipment = equipment_ids

    def build_routine(self):
        print("Now I have all the information I need to suggest you your workout routine, let's do it")

        equipment_list = ','.join(gym_equipment[equipment_id] for equipment_id in self.trainee.gym_equipment)
        message = [
            f'My age is {self.trainee.age},',
            f'My weight is {self.trainee.weight} kg,',
            f'My height is {self.trainee.height} cm,',
            '{} and I want to train {} times a week,'.format(
                training_levels[self.trainee.level]['description'],
                training_levels[self.trainee.level]['training_days_per_week']
            ),
            '{},'.format(goals[self.trainee.goal]['description']),
            f'I have following equipment in my gym to use {equipment_list}',
            'Can you build a monthly routine'
        ]
        gpt_messages = [
            {
                "role": "system",
                "content": "You are a skilled personal fitness trainer"
            },
            {
                "role": "system",
                "content": ','.join(message)
            }
        ]
        print(self.chat_gpt.request_openai(gpt_messages))

        print(dedent('''
        Feel free to modify any information you already shared to me so your workout routines can fulfill your goals
        based on your actual situation
        '''))


# Use this method to directly test assistance providing specific  by-passing console input
if __name__ == "__main__":
    load_dotenv()

    training_assistant = TrainingAssistant()
    training_assistant.trainee = Trainee()
    training_assistant.trainee.age = 33
    training_assistant.trainee.weight = 66
    training_assistant.trainee.height = 1.59
    training_assistant.trainee.level = 2
    training_assistant.trainee.goal = 2
    training_assistant.trainee.gym_equipment = list(gym_equipment.keys())
    training_assistant.build_routine()
