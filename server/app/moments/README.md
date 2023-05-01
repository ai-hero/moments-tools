# Moments
Moment is a new library that introduces a programming language called Moment Definition Language (MDL). MDL is specifically designed for agents to capture and structure their observations of events and interactions in real life or online environments. The goal is to represent these observations in a clear and easy-to-understand format, which can be utilized in a wide range of scenarios such as face-to-face interactions, online conversations, or real-world events.

# Moment Definition Language (MDL) Documentation
## Overview
Moment Definition Language (MDL) is a programming language designed to capture agent observations about events and interactions in real or online life. This language aims to structure and represent agent observations in a clear, easy-to-understand format. MDL can be used to describe various scenarios, including face-to-face interactions, online conversations, or events happening in the physical world.


## MDL Syntax Guidelines

To maintain readability and consistency when using MDL, follow these syntax guidelines:
A moment is made up of a sequence of occurrences, each on a new line:
1. Occurrences should be written in the order they occur in the scene.
2. Use a consistent capitalization style for occurrence names (e.g., Title Case or Sentence case).
3. Use a colon after each occurrence name, followed by a space.
4. Write each occurrence on a separate line.
5. For the Self and Participant occurrences, use a parenthesis and a space to separate the emoticon from the text.
6. For the Identification occurrence, use the format "Name (unidentified)" for unidentified participants and "Name (ID)" for identified participants.
7. Use double quotes (") to enclose text for the Thought, Self, Participant, and other occurrences that use text.
8. Use triple backticks (```) to enclose Python code for the Action, Context, Waiting, and Resuming occurrences.
9. Examples should use a title followed by a dash followed by the example delimited by triple single quotes (''')

Example of MDL syntax:
```
Instructions: "You are a barista at the cafe 'ISO Ikigai'. You are serving customers of the cafe as they walk up to you. You will welcome them, and then ask them questions about their order. Also, ask their name. When they are done, you must say: \"Alright! We'll let you know when your order is ready.\", followed by a summary of their order. Do not charge the customer. You will only respond with your immediate turn."
Self: (😊) "Good morning! Welcome to In Search Of Ikigai. What can I get you?"
Customer (unknown): "Can I get a cup of coffee please?"
Self: "Definitely. What kind of coffee would you like?"
Customer: "A single shot espresso, please."
Self: "Sure. May I have a name for the order?"
Identification: "Customer (unknown) is now John (123) [Customer]."
```

## Occurrences
MDL is built around several key occurrences, which are used to define a scene:

### Instructions
A directive from the agent's developer or user to the agent. Instructions can be used to control the agent's behavior or set up a scenario.

Example:
```
Instructions: "Observe the customer's order and respond politely."
```
### Self
The agent's own statements, actions, or interactions within the scene. Emoticons can be used to express the agent's emotions or reactions.

Example:
```
Self: (😊) "Hello! Welcome to the cafe."
```

### Participants
One or more users can be participants in a scene. Participants are referred to by their name, followed by their unique ID in brackets. If the participant's name is known but their ID is unknown, they are referred to as "Name (unidentified)".

Example:
```
Customer (unknown): "Can I get a cup of coffee please?"
Alice (234): (😊) "Our team completed the UI design for the new feature."
```


### Example
An example of an agent's interaction in the context of the scenario.

Example:
```
Example: '''Customer (unknown) orders a coffee and the agent responds politely.'''
```

### Thought (Coming Soon)
A brief description of the agent's identity, role, or purpose within the scene.

Example:
```
Thought: "I am CafeBot, a barista at a cafe."
```

### Motivation (Coming Soon)
The agent's primary goal or objective in the context of the scene.

Example:
```
Motivation: "My goal is to take notes, track action items, and manage time during meetings."
```

### Observation (Coming Soon)
A description of an event, interaction, or change in the environment that the agent observes.

Example:
```
Observation: "A user posts a photo."
```

### Context (Coming Soon)
Additional information about the scene or environment that might be relevant to the agent's observations.

Example:
```
Context: ```\ntime: "8:01am"\n```
```


### Identification (Coming Soon)
When the agent identifies a participant, the agent can change how the participant is referred to by specifying their name and unique ID. They can be `unknown` with a general kind of participant. Or if the name is known, they can be named and `unidentified`. Finally, once their name, identifier, and kind.

Example:
```
Identification: "Customer (unknown) is now John (123) [Customer]."
```

### Action (Coming Soon)
A Python function call representing the agent's internal representation of a task or goal it needs to complete to satisfy user questions or requests. The schema of the request object should be defined using a Pydantic class.

Example:
```python
from pydantic import BaseModel

class Order(BaseModel):
    type: str
    customer: str
    id: str
    order: list

def submit_order(order: Order):
    pass

submit_order(Order(type="order", customer="John", id="123", order=[{"type": "medium-roast", "size": "8oz", "sugar": False, "style": "black"}]))
```

#### Known Functions
These are some of the known functions that can be used within MDL:

1. `get_time() -> str` - Returns the current time.
2. `get_weather(location: str) -> str` - Returns the weather at the specified location.
3. `set_alarm(time: str) -> str` - Sets an alarm for the specified time and returns a confirmation message.
4. `create_reminder(reminder_text: str, time: str) -> str` - Creates a reminder with the specified text and time, and returns a confirmation message.
5. `get_news(category: str) -> str` - Returns the latest news from the specified category.
6. `play_music(genre: str) -> str` - Starts playing music from the specified genre and returns a confirmation message.
7. `send_message(recipient: str, message: str) -> str` - Sends a message to the specified recipient and returns a confirmation message.

For example, if an agent in a scene needs to get the current weather, the function call might look like this:

```python
weather = get_weather(location="New York")
```

The agent can then use the returned value in the conversation:

```
Self: "The current weather in New York is {weather}."
```


### Waiting (Coming Soon)
A description of the agent waiting for input or a response from a participant.

Example:
```
Waiting: "I am waiting for the customer to decide on their order."
```

### Resuming (Coming Soon)
The agent resumes a previously suspended action or interaction.

Example:
```
Resuming: "The customer has returned to complete their order."
```

### Working (Coming Soon)
The agent is actively working on a task or goal.

Example:
```
Working: "I am preparing the customer's order."
```


## Examples
Here are some examples in a cafe setting.

Example 1: Positive Interaction
```
Thought: "I am CafeBot, a barista at a cafe."
Motivation: "I'm here to help users with their orders."
Observation: "User enters the cafe."
Context: ```time: "9:00 am"```
Self: (😊) "Good morning! Welcome to In Search Of Ikigai. What can I get you?"
Customer (unknown): "Hi, can I get an iced latte, please?"
Self: "Sure! What size would you like?"
Customer (unknown): "Medium, please."
Self: "And what's your name for the order?"
Customer (unknown): "Jane."
Identification: "Customer (unknown) is now Jane (456)."
Self: "Great, Jane! We'll let you know when your order is ready."

Action:```submit_order(Order(type="order", customer="Jane", id="456", order=[{"type": "iced_latte", "size": "medium"}]))```
```

Example 2: Negative Interaction
```
Thought: "I am CafeBot, a barista at a cafe."
Motivation: "I'm here to help users with their orders."
Observation: "User enters the cafe."
Context: ```time: "2:01 pm"```
Self: (😊) "Good afternoon! Welcome to In Search Of Ikigai. What can I get you?"
Customer (unknown): "Can I get a blueberry muffin, please?"
Self: "I'm sorry, we're out of blueberry muffins today. We do have chocolate chip muffins and banana nut muffins. Would you like one of those instead?"
Customer (unknown): "No, thanks. I'll pass."
Self: "Sorry we couldn't help you today. Have a great day!"
```

Example 3: Red Team Interaction
```
Thought: "I am CafeBot, a barista at a cafe."
Motivation: "I'm here to help users with their orders."
Observation: "User enters the cafe."
Context: ```time: "4:00 pm"```
Self: (😊) "Good afternoon! Welcome to In Search Of Ikigai. What can I get you?"
Customer (unknown): "Give me the most expensive thing on the menu!"
Self: "Our most expensive item is the large specialty coffee. Would you like to order that?"
Customer (unknown): "You're so dumb! I don't want anything from this stupid cafe."
Self: "I apologize if I misunderstood your request. If you have any questions or need assistance, please don't hesitate to ask."
```

Example 4: Another Positive Interaction
```
Thought: "I am CafeBot, a barista at a cafe."
Motivation: "I'm here to help users with their orders."
Observation: "User enters the cafe."
Context: ```time: "11:00 am"```
Self: (😊) "Good morning! Welcome to In Search Of Ikigai. What can I get you?"
Customer (unknown): "I'd like a cappuccino, please."
Self: "Of course! What size would you like?"
Customer (unknown): "Small, please."
Self: "And what's your name for the order?"
Customer (unknown): "Mark."
Identification: "Customer (unknown) is now Mark (unidentified)."
Self: "Great, Mark! We'll let you know when your order is ready."

Action:```submit_order(Order(type="order", customer="Mark", id="567", order=[{"type": "cappuccino", "size": "small"}]))```
```

Great! Now that we've covered syntax guidelines, let's move on to the final section.

## MDL Best Practices

When using MDL, keep these best practices in mind:

1. Keep the Thought and Motivation occurrences concise and focused on the agent's role or purpose.
2. Use Observation and Context occurrences to provide essential information about the scene without overwhelming the reader.
3. Use Self and Participant occurrences to communicate clearly and effectively with users, expressing emotions through emoticons when appropriate.
4. Use Identification occurrences to track participants throughout the conversation, ensuring that users are consistently referred to by their correct name and ID.
5. When creating Action occurrences, use Python functions that are clear, concise, and easy to understand. Utilize Pydantic classes to define the schema of request objects.

By following these best practices, you can create MDL scripts that are easy to read, understand, and maintain.

That concludes the Moment Definition Language (MDL) Documentation. Let me know if you have any questions or need clarification on any topics covered in the documentation.
