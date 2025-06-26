# Linux Agent

## Getting started

To make it easy for you to get started with GitLab, here's a list of recommended next steps.

Already a pro? Just edit this README.md and make it your own. Want to make it easy? [Use the template at the bottom](#editing-this-readme)!

## Clone the repository:

git clone https://github.com/Kumaran-eTrk/LinuxAgent.git

## Configurations :

    Modify the necessary configurations in config.ini file.

    ├── config
        - config.ini





## Build the application :

navigate to `cd src` and run the command :

`python3 setup.py sdist bdist_wheel` or `python setup.py sdist bdist_wheel`

## Install Usermonitor Agent:

    After the build, take the dist folder from src folder.



    -- run the given .ssh script file

        `source linux.sh 2>&1 | tee output.log`

    --To active python virtual env

        `source /usr/local/share/usermonitor/.venv/bin/activate`

    -- navigate (linuxdist folder)

        `cd dist`

    -- If you want to uninstall a package, use:

       `pip uninstall MonitorUser-0.1-py3-none-any.whl`

    -- Install a package named MonitorUser from a wheel file.

        `pip install MonitorUser-0.1-py3-none-any.whl`

## Start, Stop, and Check Service Status:

    --Start the service.

        `sudo systemctl start usermonitor.service`

    --Check the status of the service.

        `sudo systemctl status usermonitor.service`

    -- Stop the service.

        `sudo systemctl stop usermonitor.service`

## Enable or Disable Service:

    -- Enable the service to start automatically on boot.

        `sudo systemctl enable usermonitor.service`

    ---Disable the service to prevent it from starting automatically on boot.

        `sudo systemctl disable usermonitor.service`

## License

For open source projects, say how it is licensed.

## Project status

If you have run out of energy or time for your project, put a note at the top of the README saying that development has slowed down or stopped completely. Someone may choose to fork your project or volunteer to step in as a maintainer or owner, allowing your project to keep going. You can also make an explicit request for maintainers.
