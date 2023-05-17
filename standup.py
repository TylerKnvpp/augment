import os

from github import Github
from datetime import datetime, timedelta
from colorama import Fore, Style
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from speech import get_speech_input
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")

token = os.getenv("GITHUB_API_KEY")
organization_name = os.getenv("GITHUB_ORGANIZATION_NAME")
repo_names = os.getenv("GITHUB_REPO_NAMES").split(",")


prompt = PromptTemplate(
    input_variables=["activity", "today", "blockers"],
    template="Generate a standup update for a developer. yesterday's activity: {activity}. Their goals today: {today}. Their blockers: {blockers}",
)

llm = OpenAI(temperature=0.9, openai_api_key=API_KEY)


def get_user_and_org():
    try:
        git = Github(token)
        user = git.get_user()
        org = git.get_organization(organization_name)
        return user, org
    except Exception as e:
        print(
            f"An error occurred while authenticating the user or getting the organization: {e}"
        )
        return None, None


def get_pull_requests(repo, user, yesterday):
    created_pull_requests = []
    reviewed_pull_requests = []
    try:
        pulls = repo.get_pulls(state="all")
        for pr in pulls:
            if pr.created_at > yesterday:
                if pr.user.login == user.login:
                    created_pull_requests.append(f"Created: {pr.title}")
                elif pr.assignee and pr.assignee.login == user.login:
                    reviewed_pull_requests.append(pr.title)
    except Exception as e:
        print(
            f"An error occurred while getting pull requests from repository {repo.name}: {e}"
        )
    return created_pull_requests, reviewed_pull_requests


def get_commits(repo, user, yesterday):
    commits = []
    try:
        repo_commits = repo.get_commits(since=yesterday)
        for commit in repo_commits:
            if commit.author.login == user.login:
                commits.append(f"Created: {commit.commit.message}")
    except Exception as e:
        print(
            f"An error occurred while getting commits from repository {repo.name}: {e}"
        )
    return commits


def get_yesterdays_activities():
    user, org = get_user_and_org()

    if not user or not org:
        return

    if org not in user.get_orgs():
        print(f"The user is not associated with the organization: {organization_name}")
        return

    yesterday = datetime.now() - timedelta(1)

    yesterdays_created_pull_requests = []
    yesterdays_reviewed_pull_requests = []
    yesterdays_commits = []

    for repo_name in repo_names:
        try:
            repo = org.get_repo(repo_name)
            print(f"Checking Repo: {repo.name}")
        except Exception as e:
            print(f"An error occurred while getting the repository {repo_name}: {e}")
            continue

        created_prs, reviewed_prs = get_pull_requests(repo, user, yesterday)
        yesterdays_created_pull_requests.extend(created_prs)
        yesterdays_reviewed_pull_requests.extend(reviewed_prs)

        repo_commits = get_commits(repo, user, yesterday)
        yesterdays_commits.extend(repo_commits)

    return (
        yesterdays_created_pull_requests,
        yesterdays_reviewed_pull_requests,
        yesterdays_commits,
    )


def get_user_input(prompt, should_use_voice):
    if should_use_voice:
        print(Fore.BLUE + prompt)
        output = get_speech_input().lower()
        return output
    else:
        return input(prompt).lower()


def generate_standup(should_use_voice):
    print(Fore.BLUE + "Fetching yesterday's activities...")
    created_pull_requests, reviewed_pull_requests, commits = get_yesterdays_activities()
    # Join arrays into a single string with newline separators
    activity_summary = "\n".join(
        created_pull_requests + reviewed_pull_requests + commits
    )
    print(Fore.GREEN + "Yesterday's activities summarized!")

    # Prompt user for today's plan and blockers
    todays_plan = get_user_input(
        "What are you planning to work on today? ", should_use_voice
    )
    blockers = get_user_input("Any blockers you are experiencing? ", should_use_voice)

    print(Fore.GREEN + "Summarizing with GPT...")
    chain = LLMChain(llm=llm, prompt=prompt)
    try:
        chain = LLMChain(llm=llm, prompt=prompt)
        standup = chain.run(
            {"activity": activity_summary, "today": todays_plan, "blockers": blockers}
        )
        print(Fore.WHITE + "Generated Standup:", standup)
    except Exception as e:
        print(Fore.RED + f"An error occurred while generating standup: {e}")
        return "Stand up could not be generated."
