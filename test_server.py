import pytest
import server


def test_get_config():
    config_data = server.get_config()
    assert config_data['targets'][0]['address'] == 'localhost:15672'
    assert config_data['targets'][0]['login'] == 'guest'
    assert config_data['targets'][0]['password'] == 'guest'


@pytest.fixture
def cli(loop, test_client):
    app = server.create_app()
    return loop.run_until_complete(test_client(app))


async def test_index(cli):
    resp = await cli.get('/')
    assert resp.status == 200

    text = await resp.text()
    assert 'RabbitMQ exporter' in text


async def test_metrics(cli):
    resp = await cli.get('/metrics')
    assert resp.status == 200

    text = await resp.text()
    assert 'rabbitmq_queues_messages' in text

