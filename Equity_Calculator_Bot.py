import os
import streamlit as st
from openai import OpenAI

# Load API key from environment variables.
# Replace "your-api-key-here" with your actual API key if not using environment variables.
api_key = os.getenv("OPENAI_API_KEY", "your-api-key-here")

# Initialize the OpenAI client.
client = OpenAI(api_key=api_key)

def get_equity_answer(prompt):
    """Send the prompt to the OpenAI API and return the generated answer."""
    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        # Debug: Print the API response structure.
        print("API Response:", completion)

        # Return the content of the first message.
        return completion.choices[0].message.content

    except Exception as e:
        error_message = str(e)
        if "Rate limit" in error_message:
            return "Error: API quota exceeded. Check your OpenAI usage and billing."
        elif "Incorrect API key" in error_message:
            return "Error: Invalid API key. Please check your API key settings."
        else:
            return f"Unexpected Error: {error_message}"

# Streamlit UI
st.title("🤖 Equity Calculator Bot")

st.markdown("### Equity Breakdown by Contribution Areas")
default_breakdown = """Employee Stock Pool: 10%
Monetary Capital Contributions: 40%
Corporate Operation Contributions: 40%
Business Idea Ownership: 10%"""
equity_breakdown = st.text_area("Enter the equity breakdown by contribution areas:", default_breakdown, height=100)

st.markdown("### Equity Breakdown by Team Member")
default_team = """Bryan:
  Monetary Capital Contributions: 100%
  Corporate Operation Contributions: 50%
  Business Idea Ownership: 100%
Chris:
  Corporate Operation Contributions: 50%"""
team_breakdown = st.text_area("Enter the equity breakdown by team member:", default_team, height=120)

st.markdown("### Ask Your Equity Question")
question = st.text_input("Enter your equity calculation question:", "What's the total equity for Bryan?")

if st.button("Calculate Equity"):
    # Construct the prompt with all the provided information.
    prompt = f"""Using the following equity breakdowns, calculate the answer to the question.

Equity breakdown by contribution areas:
{equity_breakdown}

Equity breakdown by team member:
{team_breakdown}

Question: {question}

Please provide a detailed explanation along with the final total equity for the team member.
"""
    st.write("Processing...")
    answer = get_equity_answer(prompt)
    st.markdown("### Answer")
    st.write(answer)
