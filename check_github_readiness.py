#!/usr/bin/env python3
"""
GitHub Repository Readiness Verification Script

Run this script to verify that the project is ready to push to GitHub.
"""

import os
import json
from pathlib import Path

def check_github_readiness():
    """Verify all GitHub readiness requirements."""
    
    print("\n" + "="*70)
    print("CREDIT CARD FRAUD DETECTION - GITHUB READINESS CHECK")
    print("="*70 + "\n")
    
    root_dir = Path(__file__).parent
    checks = {
        "📋 Essential Files": [],
        "📁 Directory Structure": [],
        "🔒 Git Configuration": [],
        "📝 Documentation": [],
        "🔧 Configuration": [],
        "⚙️ Package Setup": [],
    }
    
    # Essential Files
    essential_files = [
        'README.md',
        'requirements.txt',
        'setup.py',
        'LICENSE',
        'CONTRIBUTING.md',
        '.gitignore',
    ]
    
    for file in essential_files:
        file_path = root_dir / file
        status = "✅" if file_path.exists() else "❌"
        checks["📋 Essential Files"].append(f"{status} {file}")
    
    # Directory Structure
    dirs = [
        'src',
        'app',
        'notebooks',
        'data',
        'models',
        '.github',
    ]
    
    for dir_name in dirs:
        dir_path = root_dir / dir_name
        status = "✅" if dir_path.exists() else "❌"
        checks["📁 Directory Structure"].append(f"{status} {dir_name}/")
    
    # Git Configuration
    git_files = [
        ('.gitignore', 'Should exclude venv/, __pycache__/, *.pkl, data/*.csv'),
        ('.github/workflows/tests.yml', 'CI/CD workflow'),
        ('.github/pull_request_template.md', 'PR template'),
        ('.github/ISSUE_TEMPLATE/bug_report.md', 'Bug template'),
        ('.github/ISSUE_TEMPLATE/feature_request.md', 'Feature template'),
    ]
    
    for file, desc in git_files:
        file_path = root_dir / file
        status = "✅" if file_path.exists() else "⚠️"
        checks["🔒 Git Configuration"].append(f"{status} {file} - {desc}")
    
    # Documentation
    docs = [
        ('README.md', 'Main documentation'),
        ('CONTRIBUTING.md', 'Contribution guidelines'),
        ('QUICKSTART.md', 'Quick start guide'),
        ('FRAUD_DETECTION_ANALYSIS.md', 'Methodology docs'),
        ('MODEL_STRENGTH_REPORT.md', 'Model evaluation'),
        ('GITHUB_SETUP.md', 'GitHub setup guide'),
    ]
    
    for file, desc in docs:
        file_path = root_dir / file
        status = "✅" if file_path.exists() else "⚠️"
        checks["📝 Documentation"].append(f"{status} {file} - {desc}")
    
    # Configuration Files
    configs = [
        ('.gitignore', 'Version control rules'),
        ('setup.py', 'Package configuration'),
        ('requirements.txt', 'Dependencies'),
    ]
    
    for file, desc in configs:
        file_path = root_dir / file
        status = "✅" if file_path.exists() else "❌"
        checks["🔧 Configuration"].append(f"{status} {file} - {desc}")
    
    # Package Setup
    package_checks = [
        ('src/__init__.py', 'Package marker'),
        ('app/app.py', 'Main application'),
        ('models/', 'Models directory (for trained models)'),
    ]
    
    for file, desc in package_checks:
        file_path = root_dir / file
        status = "✅" if file_path.exists() else "⚠️"
        checks["⚙️ Package Setup"].append(f"{status} {file} - {desc}")
    
    # Print results
    total_checks = 0
    passed_checks = 0
    
    for category, items in checks.items():
        print(f"\n{category}")
        print("-" * 70)
        for item in items:
            print(f"  {item}")
            if "✅" in item:
                passed_checks += 1
            total_checks += 1
    
    # Summary
    print("\n" + "="*70)
    print(f"RESULTS: {passed_checks}/{total_checks} checks passed")
    print("="*70 + "\n")
    
    if passed_checks == total_checks:
        print("🎉 PROJECT IS GITHUB READY!")
        print("\nNext steps:")
        print("  1. Update author/email/URL in setup.py")
        print("  2. Create repository on GitHub")
        print("  3. Initialize git: git init")
        print("  4. Add files: git add .")
        print("  5. Initial commit: git commit -m 'Initial commit: Production-ready fraud detection'")
        print("  6. Add remote: git remote add origin https://github.com/username/credit-card-fraud-detection.git")
        print("  7. Push: git push -u origin main")
        return True
    else:
        print("⚠️  Some checks did not pass. Review above.")
        return False

if __name__ == "__main__":
    success = check_github_readiness()
    exit(0 if success else 1)
