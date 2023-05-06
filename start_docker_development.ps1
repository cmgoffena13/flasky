# 5432 port is postgres
# 5000 port is website
# 9200 is elasticsearch
# link needs redis container up first.
docker run --rm -d `
    -p 5432:5432 `
    -p 5000:5000 `
    -p 9201:9200 `
    -p 6380:6379 `
    --link redis_container:redis-server `
    --name flasky_container `
    -w /flasky `
    -v "$(Get-Location):/flasky" `
    flasky `
    sh -c "flask run"

docker logs flasky_container --follow