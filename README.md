# InfoEngage: AI-Powered Content Summarization and Interaction Platform
## Overview:

InfoEngage is a Django-based platform that leverages AI technologies to enhance user interaction with digital content. The project focuses on two core functionalities: YouTube video summarization and PDF document interaction through natural language processing (NLP). It allows users to efficiently access summarized information and ask specific questions related to video content or documents, making information consumption faster and more accessible.

## Features:

### YouTube Video Summarization and Chat:
- Users can submit YouTube video URLs to receive concise summaries of video content.
The platform uses Python libraries to fetch video transcripts and integrates with OpenAI's API for summarization.

- Users can interact with the summarized content by asking questions or requesting more details.
PDF Chat with OpenAI:

- Users can upload PDF files and ask questions related to the content.
The platform stores the PDF in OpenAI's file storage system and allows users to query the document using natural language.
The AI-driven assistant processes these queries using NLP techniques, providing precise answers.

## Technologies Used:

- Django: Powers the backend server and user interface, facilitating efficient handling of file uploads and integration with external APIs.
- OpenAI API: Utilized for both summarization of YouTube videos and answering queries related to uploaded PDFs.
- Python Libraries: Used to fetch YouTube video transcripts and manage file uploads.

## User Experience:

- Intuitive and user-friendly interface designed to enhance accessibility and ease of use.
- Sections such as About Us, Contact, Services, and FAQs are included to provide additional information and support.

## Impact and Benefits:

- Efficiency: Quickly access summarized content and precise answers.
- Accessibility: Complex information from diverse sources is made easily understandable.
- Scalability: Django ensures the platform can handle increasing user demands and data volumes effectively.

## Getting Started:
Clone the repository and follow the instructions below to set up the project locally. Ensure you have access to the necessary APIs and keys for integration with OpenAI services.

## INSTALLATION GUIDE 
1. Make sure you have installed latest python version (https://www.python.org/downloads/)

2. Make sure you have visual studio (IDE) installed in your machine

3. Clone this repository

4. create the virtual environment using this command - python -m venv venv

5. Activate the virtual environment - source venv/bin/activate

6. Install all packages at once - pip install -r requirements.txt

7. Now switch to Chatbot folder - cd ./ChatBot/

8. Finally run the project -  python manage.py runserver


#### IMPORTANT: features won't work until you replace the API key with your real API key and real assistant ID.
