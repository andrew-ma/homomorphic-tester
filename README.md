## For testing pyfhel library (https://github.com/ibarrond/Pyfhel)
## specifically the provided examples for encrypting and running calculations on encrypted floats and ints

Install
```
# raspberry pi needed these steps
sudo apt-get install -y libssl-dev zlib1g-dev gcc g++ make build-essential cmake libpython3.8-dev

# and because it is arm, it needs special compile arguments 
"-DSEAL_BUILD_SEAL_C=1", "-DSEAL_USE_INTRIN=0"
# that should be added in setup.py's extra_compile_flags variable
# won't be able to `pip install pyfhel` for raspberry pi but will need to git clone pyfhel repo because need to modify setup.py

pip install -r requirements.txt
```

Run
```
python test.py
```

Output report is exported as report.csv

## Outputs
report_laptop.csv was generated on laptop with specs
```
i7-7700HQ, 4 cores 3.5GHz, Windows 10 on WSL 2 Ubuntu 20.04.1 x64, python3.9.0
```

report_rasppi.csv was generated on raspberry pi 3b+ with specs
```
1.4GHz, Ubuntu 20.04.1 aarch64, python3.8.5
```