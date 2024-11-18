# Chappy CLI

Chappy is a command-line interface tool that helps you set up and deploy browser-based automation testing infrastructure to cloud providers. It streamlines the process of creating, building, and deploying browser automation projects using frameworks like Selenium, Playwright, or Puppeteer.

## Prerequisites

- Python 3.x
- Docker
- Node.js (for Playwright projects)
- AWS CLI (for AWS deployments)
- Azure CLI (for Azure deployments)
- AWS CDK (for AWS deployments)

## Installation

```bash
pip install chappy
```

## Usage

### Initialize a New Project

```bash
chappy init
```

This command will:
1. Prompt for your project name
2. Let you select an automation framework (Selenium/Playwright/Puppeteer)
3. Choose a cloud provider (AWS/Azure)
4. Create a project directory with the necessary configuration files

### Build Your Project

```bash
chappy build
```

This command:
- Verifies Docker installation
- Builds a Docker image for your automation project
- Installs necessary dependencies (including Chromium and framework-specific requirements)
- For Playwright projects, runs `npm install`

### Run Locally

```bash
chappy run
```

Runs your automation project in a Docker container with:
- Volume mounting for local development
- Port 3000 exposed
- Real-time log streaming

### Deploy to Cloud

```bash
chappy deploy
```

#### AWS Deployment
- Requires AWS Account ID and default region
- Bootstraps AWS CDK
- Deploys CloudFormation stack

#### Azure Deployment
- Requires Azure App Name and location selection
- Creates resource group
- Deploys as Container App

## Project Structure

After initialization, your project will have the following structure:

```
your_project_name/
├── config.json          # Project configuration
├── Dockerfile          # Docker configuration for the environment
└── [Framework-specific files]
```

## Configuration

The `config.json` file stores your project settings:
- Project name
- Selected automation framework
- Cloud provider
- AWS/Azure specific configurations

## Commands Reference

| Command | Description |
|---------|-------------|
| `chappy version` | Display installation status |
| `chappy init` | Create new project |
| `chappy build` | Build Docker environment |
| `chappy run` | Run locally in Docker |
| `chappy deploy` | Deploy to selected cloud provider |

## Troubleshooting

### Common Issues

1. Docker Issues
   - Ensure Docker daemon is running
   - Verify Docker installation with `docker --version`

2. Build Failures
   - Check Docker daemon status
   - Ensure Dockerfile exists in project directory

3. Deployment Issues
   - For AWS: Verify AWS credentials and permissions
   - For Azure: Ensure Azure CLI is logged in

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

"""
This code sets up the pip package locally.

To set up the pip package locally, follow these steps:

1. Create a virtual environment:
     - Open a terminal or command prompt.
     - Navigate to the directory where you want to create the virtual environment.
     - Run the following command to create a virtual environment named 'myenv':
         ```
         python3 -m venv myenv
         ```

2. Activate the virtual environment:
     - On Windows, run the following command:
         ```
         myenv\Scripts\activate
         ```
     - On macOS and Linux, run the following command:
         ```
         source myenv/bin/activate
         ```

3. Install the package using pip:
     - Run the following command to install the package from the current directory:
         ```
         pip3 install .
         ```

Now you have successfully set up the pip package locally in your virtual environment.

Note: Make sure you have Python and pip installed on your system before following these steps.
"""

## License

[TBD]

