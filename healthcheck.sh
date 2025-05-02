#!/bin/bash
# This script is used to check the "health" of the application, 
# i.e. if it is responding to requests with a 200 OK status.
# The CMD ["python3.13",  "-m",  "streamlit", "run" "--server.port", "8000", "src/app.py"] 
# command is the default command that is run when the container is started.
#
# However, this can be changed by providing a different command when running the container.
# I.e. docker run <container-id> /wordgame/healthcheck.sh
# This script will launch the the application,(just like mentioned above,) 
# then wait for 5 seconds, make an HTTP GET request and check the response status.
# It will then kill the application and exit with 0 if the health check was OK, otherwise it will exit with 1.

(python3.13 -m streamlit run --server.port 8000 src/app.py) &
spid=$!
sleep 5
status=$(curl -L http://localhost:8000/health -o /dev/null -w '%{http_code}\n' -s)
kill $spid
if [ $status -eq 200 ]; then
    echo "Health check was OK $status"
    exit 0
else
    echo "Health check failed with $status"
    exit 1
fi
