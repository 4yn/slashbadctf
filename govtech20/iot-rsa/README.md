# IOT RSA Token

- [`iot-rsa-solution.md`](./iot-rsa-solution.ipynb) - Full writeup
- [`iot-rsa-solution.ipynb`](./iot-rsa-solution.ipynb) - Runnable Jupyter notebook writeup
- [`capture.logicdata`](./capture.logicdata), [`rsa_token_setup.png`](./rsa_token_setup.png), [`welcome_msg.png`](./welcome_msg.png) & [`key.txt`](./key.txt) - Challenge files
- [`capture.logicsettings`](./capture.logicsettings) - Saleae logic settings file for viewing `capture.logicdata`
- [`logic-export.csv`](./logic-export.csv) - CSV export of I2C packets from `calture.logicdata` analyzed with Saleae logic
- [`securid.c`](./securid.c) & [`compile-securid.c`](./compile-securid.c) - Original C implementation of RSA SecurID algorithm found from [seclists.org mailing list](https://seclists.org/bugtraq/2000/Dec/459)
- [`libsecurid.c`](./libsecurid.c) & [`compile-libsecurid.c`](./compile-libsecurid.c) - C library version of RSA SecurID algorithm for python bindings
- [`success.zip`](./success.zip) - Flag file obtained after submitting correct OTP to challenge site


