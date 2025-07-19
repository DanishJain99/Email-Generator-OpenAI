import os
from dotenv import load_dotenv
from openai import OpenAI
import streamlit as st

load_dotenv()
api_key = os.getenv("OPEN_AI_SECRET_KEY")




def generate_email_content(prompt, tone):

	client = OpenAI(api_key=api_key)

	try:
		response_email_message = [
			        {"role": "system","content": f"You are a professional email assistant. Generate an email for {tone} tone",},
					{"role": "user", "content": prompt }
					]


		response_email = client.chat.completions.create(model="gpt-3.5-turbo", messages=response_email_message, temperature = 0.8)
		email_response = response_email.choices[0].message.content


		response_subject_line_message = [
			        {"role": "system","content": "Generate a concise and appropriate subject line for this email."},
					{"role": "user", "content": email_response }
					]
		response_subject_line = client.chat.completions.create(model="gpt-3.5-turbo", messages=response_subject_line_message, temperature = 0.8)
		subject_line =  response_subject_line.choices[0].message.content


		response_summary_message = [
            {"role": "system", "content": "Provide a concise summary of the email thread."},
            {"role": "user", "content": f"Original thread:\n{prompt}\n\nResponse:\n{email_response}"}
        ]

		respone_summary = client.chat.completions.create(model="gpt-3.5-turbo", messages=response_summary_message, temperature = 0.8)
		summary_message = respone_summary.choices[0].message.content

		return {
            "error": None,
            "response": email_response,
            "subject": subject_line,
            "summary": summary_message
        }
	except Exception as e:
		return {
            "error": str(e),
            "response": None
        }


def main():
	st.set_page_config(page_title= "Email Generator using OpenAI", layout = "wide")
	st.markdown("Generate Email with different tones")


	# Main content area
	col1, col2 = st.columns([1, 1])
	with col1:
		st.subheader("Input")

		# Email thread input
		email_thread = st.text_area(
            "Enter the email thread (most recent at top)",
            height=200,
            placeholder="""Example email:
			Hi team,
			Can we schedule a meeting to discuss the quarterly report? I've noticed some interesting trends that I'd like to explore further.
			Best regards,
			Danish"""
        )

		# Tone selection
		tone_options = ["Professional", "Casual", "Friendly", "Formal"]
		selected_tone = st.selectbox("Select tone", tone_options)

		# Context input
		additional_context = st.text_area(
            "Additional context or specific points to address (optional)",
            height=100,
            placeholder="Example: Need to highlight the positive growth trend in Q3..."
        )

		# Generate button
		if st.button("Generate Response", type="primary"):
			if not email_thread:
				st.error("Please enter an email thread.")
				return
			
			with st.spinner("Generating response..."):
				prompt = f"Email Thread:\n{email_thread}\n\nAdditional Context:\n{additional_context}\n\nGenerate a {selected_tone.lower()} tone response."

				# Generate content
				result = generate_email_content(prompt, selected_tone)
				
				if result["error"]:
					st.error(result["error"])
				else:
					st.session_state.current_response = result
					st.success("Response generated successfully!")

	
	with col2:
		st.subheader("✨ Generated Content")
		if 'current_response' in st.session_state:
			content = st.session_state.current_response
			st.markdown("Subject Line:")
			st.code(content["subject"], language=None)
			st.markdown("Email Response:")
			st.code(content["response"], language=None)
			st.markdown("Thread Summary:")
			st.code(content["summary"], language=None)
			st.markdown(f"*Tone: {selected_tone}*")







if __name__ == "__main__":
	main()




