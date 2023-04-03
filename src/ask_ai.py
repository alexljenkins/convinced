import openai

def get_api_key(filepath):
    with open(filepath, "r") as txt_file:
        return txt_file.readlines()[0]


def ask_ai(user_input):
    # Set up the prompt for the OpenAI API
    prompt = f"User: {user_input}\nChatbot:"

    try:
        # Generate the response using the OpenAI API
        response = openai.Completion.create(
            engine="davinci",
            prompt=prompt,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.0,
        )
    except openai.error.RateLimitError as E:
        return "I'm too tired to deal with you today. Someone will have to pay me to keep listening to you..."
    except openai.error.InvalidRequestError as E:
        return "I have no idea what you're even talking about."
    except Exception as E:
        return "Oh no! My brain's stopped working... Too bad for you!"
    # Return the generated response
    return response.choices[0].text.strip()