import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure the Gemini API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Select the Gemini model
# The model name might have changed, try using the full name with version
model = genai.GenerativeModel('models/gemini-2.0-flash')

def extract_key_details(plot, title):
    """
    Extract key details from a movie plot using Google Gemini.

    Args:
        plot (str): The original movie plot
        title (str): The movie title

    Returns:
        str: The extracted key details
    """
    try:
        # Create a prompt for the Gemini API
        prompt = f"""
        Extract the key details from the following movie plot:

        Movie Title: {title}

        Original Plot: {plot}

        Key Details:
        """

        # Call the Gemini API
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                candidate_count=1,
                max_output_tokens=200,
                temperature=0.7,
                top_p=1.0)
        )

        # Extract and return the extracted key details
        key_details = response.candidates[0].content.parts[0].text.strip()
        return key_details

    except Exception as e:
        print(f"Gemini API error: {str(e)}")
        return f"Error extracting key details: {str(e)}"


def generate_parody(key_details, title):
    """
    Generate a parody of a movie plot using Google Gemini.

    Args:
        key_details (str): The key details of the movie plot
        title (str): The movie title

    Returns:
        str: The generated parody
    """
    try:
        # Create a prompt for the Gemini API
        prompt = f"""
        Generate a hilarious and SHORT parody of the following movie plot, using the key details provided. Your parody should:
        - Use ridiculous character names.
        - Exaggerate plot elements to absurd extremes.
        - Insert illogical plot twists.
        - Include a running gag.
        - Reference pop culture unexpectedly.
        - Point out plot holes.
        - Replace dramatic moments with mundane concerns.
        - Add some dark humor.

        The parody should be max 3 sentences. Make it ridiculously funny with great punchlines and dark humor.

        Movie Title: {title}

        Key Details: {key_details}

        Parody:
        """

        # Call the Gemini API
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                candidate_count=1,
                max_output_tokens=500,
                temperature=0.9,  # Higher values make output more random
                top_p=1.0)
        )

        # Extract and return the generated parody
        parody = response.candidates[0].content.parts[0].text.strip()
        return parody

    except Exception as e:
        print(f"Gemini API error: {str(e)}")
        return f"Error generating parody: {str(e)}"


def review_parody(parody, feedback="Make it funnier and shorter"):
    """
    Review a parody using Google Gemini and regenerate it based on the feedback.

    Args:
        parody (str): The parody to review
        feedback (str): The feedback to use for regeneration

    Returns:
        str: The regenerated parody
    """
    try:
        # Create a prompt for the Gemini API
        prompt = f"""
        Review the following movie parody and regenerate it based on the feedback provided:

        Parody: {parody}

        Feedback: {feedback}

        Regenerated Parody:
        """

        # Call the Gemini API
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                candidate_count=1,
                max_output_tokens=500,
                temperature=0.8,
                top_p=1.0)
        )

        # Extract and return the regenerated parody
        regenerated_parody = response.candidates[0].content.parts[0].text.strip()
        return regenerated_parody

    except Exception as e:
        print(f"Gemini API error: {str(e)}")
        return f"Error regenerating parody: {str(e)}"

# Alternative implementation for reference
"""
def generate_parody_alternative(key_details, title):
    try:
        # Create a prompt for the Gemini API
        prompt = f'''
        Generate an absolutely hilarious parody of the following movie. Your parody should:
        - Use ridiculous character names that sound similar to the originals but are comically absurd
        - Exaggerate the most serious plot elements to absurd extremes
        - Insert completely illogical plot twists that make no sense but are very funny
        - Include at least one running gag or catchphrase
        - Reference other movies or pop culture in unexpected ways
        - Point out plot holes or movie clichés in a meta, fourth-wall-breaking way
        - Replace dramatic moments with mundane, everyday concerns

        The parody should be 3-5 sentences long and maintain the core story elements while making them ridiculous.

        Movie Title: {title}

        Key Details: {key_details}

        Parody:
        '''

        # Call the Gemini API
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                candidate_count=1,
                max_output_tokens=500,
                temperature=0.9,
                top_p=1.0)
        )

        # Extract and return the generated parody
        parody = response.candidates[0].content.parts[0].text.strip()
        return parody

    except Exception as e:
        print(f"Gemini API error: {str(e)}")
        return f"Error generating parody: {str(e)}"
"""
