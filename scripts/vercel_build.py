"""Run production database migrations as part of a Vercel deployment."""

import os
import subprocess
import sys


if os.environ.get("VERCEL_ENV") == "production":
    print("Applying Django migrations to the production database...")
    subprocess.run(
        [sys.executable, "manage.py", "migrate", "--noinput"],
        check=True,
    )
else:
    print("Skipping production database migrations outside production.")
