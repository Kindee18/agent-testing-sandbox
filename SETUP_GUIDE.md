# Project Setup Guide

This guide will help you configure the external integrations (Slack/Discord and Infracost) required for the advanced features of the AI Agent Sandbox.

## 1. Slack Alerting Setup (Recommended)
To receive instant failure notifications in Slack:
1.  Navigate to [api.slack.com/apps](https://api.slack.com/apps).
2.  Click **Create New App** -> **From Scratch**.
3.  Name it "TinyFish Agent" and select your workspace.
4.  Under **Add features and functionality**, select **Incoming Webhooks**.
5.  Toggle the switch to **Activate Incoming Webhooks**.
6.  Click **Add New Webhook to Workspace** at the bottom.
7.  Pick the channel where alerts should go and click **Allow**.
8.  **Copy the Webhook URL**. It should look like `https://hooks.slack.com/services/...`.
9.  Add this URL to your GitHub repository as a secret named `SLACK_WEBHOOK_URL`.

## 2. Discord Alerting Setup (Alternative)
If you prefer Discord over Slack:
1.  Go to your Discord Server Settings -> **Integrations**.
2.  Click **Webhooks** -> **New Webhook**.
3.  Give it a name and select a channel.
4.  Click **Copy Webhook URL**.
5.  Add this URL to your GitHub repository as a secret named `SLACK_WEBHOOK_URL`. (Discord webhooks work with the Slack-format logic we've implemented).

## 3. Infracost Setup (Price Prediction)
To see automated cost estimates on your Pull Requests:
1.  Sign up for a free account at [infracost.io](https://www.infracost.io/).
2.  Retrieve your **API Key** from your Infracost Dashboard (Settings section).
3.  Add this key to your GitHub repository as a secret named `INFRACOST_API_KEY`.

## 4. GitHub Secrets Configuration
To add these to your repo:
1.  Open your project on GitHub.
2.  Go to **Settings** -> **Secrets and variables** -> **Actions**.
3.  Click **New repository secret**.
4.  Enter the name (e.g., `SLACK_WEBHOOK_URL`) and paste the value.
5.  Repeat for other secrets as needed.

---

> [!TIP]
> Once these are set up, your GitHub Actions pipeline will automatically start using them. You can test the Slack alerts by running a manual workflow and simulating a health check failure!
