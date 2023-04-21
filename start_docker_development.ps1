# 5432 port is postgres
# 5000 port is website
# 9200 is elasticsearch
docker run --rm -d -p 5432:5432 -p 5000:5000 -p 9201:9200 --name flasky_container -w /app -v "$(Get-Location):/app" flasky sh -c "flask run"