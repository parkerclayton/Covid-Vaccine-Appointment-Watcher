# Covid Appointment Watcher

It's late January in 2021, and my family in NYC is eligible for the COVID-19 vaccine, but they can't get an appointment. They're constantly checking https://am-i-eligible.covid19vaccine.health.ny.gov, so I wrote a script to hit the API and email them when an appointment slot is available in their area.

It's meant to be pushed to something like a pi, and run continuously.


## Installation
``` pip install -r requirements.txt```

```python watcher.py --init```

Update the template messages.json with your email, recipients email, subject and message body

## Usage

```python watcher.py```




