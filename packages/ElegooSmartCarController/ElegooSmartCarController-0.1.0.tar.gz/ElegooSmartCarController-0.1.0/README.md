
# ElegooSmartCarController

A Python library to control the Elegoo Smart Car V4.

## Installation

Install ElegooSmartCarController using pip:

```bash
pip install ElegooSmartCarController
```

## Usage

```python
from elegoosmartcarcontroller.car_control import ArduinoCarController

# Initialize the controller
car_controller = ArduinoCarController()

# Example: Move the car forward
car_controller.car_control_no_time_limit("forward", 150)
```
