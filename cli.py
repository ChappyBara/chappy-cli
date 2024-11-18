import json
import shutil
import subprocess
from typing import Optional
import click
import os
import docker
from InquirerPy import prompt

class ConfigResponse:
    def __init__(
        self, 
        project_name: str,
        automation_framework: str,
        cloud_provider: str,
        aws_account_id: Optional[str] = None,
        aws_default_region: Optional[str] = None,
        azure_subscription_id: Optional[str] = None,
        azure_region: Optional[str] = None,
        gcp_project_id: Optional[str] = None,
        gcp_region: Optional[str] = None,
        project_dir: Optional[str] = None
    ):
        self.project_name = project_name
        self.automation_framework = automation_framework
        self.cloud_provider = cloud_provider
        self.aws_account_id = aws_account_id
        self.aws_default_region = aws_default_region
        self.azure_subscription_id = azure_subscription_id
        self.azure_region = azure_region
        self.gcp_project_id = gcp_project_id
        self.gcp_region = gcp_region
        self.project_dir = project_dir

class NonEmptyStringValidator(click.ParamType):
    name = 'non_empty_string'

    def convert(self, value, param, ctx):
        if not value.strip():
            self.fail('Value cannot be empty.', param, ctx)
        return value.strip()

@click.group()
@click.pass_context
def cli(ctx):
    """Chappy CLI - Browser Automation Testing Infrastructure Setup Tool"""
    ctx.ensure_object(dict)

@cli.command()
def version():
    """Display the current version of Chappy"""
    click.echo("Chappy v1.0.0")

@cli.command()
@click.pass_context
def init(ctx):
    """Initialize a new Chappy project"""
    # Project name prompt
    project_name = click.prompt("Enter Project Name", type=NonEmptyStringValidator())

    # Framework selection
    framework_questions = [
        {
            'type': 'list',
            'name': 'automation_framework',
            'message': 'Select Automation Framework:',
            'choices': ['Selenium', 'Playwright', 'Puppeteer']
        }
    ]
    framework_answer = prompt(framework_questions)
    automation_framework = framework_answer['automation_framework']

    # Cloud provider selection
    cloud_questions = [
        {
            'type': 'list',
            'name': 'cloud_provider',
            'message': 'Select Cloud Provider:',
            'choices': ['AWS', 'Azure', 'GCP']
        }
    ]
    cloud_answer = prompt(cloud_questions)
    cloud_provider = cloud_answer['cloud_provider']

    # Create and store config
    config = ConfigResponse(project_name, automation_framework, cloud_provider)
    create_project(config)
    ctx.obj['config'] = config

def create_project(config: ConfigResponse) -> bool:
    """Create project directory structure and copy template files"""
    project_dir = config.project_name.replace(" ", "_").lower()
    os.makedirs(project_dir, exist_ok=True)

    # Get template directory path
    script_dir = os.path.dirname(os.path.realpath(__file__))
    parent_dir = os.path.abspath(os.path.join(script_dir, os.pardir, os.pardir, os.pardir))

    # Map cloud provider to template directory
    cloud_templates = {
        "AWS": os.path.join(parent_dir, 'app', 'aws'),
        "Azure": os.path.join(parent_dir, 'app', 'azure'),
        "GCP": os.path.join(parent_dir, 'app', 'gcp')
    }

    source_dir = cloud_templates.get(config.cloud_provider)
    if not source_dir:
        click.echo(f"Error: Templates for {config.cloud_provider} not found.")
        return False

    if not os.path.exists(source_dir):
        click.echo(f"Error: Source directory {source_dir} does not exist.")
        return False

    # Copy template files
    try:
        shutil.copytree(source_dir, project_dir, dirs_exist_ok=True)
        config.project_dir = project_dir
        save_config(config, os.path.join(project_dir, 'config.json'))
        
        click.echo(f"Project {config.project_name} created successfully.")
        click.echo(f"Next steps:")
        click.echo(f"  cd {config.project_name}")
        click.echo(f"  chappy build")
        return True
    except Exception as e:
        click.echo(f"Error creating project: {str(e)}")
        return False

@cli.command()
@click.pass_context
def build(ctx):
    """Build Docker container for the project"""
    # Verify Docker installation
    if not check_docker():
        return

    config = load_config()
    if not config:
        return

    if not os.path.exists("Dockerfile"):
        click.echo("Error: Dockerfile not found in current directory.")
        return

    click.echo("Starting Docker build...")

    try:
        client = docker.from_env()
        # Clean up existing containers
        run_command("docker stop $(docker ps -a -q)", shell=True)
        
        # Build new image
        client.images.build(
            path='.',
            tag=config.project_name.lower(),
            rm=True
        )
        click.echo("Docker build completed successfully!")

        # Install framework-specific dependencies
        if config.automation_framework == "Playwright":
            subprocess.run(['npm', 'i'], check=True)

        click.echo("Next step: chappy run")
    except Exception as e:
        click.echo(f"Error during build: {str(e)}")

@cli.command()
@click.pass_context
def run(ctx):
    """Run the project locally in Docker"""
    try:
        config = load_config()
        if not config:
            return

        client = docker.from_env()
        volumes = {
            os.getcwd(): {
                'bind': '/usr/src/app',
                'mode': 'rw'
            }
        }
        
        container = client.containers.run(
            config.project_name.lower(),
            detach=True,
            volumes=volumes,
            ports={'3000/tcp': 3000}
        )
        
        click.echo("Docker container running. Logs:")
        for log in container.logs(stream=True):
            click.echo(log.strip())
    except Exception as e:
        click.echo(f"Error running container: {str(e)}")

@cli.command()
@click.pass_context
def deploy(ctx):
    """Deploy the project to the selected cloud provider"""
    config = load_config()
    if not config:
        return

    deployers = {
        "AWS": deploy_aws,
        "Azure": deploy_azure,
        "GCP": deploy_gcp
    }

    deployer = deployers.get(config.cloud_provider)
    if not deployer:
        click.echo(f"Error: Deployment not supported for {config.cloud_provider}")
        return

    deployer(ctx, config)

def deploy_aws(ctx, config: ConfigResponse):
    """Deploy to AWS"""
    # Get or prompt for AWS credentials
    if not config.aws_account_id:
        config.aws_account_id = click.prompt("Enter AWS Account ID", type=str)

    if not config.aws_default_region:
        # List of all AWS regions
        aws_regions = [
            'us-east-1', 'us-east-2', 'us-west-1', 'us-west-2',
            'af-south-1', 'ap-east-1', 'ap-south-1', 'ap-northeast-1',
            'ap-northeast-2', 'ap-northeast-3', 'ap-southeast-1',
            'ap-southeast-2', 'ap-southeast-3', 'ca-central-1',
            'eu-central-1', 'eu-west-1', 'eu-west-2', 'eu-west-3',
            'eu-north-1', 'eu-south-1', 'eu-south-2', 'me-south-1',
            'sa-east-1'
        ]
        config.aws_default_region = click.prompt(
            "Enter Default AWS Region",
            type=click.Choice(aws_regions)
        )

    save_config(config)

    try:
        # Bootstrap CDK
        subprocess.run([
            "cdk",
            "bootstrap",
            f"aws://{config.aws_account_id}/{config.aws_default_region}"
        ], check=True)

        # Deploy stack
        click.echo("Deploying CloudFormation stack...")
        subprocess.run(["cdk", "deploy"], check=True)
        click.echo("AWS deployment completed successfully!")
    except Exception as e:
        click.echo(f"AWS deployment failed: {str(e)}")

def deploy_azure(ctx, config: ConfigResponse):
    """Deploy to Azure"""
    if not config.azure_subscription_id:
        config.azure_subscription_id = click.prompt("Enter Azure Subscription ID", type=str)

    # List of all Azure regions
    azure_regions = [
        'eastus', 'eastus2', 'southcentralus', 'westus2', 'westus3',
        'australiaeast', 'southeastasia', 'northeurope', 'swedencentral',
        'uksouth', 'westeurope', 'centralus', 'southafricanorth',
        'centralindia', 'eastasia', 'japaneast', 'koreacentral',
        'canadacentral', 'francecentral', 'germanywestcentral',
        'norwayeast', 'switzerlandnorth', 'uaenorth', 'brazilsouth',
        'centralusstage', 'eastusstage', 'eastus2stage', 'northcentralusstage',
        'southcentralusstage', 'westusstage', 'westus2stage', 'asia',
        'asiapacific', 'australia', 'brazil', 'canada', 'europe',
        'global', 'india', 'japan', 'uk', 'unitedstates', 'eastasiastage',
        'southeastasiastage', 'centraluseuap', 'eastus2euap', 'westcentralus',
        'southafricawest', 'australiacentral', 'australiacentral2',
        'australiasoutheast', 'japanwest', 'jioindiawest', 'koreasouth',
        'southindia', 'westindia', 'canadaeast', 'francesouth', 'germanynorth',
        'norwaywest', 'switzerlandwest', 'ukwest', 'uaecentral', 'brazilsoutheast'
    ]

    if not config.azure_region:
        config.azure_region = click.prompt(
            "Enter Azure Region",
            type=click.Choice(azure_regions)
        )

    save_config(config)

    azure_app_name = config.project_name.replace(" ", "-").lower()

    try:
        # Azure deployment steps
        commands = [
            ["az", "login"],
            ["az", "account", "set", "--subscription", config.azure_subscription_id],
            ["az", "extension", "add", "--name", "containerapp", "--upgrade"],
            ["az", "group", "create", "--name", f"{azure_app_name}-group", "--location", config.azure_region],
            ["az", "containerapp", "up",
             "--name", azure_app_name,
             "--resource-group", f"{azure_app_name}-group",
             "--environment", f"{azure_app_name}-env",
             "--location", config.azure_region,
             "--source", "."]
        ]

        for cmd in commands:
            subprocess.run(cmd, check=True)
        click.echo("Azure deployment completed successfully!")
    except Exception as e:
        click.echo(f"Azure deployment failed: {str(e)}")

def deploy_gcp(ctx, config: ConfigResponse):
    """Deploy to Google Cloud Platform"""
    if not config.gcp_project_id:
        config.gcp_project_id = click.prompt("Enter GCP Project ID", type=str)

    # List of all GCP regions
    gcp_regions = [
        'asia-east1', 'asia-east2', 'asia-northeast1', 'asia-northeast2',
        'asia-northeast3', 'asia-south1', 'asia-south2', 'asia-southeast1',
        'asia-southeast2', 'australia-southeast1', 'australia-southeast2',
        'europe-central2', 'europe-north1', 'europe-west1', 'europe-west2',
        'europe-west3', 'europe-west4', 'europe-west6', 'northamerica-northeast1',
        'northamerica-northeast2', 'southamerica-east1', 'southamerica-west1',
        'us-central1', 'us-east1', 'us-east4', 'us-west1', 'us-west2',
        'us-west3', 'us-west4'
    ]

    if not config.gcp_region:
        config.gcp_region = click.prompt(
            "Enter GCP Region",
            type=click.Choice(gcp_regions)
        )

    save_config(config)

    try:
        # Authenticate with GCP
        subprocess.run(["gcloud", "auth", "login"], check=True)
        
        # Set project
        subprocess.run([
            "gcloud", "config", "set",
            "project", config.gcp_project_id
        ], check=True)

        # Build and push container image
        image_name = f"gcr.io/{config.gcp_project_id}/{config.project_name}"
        subprocess.run([
            "gcloud", "builds", "submit",
            "--tag", image_name
        ], check=True)

        # Deploy to Cloud Run
        subprocess.run([
            "gcloud", "run", "deploy", config.project_name,
            "--image", image_name,
            "--platform", "managed",
            "--region", config.gcp_region,
            "--allow-unauthenticated"
        ], check=True)

        click.echo("GCP deployment completed successfully!")
    except Exception as e:
        click.echo(f"GCP deployment failed: {str(e)}")

def check_docker() -> bool:
    """Verify Docker installation and daemon status"""
    try:
        subprocess.run(['docker', '--version'], check=True)
        return True
    except Exception as e:
        click.echo(f"Error: Docker is not installed or Docker daemon is not running. {str(e)}")
        return False

def load_config() -> Optional[ConfigResponse]:
    """Load configuration from config.json"""
    try:
        with open('config.json', 'r') as f:
            return ConfigResponse(**json.load(f))
    except FileNotFoundError:
        click.echo("Error: config.json not found. Run 'chappy init' first.")
        return None
    except Exception as e:
        click.echo(f"Error loading config: {str(e)}")
        return None

def save_config(config: ConfigResponse, path: str = 'config.json'):
    """Save configuration to config.json"""
    try:
        with open(path, 'w') as f:
            json.dump(config.__dict__, f, indent=4)
    except Exception as e:
        click.echo(f"Error saving config: {str(e)}")

def run_command(command: str, shell: bool = False) -> None:
    """Execute a shell command and handle output"""
    try:
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=shell
        )
        output, error = process.communicate()
        
        if process.returncode != 0:
            click.echo(f"Error executing: {command}")
            click.echo(f"Error message: {error.decode('utf-8')}")
        else:
            click.echo(output.decode('utf-8'))
    except Exception as e:
        click.echo(f"Command execution failed: {str(e)}")

if __name__ == "__main__":
    cli()