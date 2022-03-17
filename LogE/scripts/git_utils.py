import subprocess

def is_git_installed():
    try:
        subprocess.call(['git', '--version'])
    except FileNotFoundError:
        return False
    else:
        return True

def is_in_git_repo():
    git_repo = subprocess.check_output(['git', 'rev-parse', '--is-inside-work-tree'])
    return git_repo.strip() == b'true' 


def get_last_git_commit_hash() -> str:
    if not is_git_installed():
        return "no_git_on_local_git machine"
    if not is_in_git_repo():
        return "not_in_git_repo"
    return subprocess.check_output(['git', 'rev-parse', 'HEAD']).decode('ascii').strip()[:8]