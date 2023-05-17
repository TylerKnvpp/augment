# Augment

## Features

- Check Email: This feature allows you to authenticate with your Gmail account and fetch all unread emails, get summaries of the email from OpenAI's GPT, and the ability to archive emails on the spot.
- Generate Standup Update: This feature generates a standup update by fetching your previous day's activities from your Github repositories. It then uses OpenAI's GPT-4 model to generate a standup update. You can provide the tasks you're planning to do and any blockers you're experiencing, and the model will incorporate that into the update.

## Getting Started

Prerequisites: Python 3.8 or above

1. Install necessary Python packages:

```
pip install -r requirements.txt
```

or run:

```
pip install langchain openai streamlit google-auth google-auth-httplib2 google-auth-oauthlib google-api-python-client oauthlib python-dotenv colorama PyGithub googleapiclient
```

2. Generate GitHub Personal access token

To get a GitHub access token, you need to create a Personal Access Token (PAT) from your GitHub account settings. Please follow these steps:

- Go to GitHub's website and log in to your account.
- Click on your profile picture in the upper-right corner and select "Settings" from the dropdown menu.
- In the left sidebar, click on "Developer settings".
- In the left sidebar of the developer settings, click on "Personal access tokens".
- Click the "Generate new token" button at the top right.
- You will be asked to enter your password again for security reasons.
- On the new page, give your token a descriptive name under the "Note" field.
- Select the scopes (or permissions) you want to grant this token. For reading commits and pull requests, you'll need the repo scope. If you only want to read public information, you can select the public_repo sub-scope.
- After selecting the scopes, click the "Generate token" button at the bottom of the page.

You'll be taken to a new page that displays your new personal access token. Copy the token and save it somewhere safe immediately - GitHub only shows the token once for security reasons, and you won't be able to see it again.

Remember to keep your Personal Access Tokens secure! They are like passwords - anyone who has your token can make API requests on your behalf. Do not share your tokens with others, and store them securely to prevent unauthorized access to your GitHub account.

3. Enable Gmail API:

- Create a project in the [Google Developers Console](https://console.cloud.google.com).
- Enable the Gmail API.
- Create an 0Auth Client Id.
- Download the JSON key file for your service account.
- Add the JSON file to the project repo and rename it `credentials.json`

4. Duplicate `.env.example` and populate:

```
GMAIL_API_KEY=<your_gmail_api_key>
GITHUB_API_KEY=<your_github_api_key>
GITHUB_ORGANIZATION_NAME=<your_github_organization_name>
GITHUB_REPO_NAMES=<comma_separated_list_of_your_github_repo_names>
NAME=<your_name>
```

This project requires the following Python libraries to be installed:

- langchain: This library is used for the language model.
- openai: This library is used to interact with the OpenAI API.
- streamlit: This library is used to create a Web GUI for the application.
- google-auth, google-auth-httplib2, google-auth-oauthlib, google-api-python-client: These libraries are used for Google authentication and interaction with the Google API.
- oauthlib: This library is used for general OAuth support, which is used in authentication processes.
- python-dotenv: This library is used to read key-value pairs from a .env file and set them as environment variables.
- colorama: This library is used to colorize console output.
- PyGithub: This library is used to interact with the GitHub API.
- googleapiclient: This library is used to make requests to Google APIs.

### Running the Application

To run the application, use the command:

`python app.py`

This will start the application and present you with the options to Check Email, Generate Standup Update, or Exit. You can select an option by typing the corresponding number or the option name.

## Contributing

Please read CONTRIBUTING.md for details on our code of conduct, and the process for submitting pull requests to us.

## License

This project is licensed under the MIT License - see the LICENSE.md file for details.

## Acknowledgments

OpenAI for their GPT-4 model
Google for Gmail API
Github for their API
