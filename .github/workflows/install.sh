#!/bin/bash
function version_gt() { test "$(printf '%s\n' "$@" | sort -V | head -n 1)" != "$1"; }
# Check if EnergyPlus env variables exist already. If not use these defaults
if [[ -z "${ENERGYPLUS_VERSION}" ]]; then
  export ENERGYPLUS_VERSION=9.2.0
fi
if [[ -z "${ENERGYPLUS_SHA}" ]]; then
  export ENERGYPLUS_SHA=921312fa1d
fi
if [[ -z "${ENERGYPLUS_INSTALL_VERSION}" ]]; then
  export ENERGYPLUS_INSTALL_VERSION=9-2-0
fi

if [[ "$OSTYPE" == "linux-gnu"* ]]; then
  if version_gt $ENERGYPLUS_VERSION 9.3.0; then
    export EXT="sh"
    export PLATFORM=Linux-Ubuntu18.04
  else
    export EXT="sh"
    export PLATFORM=Linux
  fi
  export ATTCHBASE=67022360382
  export ATTCHNUM="multipletransitionidfversionupdater-lin.tar.gz"
elif [[ "$OSTYPE" == "darwin"* ]]; then
  if version_gt $ENERGYPLUS_VERSION 9.3.0; then
    export EXT=dmg
    export PLATFORM=Darwin-macOS10.15
  else
    export EXT=dmg
    export PLATFORM=Darwin
  fi
  export ATTCHBASE=67022360547
  export ATTCHNUM="idfversionupdater-macos-v8.4.0.zip"
elif [[ "$OSTYPE" == "win"* || "$OSTYPE" == "msys"* ]]; then
  export EXT=zip
  export PLATFORM=Windows
  export ATTCHBASE=67022360088
  export ATTCHNUM="multipletransitionidfversionupdater-win.zip"
fi
# Download EnergyPlus executable
ENERGYPLUS_DOWNLOAD_BASE_URL=https://github.com/NREL/EnergyPlus/releases/download/v$ENERGYPLUS_VERSION
ENERGYPLUS_DOWNLOAD_FILENAME=EnergyPlus-$ENERGYPLUS_VERSION-$ENERGYPLUS_SHA-$PLATFORM-x86_64
ENERGYPLUS_DOWNLOAD_URL=$ENERGYPLUS_DOWNLOAD_BASE_URL/$ENERGYPLUS_DOWNLOAD_FILENAME.$EXT
echo "$ENERGYPLUS_DOWNLOAD_URL"
curl --fail -SL -C - "$ENERGYPLUS_DOWNLOAD_URL" -o "$ENERGYPLUS_DOWNLOAD_FILENAME".$EXT

# Extra downloads
EXTRAS_DOWNLOAD_URL=https://energyplushelp.freshdesk.com/helpdesk/attachments/$ATTCHBASE
curl --fail -SL -C - $EXTRAS_DOWNLOAD_URL -o $ATTCHNUM

# Install EnergyPlus and Extra Downloads
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
  sudo chmod +x "$ENERGYPLUS_DOWNLOAD_FILENAME".$EXT
  printf "y\r" | sudo ./"$ENERGYPLUS_DOWNLOAD_FILENAME".$EXT
  sudo tar zxvf $ATTCHNUM -C /usr/local/EnergyPlus-"$ENERGYPLUS_INSTALL_VERSION"/PreProcess/IDFVersionUpdater
  sudo chmod -R a+rwx /usr/local/EnergyPlus-"$ENERGYPLUS_INSTALL_VERSION"/PreProcess/IDFVersionUpdater
  sudo chmod -R a+rwx /usr/local/EnergyPlus-"$ENERGYPLUS_INSTALL_VERSION"/ExampleFiles
  # cleanup
  sudo rm "$ENERGYPLUS_DOWNLOAD_FILENAME".$EXT
  sudo rm $ATTCHNUM
elif [[ "$OSTYPE" == "darwin"* ]]; then
  # getting custom install script https://github.com/NREL/EnergyPlus/pull/7615
  curl -SL -C - https://raw.githubusercontent.com/jmarrec/EnergyPlus/40afb275f66201db5305f54df6c070d0b0cb4fc3/cmake/qtifw/install_script.qs -o install_script.qs
  sudo hdiutil attach "$ENERGYPLUS_DOWNLOAD_FILENAME".$EXT
  sudo /Volumes/"$ENERGYPLUS_DOWNLOAD_FILENAME"/"$ENERGYPLUS_DOWNLOAD_FILENAME".app/Contents/MacOS/"$ENERGYPLUS_DOWNLOAD_FILENAME" --verbose --script install_script.qs
  sudo tar zxvf $ATTCHNUM -C /Applications/EnergyPlus-"$ENERGYPLUS_INSTALL_VERSION"/PreProcess
  sudo chmod -R a+rwx /Applications/EnergyPlus-"$ENERGYPLUS_INSTALL_VERSION"/PreProcess/IDFVersionUpdater
  sudo chmod -R a+rwx /Applications/EnergyPlus-"$ENERGYPLUS_INSTALL_VERSION"/ExampleFiles
  # cleanup
  sudo rm install_script.qs
  sudo rm "$ENERGYPLUS_DOWNLOAD_FILENAME".$EXT
  sudo rm $ATTCHNUM
elif [[ "$OSTYPE" == "win"* || "$OSTYPE" == "msys"* ]]; then
  # On windows, we are simply extracting the zip file to c:\\
  echo "Extracting and Copying files to... C:\\"
  powershell Expand-Archive -Path $ENERGYPLUS_DOWNLOAD_FILENAME.$EXT -DestinationPath C:\\
  powershell Rename-Item -Path c:\\$ENERGYPLUS_DOWNLOAD_FILENAME -NewName EnergyPlusV"$ENERGYPLUS_INSTALL_VERSION"
  # extract extra downloads to destination
  DEST=C:\\EnergyPlusV"$ENERGYPLUS_INSTALL_VERSION"\\PreProcess\\IDFVersionUpdater
  echo "Extracting and Copying files to... $DEST"
  powershell Expand-Archive -Path $ATTCHNUM -DestinationPath "$DEST" -Force
  # cleanup
  rm -v $ENERGYPLUS_DOWNLOAD_FILENAME.$EXT
  rm -v $ATTCHNUM
  IDD=C:\\EnergyPlusV"$ENERGYPLUS_INSTALL_VERSION"\\Energy+.idd
  if [ -f "$IDD" ]; then
    echo "$IDD" exists
  else
    echo "$IDD" does not exist
    travis_terminate 1
  fi
fi
