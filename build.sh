# Uninstall the package 'pyutube' with the '-y' flag to confirm the uninstallation without user prompt
pip uninstall pyutube -y

# Build a wheel distribution package using the 'setup.py' file
python setup.py bdist_wheel

# Install the wheel distribution package located in the 'dist' directory
pip3 install dist/*
