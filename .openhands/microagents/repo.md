

# Video Downloader Project Documentation

## Project Overview
This project is a universal video downloader application that allows users to download videos from various platforms. It consists of both frontend and backend components.

## File Structure
- `video-downloader-frontend/`: Contains the frontend application code
- `video_downloader_backend/`: Contains the backend API code
- `API.md`: Documentation for the API endpoints
- `DEPLOYMENT.md`: Deployment instructions
- `README.md`: Main project documentation
- `Universal_Video_Downloader_Documentation.md`: Additional documentation
- `setup.sh`: Setup script for the project

## Setup Instructions
1. Run the setup script: `./setup.sh`
2. Navigate to the frontend directory: `cd video-downloader-frontend`
3. Install dependencies: `npm install`
4. Start the frontend: `npm start`
5. In a new terminal, navigate to the backend directory: `cd ../video_downloader_backend`
6. Install dependencies: `pip install -r requirements.txt`
7. Start the backend: `python app.py`

## Testing
The project includes automated tests. To run tests:
1. For frontend: `npm test`
2. For backend: `pytest`

## Development Workflow
1. Create a new branch for each feature or bugfix
2. Make your changes and commit them
3. Push your branch and create a pull request
4. Wait for code review and approval before merging

## Contribution Guidelines
- Follow the existing code style and conventions
- Write clear commit messages
- Include tests for new features
- Document any changes to the API

