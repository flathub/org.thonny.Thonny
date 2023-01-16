# Thonny Flatpak

This is the official [Thonny](https://thonny.org/) Flatpak.

## Users

This section covers installation instructions and additional information for Thonny users.

### Install

Add the Flathub remote.

    flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo

Install the Thonny Flatpak.

    flatpak install flathub org.thonny.Thonny

### Beta

Beta versions of Thonny are made available through the `beta` branch of this repository and the Flathub Beta repository.
To use the Thonny Flatpak Beta, follow these instructions.

Add the Flathub Beta remote.

    flatpak remote-add --user flathub-beta https://flathub.org/beta-repo/flathub-beta.flatpakrepo

Install the Thonny Flatpak Beta.

    flatpak install --user flathub-beta org.thonny.Thonny//beta

## Maintainers

### Build

Get the source code.

    git clone https://github.com/flathub/org.thonny.Thonny.git
    cd org.thonny.Thonny

Add the Flathub repository.

    flatpak remote-add --user --if-not-exists flathub https://dl.flathub.org/repo/flathub.flatpakrepo

Install Flatpak Builder.

    sudo apt install flatpak-builder

Build the Flatpak.

    flatpak-builder --user --install --install-deps-from=flathub --force-clean --repo=repo build-dir org.thonny.Thonny.yaml

Run the Flatpak.

    flatpak run org.thonny.Thonny

### Update

The Python dependencies for the Flatpak are generated with the help of the [Flatpak Pip Generator](https://github.com/flatpak/flatpak-builder-tools/tree/master/pip).
This tool produces `json` files for Python packages to be included in the Flatpak manifest's `modules` section.
In order to update or add dependencies in the Flatpak, these dependencies can be generated using the following instructions.

    sudo apt -y install jq

First, install the Python dependency `requirements-parser`.

    python3 -m pip install aiohttp requirements-parser toml yq

Install the FreeDesktop SDK and Platform.

    flatpak install --user flathub org.freedesktop.Sdk//22.08

Clone the `flatpak-builder-tools` repository.

    git clone https://github.com/flatpak/flatpak-builder-tools.git

Now run the Flatpak Pip Generator script for the necessary packages.
It's probably best to do this for individual dependencies as they are added upstream, but it can be done for all of them at once as shown here.
The necessary packages are listed in the files `packaging/requirements-regular-bundle.txt` in Thonny's repository.
The following command shows how to retrieve packages from Thonny's `requirements.txt` file by producing a `bundled-python-modules.json` file.
I usually convert these to YAML and place them directly in the Flatpak manifest for readability.

    git clone https://github.com/thonny/thonny.git
    thonny_commit = $(yq -r '.[].commit' thonny-sources.yaml)
    git -C thonny checkout "$thonny_commit"
    python3 flatpak-builder-tools/pip/flatpak-pip-generator --runtime org.freedesktop.Sdk//22.08 -r thonny/packaging/requirements-regular-bundle.txt -o bundled-python-modules --checker-data

If you have `org.freedesktop.Sdk//22.08` installed in *both* the user and system installations, the Flatpak Pip Generator will choke generating the manifest.
The best option at the moment is to temporarily remove either the user or the system installation until this issue is fixed upstream.

#### bcrypt and cryptography

The Python bcrypt and cryptography libraries require a bit of extra work to update because they use Rust modules.
Whenever updating the bcrypt and cryptography libraries, their Rust dependencies may also need to be updated.
The instructions here describe how to do just this.

##### bcrypt

First, clone the bcrypt library, checking out the particular version to built as part of the Flatpak.

    git clone https://github.com/pyca/bcrypt.git
    git -C bcrypt pull
    git -C bcrypt checkout <insert commit here>

Generate the Rust sources list using the `flatpak-cargo-generator` for the cryptography library's Rust crate.

    python3 flatpak-builder-tools/cargo/flatpak-cargo-generator.py bcrypt/src/_bcrypt/Cargo.lock -o bcrypt-cargo-sources.json

This generates a `bcrypt-cargo-sources.json` file which is already incorporated into the Flatpak manifest file when building bcrypt.

##### cryptography

First, clone the cryptography library, checking out the particular version to built as part of the Flatpak.

    git clone https://github.com/pyca/cryptography.git
    git -C cryptography pull
    git -C cryptography checkout <insert commit here>

Generate the Rust sources list using the `flatpak-cargo-generator` for the cryptography library's Rust crate.

    python3 flatpak-builder-tools/cargo/flatpak-cargo-generator.py cryptography/src/rust/Cargo.lock -o cryptography-cargo-sources.json

This generates a `cryptography-cargo-sources.json` file which is already incorporated into the Flatpak manifest file when building cryptography.
