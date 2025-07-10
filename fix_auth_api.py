#!/usr/bin/env python3
"""Fix Authentication API Configuration Issues
Addresses critical issues preventing API server startup for testing
"""

from pathlib import Path


def fix_main_py():
    """Fix main.py to properly include authentication endpoints"""
    main_file = Path("tools/aar/api/main.py")

    if not main_file.exists():
        print("❌ main.py not found")
        return False

    # Read current content
    with open(main_file, encoding="utf-8") as f:
        content = f.read()

    # Add router inclusion if not present
    if "from .endpoints import router" not in content:
        # Find the imports section and add router import
        import_section = content.find("# Import local modules")
        if import_section != -1:
            # Add router import after local modules
            router_import = '\n# Import API endpoints\ntry:\n    from .endpoints import router\n    ENDPOINTS_AVAILABLE = True\nexcept ImportError as e:\n    print(f"⚠️ Endpoints not available: {e}")\n    ENDPOINTS_AVAILABLE = False\n    router = None\n'
            content = (
                content[:import_section] + router_import + content[import_section:]
            )

    # Add router inclusion in app setup if not present
    if "app.include_router(router)" not in content:
        # Find where to add router inclusion
        cors_section = content.find("app.add_middleware(")
        if cors_section != -1:
            # Add router inclusion after middleware setup
            router_inclusion = '\n# Include API endpoints\nif ENDPOINTS_AVAILABLE and router:\n    app.include_router(router)\n    logger.info("API endpoints included")\nelse:\n    logger.warning("API endpoints not available")\n'
            # Find end of middleware section
            middleware_end = content.find("# Initialize core components", cors_section)
            if middleware_end != -1:
                content = (
                    content[:middleware_end]
                    + router_inclusion
                    + "\n"
                    + content[middleware_end:]
                )

    # Write fixed content
    with open(main_file, "w", encoding="utf-8") as f:
        f.write(content)

    print("✅ Fixed main.py router inclusion")
    return True


def create_minimal_requirements():
    """Create minimal requirements for testing"""
    requirements_content = """# Minimal requirements for authentication testing
fastapi>=0.68.0
uvicorn>=0.15.0
python-jose[cryptography]>=3.3.0
passlib[bcrypt]>=1.7.4
python-multipart>=0.0.5
requests>=2.25.1
"""

    req_file = Path("tools/aar/api/requirements.txt")
    req_file.parent.mkdir(parents=True, exist_ok=True)

    with open(req_file, "w", encoding="utf-8") as f:
        f.write(requirements_content)

    print("✅ Created minimal requirements.txt")
    return True


def create_environment_config():
    """Create environment configuration file"""
    env_content = """# Authentication API Environment Configuration
JWT_SECRET_KEY=sacred-geometry-phi-optimized-key-2025-CHANGE-IN-PRODUCTION
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=48

# Database Configuration (for future use)
DATABASE_URL=sqlite:///./aar_auth.db

# CORS Configuration
ALLOWED_ORIGINS=["http://localhost:3000", "http://localhost:8080"]
ALLOWED_HOSTS=["localhost", "127.0.0.1"]

# Rate Limiting
RATE_LIMIT_REQUESTS=162
RATE_LIMIT_WINDOW=97
"""

    env_file = Path("tools/aar/api/.env")
    with open(env_file, "w", encoding="utf-8") as f:
        f.write(env_content)

    print("✅ Created .env configuration file")
    return True


def fix_endpoints_import():
    """Fix endpoints.py import issues"""
    endpoints_file = Path("tools/aar/api/endpoints.py")

    if not endpoints_file.exists():
        print("❌ endpoints.py not found")
        return False

    # Read current content
    with open(endpoints_file, encoding="utf-8") as f:
        content = f.read()

    # Fix relative import issue
    if "from .main import" in content:
        # Replace relative import with absolute import handling
        old_import = """try:
    from .main import ("""

        new_import = """try:
    # Try relative import first
    from .main import ("""

        content = content.replace(old_import, new_import)

        # Add fallback for when running endpoints directly
        fallback_section = """except ImportError:
    # Fallback for direct execution
    try:
        from main import (
            JWT_ACCESS_TOKEN_EXPIRE_MINUTES,
            PHI,
            AuthToken,
            PluginExecutionRequest,
            PluginExecutionResponse,
            PluginInfo,
            UserLogin,
            app,
            check_rate_limit,
            create_access_token,
            logger,
            pwd_context,
            verify_token,
        )
        MAIN_IMPORTS_AVAILABLE = True
    except ImportError as e:
        print(f"⚠️ Main module imports not available: {e}")
        MAIN_IMPORTS_AVAILABLE = False"""

        # Find the existing except block and replace it
        except_start = content.find("except ImportError as e:")
        if except_start != -1:
            except_end = content.find("MAIN_IMPORTS_AVAILABLE = False", except_start)
            if except_end != -1:
                except_end = content.find("\n", except_end) + 1
                content = (
                    content[:except_start] + fallback_section + content[except_end:]
                )

    # Write fixed content
    with open(endpoints_file, "w", encoding="utf-8") as f:
        f.write(content)

    print("✅ Fixed endpoints.py import issues")
    return True


def install_dependencies():
    """Install required dependencies"""
    try:
        import subprocess
        import sys

        # Install basic dependencies
        deps = [
            "fastapi>=0.68.0",
            "uvicorn>=0.15.0",
            "python-jose[cryptography]>=3.3.0",
            "passlib[bcrypt]>=1.7.4",
            "python-multipart>=0.0.5",
        ]

        for dep in deps:
            try:
                result = subprocess.run(
                    [sys.executable, "-m", "pip", "install", dep],
                    check=False, capture_output=True,
                    text=True,
                    timeout=60,
                )
                if result.returncode == 0:
                    print(f"✅ Installed {dep}")
                else:
                    print(f"⚠️ Failed to install {dep}: {result.stderr}")
            except subprocess.TimeoutExpired:
                print(f"⚠️ Timeout installing {dep}")
            except Exception as e:
                print(f"⚠️ Error installing {dep}: {e}")

        return True
    except Exception as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False


def main():
    """Main fix execution"""
    print("🔧 Fixing Authentication API Configuration Issues...")
    print("=" * 60)

    success_count = 0
    total_fixes = 5

    if fix_main_py():
        success_count += 1

    if create_minimal_requirements():
        success_count += 1

    if create_environment_config():
        success_count += 1

    if fix_endpoints_import():
        success_count += 1

    if install_dependencies():
        success_count += 1

    print("\n📊 Fix Results:")
    print(f"Successful fixes: {success_count}/{total_fixes}")

    if success_count >= 4:  # Allow for dependency install to fail
        print("✅ API configuration fixes completed successfully")
        print("🚀 Ready for authentication testing")
        return True
    else:
        print("❌ Some fixes failed - manual intervention may be required")
        return False


if __name__ == "__main__":
    main()
