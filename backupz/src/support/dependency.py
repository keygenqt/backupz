import subprocess

from backupz.src.support.output import echo_stderr
from backupz.src.support.texts import AppTexts


# Check dependency for init
def check_dependency_init():
    # Check git application
    try:
        subprocess.run(['tar', '--version'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except (Exception,):
        echo_stderr(AppTexts.error_dependency_git())
        exit(1)

    # Check git application
    try:
        subprocess.run(['pigz', '--version'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except (Exception,):
        echo_stderr(AppTexts.error_dependency_pigz())
        exit(1)
