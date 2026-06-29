dir := justfile_directory()

# Install the udev rule + systemd service (asks for sudo password)
install:
    sudo cp "{{dir}}/kindle-sync.service" /etc/systemd/system/
    sudo cp "{{dir}}/99-kindle-sync.rules" /etc/udev/rules.d/
    sudo systemctl daemon-reload
    sudo udevadm control --reload-rules
    @echo "Installed. Replug the Kindle to test."
