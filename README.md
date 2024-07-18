# Calendar Co-Pilot

Welcome to Calendar Co-Pilot! This application simplifies the process of setting tutor availability for an online tutoring platform by using natural language input and AI-driven parsing.

## Objective

The objective is to help tutors easily create their availability schedules in a marketplace that connects them to students, by leveraging AI to understand natural language descriptions of availability.

## Estimated Time of Development

- Development: 6-8 hours
- Testing: 4 hours

## Skills Tested

- Prompt Engineering
- NoSQL (MongoDB) Database Design
- API Design
- Interface Design

## Problem Statement

Tutors frequently need to update their availability schedules. Doing this manually via a traditional calendar interface can be cumbersome. The goal of this project is to create a system that can interpret a tutor's natural language description of their availability and convert it into a structured calendar format for display and storage.

## Solution Overview

The system will:
1. Take a natural language input describing the tutor's availability.
2. Use Generative AI to parse this input and create a structured calendar proposal.
3. Present this proposal for tutor confirmation.
4. Save the confirmed availability schedule to a MongoDB database.

## Infrastructure

1. **Database**: Set up a free MongoDB cluster.
2. **Web Page**: Create a simple web interface where a tutor can enter their availability.
3. **APIs**: Use FastAPI to create APIs for creating tutors, getting their availability, and saving updated availability.

### Tools Used

- **FastAPI**: A modern Python web framework for building APIs.
- **MongoDB**: A NoSQL database to store tutor profiles.
- **OpenAI GPT**: To parse natural language input and generate structured availability.
- **Bootstrap**: For front-end styling.
- **dotenv**: For managing environment variables.

## Project Structure

```plaintext
.
├── app.py                 # FastAPI backend application
├── index.html             # Front-end HTML file
├── .env                   # Environment variables (for OpenAI and MongoDB credentials)
└── README.md              # This README file
```

## API Endpoints

### Create Tutor

**Endpoint**: `/create-tutor`  
**Method**: `POST`  
**Request Body**:
```json
{
  "username": "tutor_username"
}
```
**Response**:
```json
{
  "id": "tutor_id",
  "username": "tutor_username",
  "availability": []
}
```

### Get Availability

**Endpoint**: `/get/{tutor_id}`  
**Method**: `GET`  
**Response**:
```json
{
  "availability": [
    {
      "day": "Monday",
      "from": "9pm",
      "to": "12am"
    }
  ]
}
```

### Parse Availability

**Endpoint**: `/availability`  
**Method**: `POST`  
**Request Body**:
```json
{
  "content": "I am available between noon and 4pm on weekends, after 7 pm to midnight on Monday and Wednesday, and after 9pm otherwise"
}
```
**Response**:
```json
[
  {
    "day": "Friday",
    "from": "1pm",
    "to": "4pm"
  }
]
```

### Save Availability

**Endpoint**: `/save/{tutor_id}`  
**Method**: `POST`  
**Request Body**:
```json
{
  "availability": [
    {
      "day": "Monday",
      "from": "9pm",
      "to": "12am"
    }
  ]
}
```
**Response**:
```json
{
  "message": "Availability saved successfully"
}
```

## Usage

### Instructions to Set Up and Run the Application

1. **Create a Virtual Environment**:
   Navigate to the project directory and create a virtual environment:
   ```sh
   python -m venv venv
   ```

2. **Activate the Virtual Environment**:
   - For Windows:
     ```sh
     .\venv\Scripts\activate
     ```
   - For macOS/Linux:
     ```sh
     source venv/bin/activate
     ```

3. **Install Dependencies**:
   Ensure you have a `requirements.txt` file in your project directory with all the required dependencies listed. Then, run:
   ```sh
   pip install -r requirements.txt
   ```

4. **Setup Environment Variables**:
   Create a `.env` file in the project directory and add the following:
   ```
   MONGO_URL=<your_mongo_url>
   OPENAI_API_KEY=<your_openai_api_key>
   ```

5. **Run FastAPI Application**:
   Navigate to the project directory and run:
   ```sh
   uvicorn app:app --reload --port 8080
   ```

6. **Open Web Page**:
   Open `index.html`
   ```sh
   python -m http.server 8080
   ```

7. **Sign Up**:
   Create a tutor profile by entering a username and clicking "Signup".

8. **Input Availability**:
   Enter your availability in natural language and click "Send".

9. **Confirm Availability**:
   If the parsed availability is correct, click "Save".

10. **Deactivate the Virtual Environment**:
    When done, you can deactivate the virtual environment by running:
    ```sh
    deactivate
    ```

## Visual Display

The availability schedule will be displayed in a structured table format on the web page. Each time slot will be listed by day, with start and end times.

## Limitations

1. The AI parsing may not be 100% accurate for all natural language inputs.
2. Requires a stable internet connection for API calls to the OpenAI service.

## Areas of Improvement

1. **Enhance Natural Language Processing**: Improve the AI prompt and fine-tune the model for better accuracy.
2. **Error Handling**: Add more robust error handling and user feedback mechanisms.
3. **User Interface**: Enhance the UI for better user experience, including more interactive components for calendar visualization.
4. **Testing**: Add unit and integration tests to ensure the robustness of the application.
5. **Extending Functionality**: Enable editing and deleting of existing availability slots.
