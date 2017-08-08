#! /usr/bin/env python
import argparse
import yaml
from aiohttp import web, ClientSession, TCPConnector, BasicAuth
import async_timeout

parser = argparse.ArgumentParser(description='Prometheus rabbitmq exporter.')
parser.add_argument('-c', '--config', dest='config', default='config.yml',
                    help='Path to configuration yaml-file. Default config.yml')
parser.add_argument('--host', dest='host', default='0.0.0.0',
                    help='HTTP server host. Default 0.0.0.0')
parser.add_argument('-p', '--port', dest='port', default=9125, type=int,
                    help='HTTP server port. Default 9125')
args = parser.parse_args()


def create_app() -> web.Application:
    app = web.Application()
    app.router.add_get('/', index)
    app.router.add_get('/metrics', metrics)
    return app


def get_config() -> dict:
    config_path = args.config
    with open(config_path) as f:
        config_data = yaml.load(f)
    return config_data

async def get_queues(target: dict) -> list:
    try:
        queues = []

        target_url = target['url']
        auth = BasicAuth(login=target['login'], password=target['password'])

        connector = TCPConnector(verify_ssl=False)
        async with ClientSession(connector=connector) as session:
            url = target_url + '/api/queues'
            with async_timeout.timeout(10):
                async with session.get(url, auth=auth) as response:
                    result = await response.json()
                    for item in result:
                        queues.append({
                            'name': item['name'],
                            'messages': item['messages']
                        })

        return queues
    except Exception as ex:
        print(ex)
        return []

async def index(request):
    return web.Response(text='<h1>RabbitMQ exporter</h1><p><a href="/metrics">Metrics</a><p>', content_type='text/html')

async def metrics(request):
    config = get_config()

    result = '# HELP rabbitmq_queues_messages Displays queue messages count\n'
    result += '# TYPE rabbitmq_queues_messages gauge\n'

    for target in config.get('targets', []):
        queues = await get_queues(target=target)
        for queue in queues:
            result += 'rabbitmq_queues_messages{target="%s",name="%s",queue="%s"} %s\n' % (
                target['url'], target['name'], queue['name'], queue['messages']
            )

    return web.Response(text=result)


if __name__ == '__main__':
    app = create_app()
    web.run_app(app, host=args.host, port=args.port)
