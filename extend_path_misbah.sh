#export PYTHONPATH="D:\Research\DFT_main\Codes\abinit_codes\src:$PYTHONPATH"

# Add src to PATH in the current session
$env:PYTHONPATH += ";D:\PhD\DFT\abinit_codes\Abinitio-Codes\src"


set PYTHONPATH=D:\PhD\DFT\abinit_codes\Abinit-Codes\src;%PYTHONPATH%

# Verify PATH
echo $env:PATH
