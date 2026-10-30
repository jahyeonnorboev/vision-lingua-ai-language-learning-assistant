VisionLingua --- AI-Powered Visual Language Learning Assistant

VisionLingua is an AI-assisted language learning application designed to help users understand unfamiliar words and text from images. Users can upload an image or enter text directly, extract text with OCR, translate the extracted content, listen to the original and translated text, and use vocabulary-learning tools.

Project documentation is based on the available research notes and application screenshots. Features described as planned or under improvement should not be interpreted as fully completed.

Overview

The project began as an AI-based personalized language-learning assistant. During the planning stage, the team discussed pronunciation assessment, grammar correction, personalized vocabulary lists, spaced repetition, and conversational practice.

As development progressed, the prototype direction focused on a practical visual translation workflow: extracting text from images and helping learners understand and review it. The application interface is titled VisionLingua and describes itself in Korean as a camera-based AI translator.

Main Application Workflow

Upload an image --- Select an image file (JPG, JPEG, or PNG) containing text.
Extract text with OCR --- Choose the OCR language and run text extraction.
Translate --- View the translated result in the results panel.
Listen to the text --- Use text-to-speech controls to listen to the original text and its translation.
Study vocabulary --- The interface includes vocabulary, quiz, learning-statistics, and settings sections.
Users can also enter or paste text directly instead of uploading an image.

Features Visible in the Prototype

Image upload for JPG, JPEG, and PNG files
OCR language selection
Text extraction from an uploaded image
Translation result display
Direct text input as an alternative to image upload
Text-to-speech controls for the original and translated text
Navigation sections for vocabulary, quizzes, learning statistics, and settings
The screenshots confirm the presence of these interface elements. The exact persistence, analytics, and quiz behavior should be documented further only after checking the corresponding implementation.

Team members proposed several project ideas, including a financial-information application, a medical communication application, and an AI-based language-learning assistant. The team selected the language-learning idea proposed by Shohjakhon Norboev.

Initial planning and prototype

The initial concept included:

Pronunciation analysis and feedback
Grammar correction
A personal vocabulary list and spaced repetition
Conversational practice with an AI chatbot
The initial architecture was discussed around speech models such as Whisper or wav2vec2, language models such as BERT or GPT, a FastAPI/Django backend, a React/Next.js frontend, and PostgreSQL/MongoDB.

A UI prototype was also started using React and Tailwind CSS, according to the research notes.

Core learning functions -> The research notes describe implementation work on three learning functions:

Pronunciation assessment: Whisper-based speech-to-text, followed by a text-similarity comparison against a target sentence. The notes identify the /speech/analyze endpoint.
Grammar correction: GPT-based sentence correction and explanations through /grammar/correct.
Vocabulary and review scheduling: A basic vocabulary-management test using temporary data and review intervals of 1, 3, and 7 days.
The notes describe a FastAPI backend using Python 3.10, Whisper and GPT APIs, and SQLite for testing. PostgreSQL integration and the React/Next.js frontend were listed as future work at that point.

Demo review and improvement proposals

During the demo review, the team identified issues with OCR recognition, translation consistency, dictionary API response times, text-to-speech naturalness, and UI usability.

Proposed improvements included:

Image preprocessing with OpenCV, including noise reduction, contrast enhancement, and binarization
Testing OCR pattern customization for mixed-language text
Evaluating Hugging Face MarianMT for context-aware translation
Comparing dictionary services such as Oxford, Cambridge, and Papago
Evaluating more natural TTS options
Improving vocabulary management and spaced-repetition scheduling
Considering web and mobile deployment options
These items are recorded as proposals or future improvements, not confirmed completed features.

The research notes mention the following technologies at different stages of planning and development:

Area Technologies mentioned Status in the available notes

Backend FastAPI, Python 3.10 FastAPI implementation is documented for the October prototype

Speech recognition OpenAI Whisper API Used in the documented pronunciation-analysis prototype

Language correction OpenAI GPT API Used in the documented grammar-correction prototype

Database SQLite; PostgreSQL SQLite used for testing; considered PostgreSQL listed as future work

Frontend React, Next.js, React/Tailwind prototype Tailwind CSS documented; later UI screenshots show the application

OCR improvement OpenCV, Tesseract Proposed during the demo pattern customization review

Translation improvement Hugging Face MarianMT Proposed for evaluation

Text-to-speech Google Cloud TTS, Naver Options discussed; final CLOVA Voice, Mozilla selection is not TTS, ElevenLabs, established by the notes CAMP.AI
Note: The available material does not establish the exact final dependency list or confirm that every technology above is part of the final running application. Update this section after reviewing the source code and dependency files.

Team
Shohjakhon Norboev --- Project idea proposer; contributed to project direction and discussions on OCR, translation, TTS, and learning-system improvements.
Taehoon Lee (이태훈) --- Team member.
Jiwoong Jeon (전지웅) --- Team member.
Screenshots
Add the project screenshots to a docs/images/ directory in this repository, then uncomment and update the paths below.

<!--
![VisionLingua main screen](docs/images/visionlingua-main.png)
![Image upload and OCR](docs/images/visionlingua-ocr.png)
![Translation and text-to-speech](docs/images/visionlingua-translation.png)
-->
Current Limitations and Future Work
The November 3 research notes identify the following areas for improvement:

Improve OCR accuracy for low-light images, distorted characters, and small text.
Improve translation consistency and handling of proper nouns.
Reduce dictionary API latency and improve reliability.
Make TTS voices sound more natural to support pronunciation and intonation learning.
Improve the UI for practical everyday use.
Expand vocabulary management with deletion and review scheduling.
Evaluate spaced repetition for more effective review.
Investigate web and mobile deployment.
The notes mention Streamlit Cloud, Vercel, Flutter Web, and React Native as possible deployment or expansion options. They are proposals, not confirmed deployment targets.

Running the ...

The research notes do not provide a verified final installation procedure or complete dependency list. For that reason, setup commands are intentionally not included here. Add the following after checking the actual repository:

Required runtime and version
Dependency installation command
API keys and environment variables
Local development command
OCR language/data setup, if required
Project Status

This README describes the project using the research notes dated September 17, September 29, October 29, and November 3, 2025, together with the supplied application screenshots. It distinguishes documented prototype work, visible UI elements, and proposed improvements. The final implementation details should be verified against the source code before making stronger technical claims.
