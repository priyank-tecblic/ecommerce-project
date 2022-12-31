#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import dotenv

def main():
    """Run administrative tasks."""
    dotenv.load_dotenv()
    print(os.environ.get("DEVELOPMENT")=="10")
    if str(os.environ.get('DEVELOPMENT'))=="1":
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.development_settings')
    else:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.production_settings')

    # if os.environ.get("DEVELOPMENT")=="10":
    #     os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.development_settings')    
    # else:
    #     os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.production_settings')    
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    print(sys.argv)
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()