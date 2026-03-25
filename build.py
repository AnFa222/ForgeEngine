import os
import sys
import subprocess
from pathlib import Path
import shutil

class Build:
    def __init__(self, main_script, output_name='game', extra_data=None, console=False, onefile=True):
        self.main_script = Path(main_script)
        if not self.main_script.exists():
            raise FileNotFoundError(f"Main script not found: {self.main_script}")

        self.output_name = output_name
        self.onefile = onefile
        self.extra_data = list(extra_data) if extra_data else []
        self.console = console

        self.engine_package = Path(__file__).resolve().parent

    def clean(self):
        for folder in ["build", "dist", "__pycache__"]:
            if Path(folder).exists():
                shutil.rmtree(folder)

    def add_asset(self, asset_path):
        p = Path(asset_path)
        if not p.exists():
            raise FileNotFoundError(f"Asset not found: {asset_path}")
        self.extra_data.append(str(p))

    def _normalize_add_data(self, path):
        p = Path(path)
        if not p.exists():
            raise FileNotFoundError(f"add-data path not found: {path}")

        if sys.platform.startswith('win'):
            sep = ';'
        else:
            sep = ':'

        dest = p.name if p.is_file() else p.name
        return f"{p}{sep}{dest}"

    def run(self):
        self.clean()

        if shutil.which('pyinstaller') is None:
            raise RuntimeError('PyInstaller not installed. Run "pip install pyinstaller" first.')

        hook_code = "import sys\n"
        hook_path = Path(self.engine_package) / "_build_hook.py"
        hook_path.write_text(hook_code)

        cmd = ['pyinstaller']

        if self.onefile:
            cmd.append('--onefile')

        for asset in self.extra_data:
            cmd.extend(['--add-data', self._normalize_add_data(asset)])

        cmd.extend(['--collect-all', 'pygame'])

        cmd.extend(['--runtime-hook', str(hook_path)])

        cmd.extend(['--name', self.output_name, str(self.main_script)])

        if not self.console:
            if sys.platform.startswith('win'):
                cmd.append('--windowed')
            else:
                cmd.append('--console')

        print('Running build:', ' '.join(cmd))
        subprocess.check_call(cmd)

        if hook_path.exists():
            hook_path.unlink()


def resource_path(rel_path):
    base = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, rel_path)