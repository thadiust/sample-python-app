"""
CI-only fixture: Bandit must report a finding here (B201).

Do not copy this pattern into application code.
"""

from flask import Flask

app = Flask(__name__)
app.run(debug=True)
