name: Schedule for GET requests

on:
  schedule:
    - cron: '*/10 * * * *'
  workflow_dispatch:

jobs:
  keep-it-alive:
    runs-on: ubuntu-latest
    steps:
      - name: Keep WebApp alive
        run: |
          for i in {1..3}
          do
            echo "Execute first GET requests"
            response=$(curl -sS https://personal-wallet.onrender.com/)
            echo "Wait 5 seconds"
            sleep 5
            echo "GET Request operation was successful"
          done